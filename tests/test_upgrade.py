"""Fault injection, cache and planner tests; no paid API calls."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx
from openai import OpenAI
from PIL import Image

from nimoteshot import analyzer, captures, design, pipeline, planner, providers

ROOT = Path(__file__).resolve().parents[1]


def proposal():
    return {'schema_version':1,'screens':[
        {'file':'code-editor.png','title_en':['Code tools'],'subtitle_en':'Navigate symbols',
         'title_zh':['符号工具'],'subtitle_zh':'查找代码符号',
         'analysis':{'page_type':'editor','evidence':'Go to Definition menu is visible','uncertainty':'Execution is unconfirmed','priority':9},
         'design':{'template':'compact','background':0}},
        {'file':'terminal.png','title_en':['Terminal'],'subtitle_en':'Review shell output',
         'title_zh':['终端'],'subtitle_zh':'查看命令输出',
         'analysis':{'page_type':'terminal','evidence':'Bash and terminal output are visible','uncertainty':'Connection reliability is unconfirmed','priority':8},
         'design':{'template':'showcase','background':1}}]}


class UpgradeTests(unittest.TestCase):
    def test_sdk_retry_errors_are_bounded_and_do_not_echo_credentials(self):
        for mode,expected in [('rate','429'),('server','503'),('timeout','timed out'),('network','network'),('auth','401')]:
            calls=[]
            def transport(request):
                calls.append(request)
                if mode=='timeout': raise httpx.ReadTimeout('secret-key',request=request)
                if mode=='network': raise httpx.ConnectError('secret-key',request=request)
                return httpx.Response({'rate':429,'server':503,'auth':401}[mode],
                                      headers={'retry-after-ms':'1'},json={'error':{'message':'secret-key'}})
            def client(**kwargs):
                return OpenAI(**kwargs,http_client=httpx.Client(transport=httpx.MockTransport(transport)))
            with self.subTest(mode=mode),patch('openai.OpenAI',side_effect=client),patch('openai._base_client.time.sleep'):
                with self.assertRaises(RuntimeError) as caught:
                    providers._openai_request('https://vision.example','secret-key','deepseek-flash',[])
                self.assertIn(expected,str(caught.exception))
                self.assertNotIn('secret-key',str(caught.exception))
                self.assertEqual(len(calls),1 if mode=='auth' else 3)

    def test_sdk_rate_retry_recovers_and_requests_json(self):
        calls=[]
        def transport(request):
            calls.append(json.loads(request.content))
            if len(calls)==1: return httpx.Response(429,headers={'retry-after-ms':'1'},json={'error':{'message':'busy'}})
            return httpx.Response(200,json={'id':'test','object':'chat.completion','created':0,'model':'deepseek-flash',
                                           'choices':[{'index':0,'finish_reason':'stop','message':{'role':'assistant','content':'{"screens":[]}'}}]})
        def client(**kwargs):
            return OpenAI(**kwargs,http_client=httpx.Client(transport=httpx.MockTransport(transport)))
        with patch('openai.OpenAI',side_effect=client),patch('openai._base_client.time.sleep'):
            providers._openai_request('https://vision.example','test','deepseek-flash',[{'type':'text','text':'JSON'}])
        self.assertEqual(len(calls),2)
        self.assertEqual(calls[0]['response_format'],{'type':'json_object'})
        self.assertEqual(calls[0]['max_tokens'],8192)

    def test_cache_hit_refresh_expiration_and_corruption(self):
        calls=[]
        def produce(): calls.append(1);return proposal()
        with tempfile.TemporaryDirectory() as folder:
            get=lambda refresh=False:analyzer.cached_analysis(folder,['same-content'],produce,design.validate_design,refresh=refresh)
            get();get();self.assertEqual(len(calls),1)
            get(True);self.assertEqual(len(calls),2)
            cache=next(Path(folder).glob('*.json'))
            cache.write_text('broken JSON');get();self.assertEqual(len(calls),3)
            payload=json.loads(cache.read_text());payload['expires_at']=0
            cache.write_text(json.dumps(payload))
            get();self.assertEqual(len(calls),4)
            analyzer.cached_analysis(folder,['new-image'],produce,design.validate_design)
            self.assertEqual(len(calls),5)

    def test_copy_regeneration_preserves_analysis_layout_and_order(self):
        before=proposal();new=proposal();new['screens'][0]['title_en']=['Find symbols']
        with patch.object(planner,'analyze',return_value=new) as request:
            after=planner.revise(before,'copy','App','Context',['zh'],'deepseek',api_key='test')
        self.assertEqual(request.call_args.args[0],[])
        self.assertEqual(after['screens'][0]['title_en'],['Find symbols'])
        self.assertEqual(after['screens'][0]['analysis'],before['screens'][0]['analysis'])
        self.assertEqual(after['screens'][0]['design'],before['screens'][0]['design'])
        self.assertEqual(before,proposal())
        new['screens'].reverse()
        with patch.object(planner,'analyze',return_value=new), self.assertRaisesRegex(ValueError,'mapping'):
            planner.revise(before,'copy','App','Context',['zh'],'deepseek',api_key='test')

    def test_layout_regeneration_uses_evidence_without_api_and_varies_by_page(self):
        before=proposal()
        with patch.object(planner,'analyze',side_effect=AssertionError('No API')):
            after=planner.revise(before,'layout','App','Context',['zh'],'deepseek')
        self.assertEqual([s['design']['template'] for s in after['screens']],['compact','showcase'])
        self.assertEqual([s['title_en'] for s in after['screens']],[s['title_en'] for s in before['screens']])
        with self.assertRaises(ValueError):
            planner.revise({'screens':[{'file':'a.png','title_en':['a'],'subtitle_en':'b'}]},'copy','App','Context',[],'deepseek')

    def test_capture_formats_and_invalid_content(self):
        with tempfile.TemporaryDirectory() as folder:
            for extension,format in [('png','PNG'),('jpg','JPEG'),('webp','WEBP')]:
                path=Path(folder)/('capture.'+extension);Image.new('RGB',(80,160),'navy').save(path,format=format)
            self.assertEqual(len(captures.collect(folder)),3)
            bad=Path(folder)/'bad.png';bad.write_bytes(b'not an image')
            with self.assertRaises(ValueError): captures.collect(folder)
            with self.assertRaises(ValueError): captures.unpack([{'name':'../bad.png','data':''}],folder)

    def test_model_evidence_lists_are_repaired_without_losing_facts(self):
        data=proposal();data['screens'][0]['analysis']['evidence']=['Visible file tabs','Go to Definition menu']
        repaired=design.validate_design(data)
        self.assertEqual(repaired['screens'][0]['analysis']['evidence'],'Visible file tabs\nGo to Definition menu')
        self.assertIsInstance(data['screens'][0]['analysis']['evidence'],list)

    def test_schema_mapping_crop_and_unknown_tokens(self):
        for key,value in [('scale','evil'),('alignment','absolute'),('focus_region',[0,0,1,1]),('css','body{}')]:
            data=proposal();data['screens'][0]['design'][key]=value
            with self.assertRaises(ValueError): design.validate_design(data)
        data=proposal();data['screens'][0]['target_files']={'iphone_portrait':[]}
        with self.assertRaises(ValueError): design.validate_design(data)
        data=proposal();data['brand_accent']='url(secret)'
        with self.assertRaises(ValueError): design.validate_design(data)

    def test_excessive_copy_is_rejected_instead_of_becoming_unreadable(self):
        files=[ROOT/'demo/nimotecode/originals'/name for name in ('code-editor.png','terminal.png')]
        data=proposal();data['screens'][0]['title_en']=['W'*80]
        config=pipeline.build_config('20000101-000000-abcdef','App',files,data)
        config['source_dir']=str(ROOT/'demo/nimotecode/originals')
        with self.assertRaisesRegex(ValueError,'Text does not fit'):
            pipeline.renderer.render(config,config['screens'][0],(330,717))
        data=proposal();data['screens'][0]['subtitle_en']='First line\nHidden second line'
        with self.assertRaises(ValueError):design.validate_design(data)

    def test_all_publication_languages_render_after_manual_edit(self):
        files=[ROOT/'demo/nimotecode/originals'/name for name in ('code-editor.png','terminal.png')]
        data=proposal()
        for screen in data['screens']:
            for code,title,subtitle in (('ja','コードと端末','実際の画面を確認'),('ko','코드와 터미널','실제 화면 확인'),('es','Código y terminal','Revisa tu espacio de trabajo')):
                screen['title_'+code]=[title];screen['subtitle_'+code]=subtitle
        config=pipeline.build_config('20000101-000000-abcdef','NimoteCode',files,data,locales=('zh-CN','ja-JP','ko-KR','es-ES'))
        config['source_dir']=str(ROOT/'demo/nimotecode/originals')
        for language in pipeline.renderer.locales(config):
            localized=pipeline.renderer.localized(config,language)
            for target,size in (('iphone_portrait',(330,717)),('ipad_landscape',(480,360))):
                render=pipeline.renderer.render if target=='iphone_portrait' else pipeline.renderer.render_landscape
                image=render(localized,localized['screens'][0],size,target)
                self.assertEqual(image.size,size)

    def test_all_templates_languages_devices_and_safe_layout_tokens(self):
        files=[ROOT/'demo/nimotecode/originals'/name for name in ('code-editor.png','terminal.png')]
        for template in design.TEMPLATES:
            data=proposal()
            data['screens'][0]['design'].update(template=template,focus_region='center',secondary_file='terminal.png',scale='large',alignment='right',typography='compact')
            config=pipeline.build_config('20000101-000000-abcdef','App',files,data)
            config['source_dir']=str(ROOT/'demo/nimotecode/originals')
            for locale in ('en-US','zh-CN'):
                localized=pipeline.renderer.localized(config,locale)
                for target,preset in pipeline.renderer.targets(localized).items():
                    w,h=preset['sizes'][0];factor=min(480/w,720/h);size=(round(w*factor),round(h*factor))
                    render=pipeline.renderer.render if preset['layout']=='portrait' else pipeline.renderer.render_landscape
                    with self.subTest(template=template,locale=locale,target=target):
                        image=render(localized,localized['screens'][0],size,target)
                        self.assertEqual(image.size,size);self.assertEqual(image.mode,'RGB')
