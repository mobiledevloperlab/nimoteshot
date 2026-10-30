"""Chromium E2E: SHOTNIMOTE_BROWSER_TEST=1 python -m unittest discover -s tests -p test_browser_workflow.py -v.

Optional live test uses test.md only when SHOTNIMOTE_LIVE_TEST=1, and sends exactly
code-editor.png and terminal.png. No credentials, network traces or profile changes are saved.
"""
import json
import os
import re
import tempfile
import threading
import unittest
import zipfile
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from nimoteshot import pipeline, server
from test_typography import SAMPLES

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.environ.get('SHOTNIMOTE_BROWSER_TEST') == '1', 'Browser tests run in the dedicated Chromium job')
class BrowserWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.httpd = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.httpd.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown(); cls.httpd.server_close(); cls.thread.join()
        cls.browser.close(); cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width':1280,'height':900})
        self.page = self.context.new_page()
        self.errors = []
        self.page.on('pageerror',lambda error:self.errors.append(str(error)))
        self.page.on('response',lambda response:print('Preview error:',response.text()) if '/api/preview' in response.url and response.status>=400 else None)
        self.page.goto(self.url)
        self.page.wait_for_function("document.getElementById('generate').disabled === false")
        self.page.select_option('#language','en')
        self.page.fill('#brand','NimoteCode')
        self.page.fill('#description','Mobile development workspace. Only describe features visible in each screenshot.')
        # Two languages and two real source captures; no other source is used.
        for item in self.page.locator('#locale-list input:not(:disabled)').all():
            item.set_checked(item.get_attribute('value') == 'zh-CN')
        self.page.click('#step-next')
        self.page.set_input_files('#files',[str(ROOT/'demo/nimotecode/originals'/name) for name in ('code-editor.png','terminal.png')])
        for item in self.page.locator('.export-targets input').all():
            item.set_checked(item.get_attribute('value') == 'iphone_portrait')
        self.page.click('#step-next'); self.page.click('#step-next')

    def tearDown(self):
        self.context.close()

    def wait_preview(self):
        self.page.wait_for_function("['ready','error'].includes(document.getElementById('preview-status')?.dataset.state)",timeout=60000)
        self.assertEqual(self.page.locator('#preview-status').get_attribute('data-state'),'ready',self.page.locator('#preview-status').inner_text())
        self.assertEqual(self.page.locator('.design-rendered-preview:not([hidden])').count(),2)

    def edit_and_export(self):
        self.page.wait_for_selector('#design-editor')
        self.wait_preview()
        self.page.locator('[data-copy-key=title_en][data-screen-index="1"]').fill('代码工具\nOn your phone')
        self.wait_preview()
        self.page.get_by_label('Copy version to edit',exact=True).select_option('zh')
        self.wait_preview()
        self.page.locator('[data-copy-key=title_zh][data-screen-index="1"]').fill('代码工具\n随身使用')
        self.wait_preview()
        # Cover new compositions, safe crop tokens and ordering through actual DOM events.
        self.page.get_by_label('Template',exact=True).nth(0).select_option('detail')
        self.wait_preview()
        self.page.get_by_label('Template',exact=True).nth(1).select_option('duo')
        self.wait_preview()
        self.page.get_by_label('Move up 2',exact=True).click(); self.wait_preview()
        self.page.set_viewport_size({'width':390,'height':844})
        self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'))
        for theme in ('light','dark'):
            self.page.evaluate('(theme)=>document.documentElement.dataset.theme=theme',theme)
            for selector in ('.brand-icon','.footer-logo'):
                self.assertTrue(self.page.locator(selector).evaluate('(image)=>image.complete && image.naturalWidth > 0'))
        self.page.click('#export-design')
        self.page.wait_for_function("!document.getElementById('download').classList.contains('hidden') || !document.getElementById('error').classList.contains('hidden')",timeout=180000)
        self.assertTrue(self.page.locator('#error').evaluate('(e)=>e.classList.contains("hidden")'),self.page.locator('#error').inner_text())
        href=self.page.locator('#download').get_attribute('href')
        response=self.context.request.get(self.url+href)
        self.assertEqual(response.status,200)
        import io
        with zipfile.ZipFile(io.BytesIO(response.body())) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(len([name for name in archive.namelist() if name.endswith('.png')]),28)
        self.assertEqual(self.errors,[])
        return href

    def test_manual_design_edit_preview_reorder_and_zip_without_ai_key(self):
        with patch.object(pipeline,'analyze',side_effect=AssertionError('Manual editing must not call AI')):
            self.page.check('#manual-mode');self.page.click('#generate')
            self.page.wait_for_selector('#design-editor')
            self.assertEqual(self.page.locator('.design-screen-body').count(),2)
            self.assertEqual(self.page.locator('.design-original img').count(),2)
            positions=self.page.locator('.design-screen-body').first.evaluate("node=>({source:node.querySelector('.design-source').getBoundingClientRect().left,configuration:node.querySelector('.design-configuration').getBoundingClientRect().left})")
            self.assertLess(positions['source'],positions['configuration'])
            self.edit_and_export()
            self.assertTrue(self.page.locator('#export-location').is_visible())
            self.assertTrue(self.page.locator('#export-path').inner_text().endswith('/exports'))
            self.assertTrue(self.page.locator('#open-export').is_visible())
            self.assertEqual(self.page.locator('#export-progress-value').inner_text(),'100%')

    def test_ai_failure_keeps_manual_workflow_available(self):
        with patch.object(pipeline,'cached_analysis',side_effect=lambda directory,identity,produce,validate,*args,**kwargs:validate(produce())), patch.object(pipeline,'analyze',side_effect=ValueError('Vision model did not return valid JSON')):
            self.page.fill('#api-key','fake-test-key');self.page.click('#generate')
            self.page.wait_for_function("document.getElementById('error').textContent.includes('invalid design')",timeout=30000)
            self.page.check('#manual-mode');self.page.click('#generate');self.wait_preview()
        self.assertEqual(self.errors,[])

    def test_new_editor_controls_follow_all_five_interface_languages(self):
        self.page.check('#manual-mode');self.page.click('#generate');self.wait_preview()
        self.page.locator('[data-copy-key=title_en][data-screen-index="1"]').fill('Keep my copy')
        for language in ('zh','en','ja','ko','es'):
            self.page.select_option('#language',language)
            labels=self.page.evaluate('(language)=>editorMessages[language]',language)
            self.assertEqual(self.page.get_by_role('button',name=labels['exportDesign'],exact=True).count(),1)
            self.assertEqual(self.page.locator('.design-rework').count(),0)
            self.assertEqual(self.page.locator('.design-source figcaption').first.inner_text(),labels['livePreview'])
            self.assertEqual(self.page.locator('#copy-language-help').inner_text(),labels['copyLocaleHelp'])
            self.assertEqual(self.page.locator('#copy-language').get_attribute('aria-label'),labels['copyLocale'])
            self.assertEqual(self.page.get_by_label(labels['editTemplate'],exact=True).count(),2)
            self.assertEqual(self.page.locator('[data-i18n=manualMode]').inner_text(),labels['manualMode'])
            self.assertEqual(self.page.locator('[data-copy-key=title_en][data-screen-index="1"]').input_value(),'Keep my copy')
            self.assertEqual(self.page.get_by_label(labels['editTemplate'],exact=True).first.locator('option[value=duo]').inner_text(),labels['duo'])
        self.assertEqual(self.errors,[])

    def test_edits_refresh_rendered_images_and_preview_failure_can_retry(self):
        requests=[]
        self.page.on('request',lambda request:requests.append(request.post_data_json) if request.url.endswith('/api/preview') else None)
        with patch.object(pipeline,'analyze',side_effect=AssertionError('Preview must not call AI')):
            self.page.check('#manual-mode');self.page.click('#generate');self.wait_preview()
            image=self.page.locator('.design-rendered-preview').first
            before=image.get_attribute('src')
            title=self.page.locator('[data-copy-key=title_en][data-screen-index="1"]')
            subtitle=self.page.locator('[data-copy-key=subtitle_en][data-screen-index="1"]')
            title.fill('Code tools')
            self.assertEqual(self.page.locator('#preview-status').get_attribute('data-state'),'loading')
            subtitle.fill('Build on your phone')
            self.wait_preview()
            self.assertNotEqual(image.get_attribute('src'),before)
            self.assertEqual(self.page.locator('.design-screen').first.locator('.design-rendered-preview').count(),1)
            self.assertTrue(self.page.locator('#retry-preview').is_hidden())

            self.page.route('**/api/preview',lambda route:route.fulfill(status=500,json={'error':'Preview failed'}),times=1)
            title.fill('Edit anywhere')
            self.page.wait_for_function("document.getElementById('preview-status').dataset.state === 'error'")
            self.assertTrue(self.page.locator('#retry-preview').is_visible())
            self.assertIn('preview-stale',image.get_attribute('class'))
            self.page.click('#retry-preview');self.wait_preview()
            self.assertEqual(requests[-1]['preview_indices'],[0])
            self.assertNotIn('preview-stale',image.get_attribute('class'))
            self.assertEqual(title.input_value(),'Edit anywhere')
        self.assertEqual(self.errors,[])

    def test_local_edits_render_one_screen_and_global_changes_render_all(self):
        requests=[]
        self.page.on('request',lambda request:requests.append(request.post_data_json) if request.url.endswith('/api/preview') else None)
        self.page.evaluate("""() => {
            const target=document.querySelector('.export-targets input[value="iphone_landscape"]');
            target.checked=true;target.dispatchEvent(new Event('change',{bubbles:true}));
        }""")
        self.page.check('#manual-mode');self.page.click('#generate');self.wait_preview()
        self.assertEqual(requests[-1]['preview_indices'],[0,1])
        self.page.evaluate("window.untouchedPreview=document.querySelectorAll('.design-rendered-preview')[1]")
        unchanged=self.page.locator('.design-rendered-preview').nth(1).get_attribute('src')
        for key,value in (('title_en','Edit code'),('subtitle_en','Find your symbols')):
            self.page.locator(f'[data-copy-key={key}][data-screen-index="1"]').fill(value)
            self.wait_preview()
            self.assertEqual(requests[-1]['preview_indices'],[0])
            self.assertEqual(self.page.locator('.design-rendered-preview').nth(1).get_attribute('src'),unchanged)
        self.page.get_by_label('Template',exact=True).first.select_option('detail');self.wait_preview()
        self.assertEqual(requests[-1]['preview_indices'],[0])
        self.assertTrue(self.page.evaluate("window.untouchedPreview===document.querySelectorAll('.design-rendered-preview')[1]"))
        self.page.locator('.design-configuration').first.locator('details').last.locator('summary').click()
        self.page.get_by_label('Detail region',exact=True).select_option('top');self.wait_preview()
        self.assertEqual(requests[-1]['preview_indices'],[0])
        self.page.get_by_label('Brand accent',exact=True).fill('#dd3344');self.wait_preview()
        self.assertEqual(requests[-1]['preview_indices'],[0,1])
        self.page.get_by_label('Copy version to edit',exact=True).select_option('zh');self.wait_preview()
        self.assertEqual(requests[-1]['preview_indices'],[0,1])
        self.assertEqual(requests[-1]['preview_locale'],'zh-CN')
        self.page.get_by_label('Preview device',exact=True).select_option('iphone_landscape');self.wait_preview()
        self.assertEqual(requests[-1]['preview_indices'],[0,1])
        self.assertEqual(requests[-1]['preview_target'],'iphone_landscape')
        self.page.get_by_label('Move up 2',exact=True).click();self.wait_preview()
        self.assertEqual(requests[-1]['preview_indices'],[0,1])
        self.assertEqual(requests[-1]['proposal']['screens'][0]['file'],'terminal.png')
        self.assertEqual(self.errors,[])

    def test_batched_edits_and_superseded_response_do_not_lose_pending_screens(self):
        requests=[]
        self.page.on('request',lambda request:requests.append(request.post_data_json) if request.url.endswith('/api/preview') else None)
        self.page.check('#manual-mode');self.page.click('#generate');self.wait_preview()
        requests.clear()
        # Both edits occur within one debounce interval.
        self.page.evaluate("""() => {
            document.querySelectorAll('[data-copy-key=title_en]').forEach((field,index)=>{
                field.value='Code '+index;field.dispatchEvent(new Event('input',{bubbles:true}));
            });
        }""")
        self.wait_preview()
        self.assertEqual(len(requests),1)
        self.assertEqual(requests[-1]['preview_indices'],[0,1])
        # Hold an actual successful response after transport completes, so abort
        # alone cannot protect against it committing over the next response.
        self.page.evaluate("""() => {
            const original=window.fetch;
            window.holdNextPreview=true;
            window.fetch=async(...args)=>{
                if(args[0]==='/api/preview' && window.holdNextPreview){
                    window.holdNextPreview=false;
                    const response=await original(...args);
                    return new Promise(resolve=>{
                        window.releaseHeldPreview=()=>resolve(response);
                        window.heldPreviewReady=true;
                    });
                }
                return original(...args);
            };
        }""")
        self.page.locator('[data-copy-key=title_en][data-screen-index="1"]').fill('First edit')
        self.page.wait_for_function('window.heldPreviewReady === true')
        self.assertEqual(requests[-1]['preview_indices'],[0])
        self.page.locator('[data-copy-key=title_en][data-screen-index="2"]').fill('Second edit')
        self.wait_preview()
        self.assertEqual(requests[-1]['preview_indices'],[0,1])
        latest=self.page.locator('.design-rendered-preview').evaluate_all('(images)=>images.map(image=>image.src)')
        self.page.evaluate('async()=>{window.releaseHeldPreview();await new Promise(resolve=>setTimeout(resolve,0));}')
        self.assertEqual(self.page.locator('.design-rendered-preview').evaluate_all('(images)=>images.map(image=>image.src)'),latest)
        self.assertEqual(self.page.locator('#preview-status').get_attribute('data-state'),'ready')
        self.assertEqual(self.errors,[])

    def test_major_language_text_in_english_fields_and_ime_commit(self):
        requests=[]
        self.page.on('request',lambda request:requests.append(request.post_data_json) if request.url.endswith('/api/preview') else None)
        with patch.object(pipeline,'analyze',side_effect=AssertionError('Text editing must not call AI')):
            self.page.check('#manual-mode');self.page.click('#generate');self.wait_preview()
            title=self.page.locator('[data-copy-key=title_en][data-screen-index="1"]')
            subtitle=self.page.locator('[data-copy-key=subtitle_en][data-screen-index="1"]')
            image=self.page.locator('.design-rendered-preview').first
            unchanged=self.page.locator('.design-rendered-preview').nth(1).get_attribute('src')
            previous=image.get_attribute('src')
            for language,text,sub in SAMPLES:
                with self.subTest(language=language):
                    title.fill(text);subtitle.fill(sub)
                    if pipeline.renderer.needs_complex_layout(text+sub) and not self.page.evaluate('state.options.text_shaping'):
                        self.page.wait_for_function("document.getElementById('preview-status').dataset.state === 'error'")
                        self.assertEqual(self.page.locator('#preview-status').inner_text(),self.page.evaluate('editorMessages.en.errorShaping'))
                        continue
                    self.wait_preview()
                    self.assertEqual(requests[-1]['preview_indices'],[0])
                    self.assertEqual(requests[-1]['preview_locale'],'en-US')
                    self.assertNotEqual(image.get_attribute('src'),previous)
                    self.assertEqual(self.page.locator('.design-rendered-preview').nth(1).get_attribute('src'),unchanged)
                    previous=image.get_attribute('src')
            requests.clear()
            self.page.evaluate("""async() => {
                const field=document.querySelector('[data-copy-key=title_en]');
                field.dispatchEvent(new CompositionEvent('compositionstart',{bubbles:true}));
                field.value='zhongwen';
                field.dispatchEvent(new InputEvent('input',{bubbles:true,isComposing:true,inputType:'insertCompositionText'}));
                await new Promise(resolve=>setTimeout(resolve,450));
            }""")
            self.assertEqual(requests,[])
            self.page.evaluate("""() => {
                const field=document.querySelector('[data-copy-key=title_en]');field.value='中文输入';
                field.dispatchEvent(new CompositionEvent('compositionend',{bubbles:true,data:'中文输入'}));
                field.dispatchEvent(new InputEvent('input',{bubbles:true,isComposing:false}));
            }""")
            self.wait_preview()
            self.assertEqual(len(requests),1)
            self.assertEqual(requests[0]['proposal']['screens'][0]['title_en'],['中文输入'])
            self.assertEqual(requests[0]['preview_indices'],[0])
            title.fill('🦄')
            self.page.wait_for_function("document.getElementById('preview-status').dataset.state === 'error'")
            self.assertEqual(self.page.locator('#preview-status').inner_text(),self.page.evaluate('editorMessages.en.errorFont'))
            title.fill('代码工具');self.wait_preview()
        self.assertEqual(self.errors,[])

    def test_copy_version_switch_preserves_independent_text_and_chooses_matching_preview(self):
        requests=[]
        self.page.on('request',lambda request:requests.append(request.post_data_json) if request.url.endswith('/api/preview') else None)
        self.page.check('#manual-mode');self.page.click('#generate');self.wait_preview()
        self.assertEqual(self.page.locator('#copy-language').get_attribute('aria-describedby'),'copy-language-help')
        english=self.page.locator('[data-copy-key=title_en][data-screen-index="1"]')
        english.fill('英文版本中文');self.wait_preview()
        self.assertEqual(requests[-1]['preview_locale'],'en-US')
        english_image=self.page.locator('.design-rendered-preview').first.get_attribute('src')
        self.page.locator('#copy-language').select_option('zh');self.wait_preview()
        chinese=self.page.locator('[data-copy-key=title_zh][data-screen-index="1"]')
        self.assertNotEqual(chinese.input_value(),'英文版本中文')
        chinese.fill('中文版自定义');self.wait_preview()
        self.assertEqual(requests[-1]['preview_locale'],'zh-CN')
        chinese_image=self.page.locator('.design-rendered-preview').first.get_attribute('src')
        self.assertNotEqual(english_image,chinese_image)
        self.page.locator('#copy-language').select_option('en');self.wait_preview()
        self.assertEqual(english.input_value(),'英文版本中文')
        self.assertEqual(self.page.locator('.design-rendered-preview').first.get_attribute('src'),english_image)
        self.page.locator('#copy-language').select_option('zh');self.wait_preview()
        self.assertEqual(chinese.input_value(),'中文版自定义')
        self.assertEqual(self.page.locator('.design-rendered-preview').first.get_attribute('src'),chinese_image)
        self.assertEqual(self.errors,[])

    def test_all_output_language_options_reach_the_matching_copy_and_preview(self):
        requests=[]
        self.page.on('request',lambda request:requests.append(request.post_data_json) if request.url.endswith('/api/preview') else None)
        self.assertEqual(self.page.locator('#locale-list input').count(),len(pipeline.OUTPUT_LOCALES))
        shaping=self.page.evaluate('state.options.text_shaping')
        available={locale:options for locale,options in pipeline.OUTPUT_LOCALES.items() if not options['requires_shaping'] or shaping}
        self.page.evaluate("""() => document.querySelectorAll('#locale-list input:not(:disabled)').forEach(field=>{
            field.checked=true;field.dispatchEvent(new Event('change',{bubbles:true}));
        })""")
        self.page.check('#manual-mode');self.page.click('#generate');self.wait_preview()
        self.assertEqual(self.page.locator('#copy-language option').count(),len(available))
        for locale,options in available.items():
            with self.subTest(locale=locale):
                code=options['code']
                self.page.locator('#copy-language').select_option(code);self.wait_preview()
                title=self.page.locator(f'[data-copy-key=title_{code}][data-screen-index="1"]')
                self.assertEqual(title.input_value(),options['placeholder_title'])
                title.fill(options['placeholder_title']+'\nGit');self.wait_preview()
                self.assertEqual(requests[-1]['preview_locale'],locale)
                self.assertEqual(requests[-1]['preview_indices'],[0])
        for locale,options in available.items():
            self.page.locator('#copy-language').select_option(options['code']);self.wait_preview()
            self.assertEqual(self.page.locator(f'[data-copy-key=title_{options["code"]}][data-screen-index="1"]').input_value(),options['placeholder_title']+'\nGit')
        self.assertEqual(self.errors,[])

    def test_adding_an_output_language_after_planning_initializes_editable_placeholders(self):
        self.page.check('#manual-mode');self.page.click('#generate');self.wait_preview()
        self.page.locator('[data-copy-key=title_en][data-screen-index="1"]').fill('Keep my edits');self.wait_preview()
        self.page.evaluate("""() => {
            editingProposal.screens.forEach(screen=>{delete screen.title_fr;delete screen.subtitle_fr;});
            const field=document.querySelector('#locale-list input[value="fr-FR"]');
            field.checked=true;field.dispatchEvent(new Event('change',{bubbles:true}));
        }""")
        self.wait_preview()
        self.assertEqual(self.page.locator('#result-summary').inner_text(),self.page.evaluate('editorMessages.en.addedLanguage'))
        self.page.locator('#copy-language').select_option('fr');self.wait_preview()
        title=self.page.locator('[data-copy-key=title_fr][data-screen-index="1"]')
        self.assertEqual(title.input_value(),pipeline.OUTPUT_LOCALES['fr-FR']['placeholder_title'])
        title.fill('Outils mobiles');self.wait_preview()
        self.page.locator('#copy-language').select_option('en');self.wait_preview()
        self.assertEqual(self.page.locator('[data-copy-key=title_en][data-screen-index="1"]').input_value(),'Keep my edits')
        self.assertEqual(self.errors,[])

    def test_unavailable_complex_languages_have_setup_guidance_before_generation(self):
        def without_shaping(route):
            response=route.fetch();data=response.json();data['text_shaping']=False
            route.fulfill(response=response,json=data)
        self.page.route('**/api/options',without_shaping)
        self.page.reload();self.page.wait_for_function("document.getElementById('generate').disabled === false")
        for locale,options in pipeline.OUTPUT_LOCALES.items():
            field=self.page.locator(f'#locale-list input[value="{locale}"]')
            self.assertEqual(field.is_disabled(),locale=='en-US' or options['requires_shaping'])
            if options['requires_shaping']:
                self.assertFalse(field.is_checked())
        self.assertTrue(self.page.locator('#language-availability').is_visible())
        self.assertTrue(self.page.locator('#language-availability a').get_attribute('href').startswith('/docs/guide'))
        self.assertEqual(self.errors,[])

    def test_ai_rework_is_collapsed_and_explains_overwrites(self):
        self.page.check('#manual-mode');self.page.click('#generate');self.wait_preview()
        # Attach the evidence an AI plan supplies; no provider request is needed.
        self.page.evaluate("""() => {
            editingProposal.screens.forEach(screen=>screen.analysis={evidence:'Visible code editor',page_type:'editor'});
            showDesignEditor();
        }""")
        self.wait_preview()
        for language in ('en','zh','ja','ko','es'):
            self.page.select_option('#language',language)
            labels=self.page.evaluate('(language)=>editorMessages[language]',language)
            self.assertFalse(self.page.locator('.design-rework').evaluate('(node)=>node.open'))
            self.assertTrue(self.page.get_by_role('button',name=labels['exportDesign'],exact=True).is_visible())
            self.page.locator('.design-rework > summary').click()
            for label,help_key in (('regenerateCopy','copyHelp'),('recommendLayouts','layoutHelp'),('reanalyze','reanalyzeHelp')):
                self.assertTrue(self.page.get_by_role('button',name=labels[label],exact=True).is_visible())
                self.assertTrue(self.page.get_by_text(labels[help_key],exact=True).is_visible())
        self.assertEqual(self.errors,[])

    def test_document_pages_render_source_content(self):
        documents = {
            'guide-zh': '使用指南',
            'guide': 'User guide',
            'contributing': '参与贡献',
            'security': '安全与数据',
            'license': '许可证',
            'notices': '第三方声明',
        }
        self.page.set_viewport_size({'width': 390, 'height': 844})
        for slug, expected_title in documents.items():
            with self.subTest(document=slug):
                self.page.goto(f'{self.url}/docs/{slug}')
                self.page.wait_for_function("document.querySelectorAll('#doc-content > *').length > 2")
                self.assertEqual(self.page.locator('#doc-title').inner_text(), expected_title)
                self.assertGreater(len(self.page.locator('#doc-content').inner_text()), 500)
                self.assertEqual(self.page.locator('.docs-sidebar a.active').count(), 1)
                if slug in ('guide','guide-zh'):
                    image=self.page.locator('.docs-figure img[src="/assets/redefine_promotion.png"]')
                    self.assertEqual(image.count(),1)
                    image.scroll_into_view_if_needed()
                    self.page.wait_for_function("document.querySelector('.docs-figure img').naturalWidth > 0")
                    self.assertEqual(image.get_attribute('alt').strip()!='',True)
                    self.assertEqual(self.page.locator('#'+('quick-start' if slug=='guide' else '快速开始')).count(),1)
                self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'))
        self.assertEqual(self.errors, [])

    @unittest.skipUnless(os.environ.get('SHOTNIMOTE_LIVE_TEST') == '1','Live API testing is explicitly opt-in')
    def test_live_two_image_analysis_copy_layout_and_export(self):
        text=(ROOT/'test.md').read_text(encoding='utf-8')
        match=re.search(r'(?im)^\s*apikey\s*[:：]\s*(.+?)\s*$',text)
        self.assertIsNotNone(match,'test.md requires an apikey field')
        self.page.select_option('#provider','deepseek')
        self.page.fill('#api-key',match.group(1).strip().strip('`\"\''))
        self.page.click('#generate');self.page.wait_for_selector('#design-editor',timeout=180000)
        self.wait_preview()
        self.page.locator('.design-rework > summary').click()
        self.page.get_by_role('button',name='Regenerate copy',exact=True).click()
        self.page.wait_for_function("document.getElementById('generate').disabled === false",timeout=180000)
        self.assertTrue(self.page.locator('#error').evaluate('(e)=>e.classList.contains("hidden")'))
        self.page.locator('.design-rework > summary').click()
        self.page.get_by_role('button',name='Recommend layouts',exact=True).click()
        self.page.wait_for_function("document.getElementById('generate').disabled === false",timeout=30000)
        self.wait_preview()
        templates=self.page.get_by_label('Template',exact=True).evaluate_all('(items)=>items.map(item=>item.value)')
        self.assertEqual(set(templates),{'compact','showcase'})
        href=self.edit_and_export()
        output=ROOT/'test_outputs';output.mkdir(exist_ok=True)
        (output/'browser-live-result.json').write_text(json.dumps({'download':href,'templates':templates,'source_count':2,'pngs':28,'browser_errors':self.errors},indent=2), encoding='utf-8')
        self.page.screenshot(path=str(output/'browser-live-mobile.png'),full_page=True)
