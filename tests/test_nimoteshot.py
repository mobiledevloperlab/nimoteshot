import json
import io
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from nimoteshot import pipeline, providers, context, settings


RUN_ID = '20261028-120000-abcdef'


class StudioTests(unittest.TestCase):
    def proposal(self):
        return {"screens": [{"file": "capture.png", "title_en": ["Real editor"],
                             "subtitle_en": "Edit your files.", "title_zh": ["真实编辑器"],
                             "subtitle_zh": "编辑你的文件。", "locale_files": {"zh-CN": "chinese.png"}}]}

    def test_provider_adapters_for_global_and_mainland_models(self):
        with tempfile.TemporaryDirectory() as temp:
            image = Path(temp) / 'capture.png'
            Image.new('RGB', (64, 128), '#143045').save(image)
            responses = {
                'gemini': {"candidates": [{"content": {"parts": [{"text": json.dumps(self.proposal())}]}}]},
                'claude': {"content": [{"type": "text", "text": json.dumps(self.proposal())}]},
                'ollama': {"message": {"content": json.dumps(self.proposal())}},
                'qwen': {"choices": [{"message": {"content": json.dumps(self.proposal())}}]},
                'zhipu': {"choices": [{"message": {"content": json.dumps(self.proposal())}}]},
                'doubao': {"choices": [{"message": {"content": json.dumps(self.proposal())}}]},
                'hunyuan': {"choices": [{"message": {"content": json.dumps(self.proposal())}}]},
                'openai': {"choices": [{"message": {"content": json.dumps(self.proposal())}}]},
                'compatible': {"choices": [{"message": {"content": json.dumps(self.proposal())}}]}
            }
            for provider, response in responses.items():
                compatible = providers.PROVIDERS[provider]['protocol'] == 'openai_compatible'
                mock_target = '_openai_request' if compatible else '_request'
                mock_value = json.dumps(self.proposal()) if compatible else response
                with self.subTest(provider=provider), patch.object(providers, mock_target, return_value=mock_value) as request:
                    generic = provider in {'doubao', 'compatible'}
                    result = providers.analyze([image], 'Describe the app', provider,
                                               model='qwen3-vl:8b' if provider == 'ollama' else ('vision-model' if generic else ''),
                                               base_url='https://vision.example/v1' if provider == 'compatible' else '', api_key='test-key')
                    self.assertEqual(result, self.proposal())
                    self.assertEqual(request.call_count, 1)
            model, endpoint, key = providers.choice('openai', 'gpt-6.1-terra', api_key='test-key')
            self.assertEqual((model, endpoint, key), ('gpt-6.1-terra', 'https://api.openai.com/v1', 'test-key'))
            self.assertEqual(providers.choice('qwen', api_key='test-key')[1], 'https://dashscope.aliyuncs.com/compatible-mode/v1')
            with patch.object(providers.urllib.request, 'urlopen', return_value=io.BytesIO(b'{}')):
                self.assertTrue(providers.check_connection('gemini', api_key='test-key')['ready'])

    def test_context_and_style_requirements(self):
        with self.assertRaises(ValueError):
            pipeline.prepare_context('Example', '', '')
        with patch.object(pipeline, 'fetch_website', return_value='A public app website'):
            self.assertIn('public app', pipeline.prepare_context('Example', '', 'https://example.com')[3])
        self.assertTrue({'editorial', 'soft_gradient', 'midnight', 'bold_color'}.issubset(pipeline.STYLE_MAP))
        categories = {}
        for style in pipeline.STYLE_MAP.values():
            if style.get('category'):
                categories[style['category']] = categories.get(style['category'], 0) + 1
        self.assertEqual(len(categories), 8)
        self.assertTrue(all(count == 3 for count in categories.values()))
        self.assertEqual(len(pipeline.STYLES['prompt_presets']), 10)
        with self.assertRaises(ValueError):
            pipeline.fetch_website('https://127.0.0.1/private')
        parser = context._Text()
        parser.feed('<meta name="description" content="An editor"><script>private()</script><h1>Write code</h1>')
        self.assertIn('An editor', parser.parts)
        self.assertIn('Write code', parser.parts)
        self.assertNotIn('private()', parser.parts)

    def test_local_profile_and_codex_cli_configuration(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(settings, 'config_path', return_value=Path(temp) / 'config.json'):
            saved = settings.save('qwen', model='qwen3-vl-plus', api_key='secret')
            self.assertTrue(saved.is_file())
            self.assertEqual(settings.describe()['qwen']['model'], 'qwen3-vl-plus')
            self.assertFalse('secret' in str(settings.describe()))
            with patch.object(providers, 'profile', return_value=settings.profile('qwen')):
                self.assertEqual(providers.choice('qwen')[2], 'secret')
        with patch.object(providers.shutil, 'which', return_value='/usr/bin/codex'), \
             patch.object(providers.subprocess, 'run') as run:
            self.assertTrue(providers.check_connection('codex')['ready'])
            run.assert_called_once()

    def test_each_style_changes_real_rendered_pixels(self):
        base = json.loads(pipeline.TEMPLATE.read_text(encoding='utf-8'))
        checksums = set()
        for style_id, style in pipeline.STYLE_MAP.items():
            config = json.loads(json.dumps(base))
            config['colors'] = style['colors']
            config['layout'].update(style['layout_overrides'])
            config['landscape_layout'] = style['landscape_layout']
            image = pipeline.renderer.render_landscape(config, config['screens'][0], (1280, 960), 'ipad_landscape')
            checksums.add(__import__('hashlib').sha256(image.tobytes()).hexdigest())
        self.assertGreater(len(checksums), 10)

    def test_selected_store_targets_are_preserved_in_config(self):
        config = pipeline.build_config(
            RUN_ID, 'Example', [Path('capture.png'), Path('chinese.png')], self.proposal(),
            targets=('iphone_landscape', 'ipad_portrait'),
        )
        self.assertEqual(config['targets'], ['iphone_landscape', 'ipad_portrait'])

    def test_shared_generation_pipeline_both_languages(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            template = root / 'demo/nimotecode'
            template.mkdir(parents=True)
            config = json.loads(pipeline.TEMPLATE.read_text(encoding='utf-8'))
            config['sizes'] = [[1179, 2556]]
            (template / 'config.json').write_text(json.dumps(config), encoding='utf-8')
            assets = root / 'store_screenshots/assets'
            assets.parent.mkdir(parents=True)
            shutil.copytree(pipeline.ROOT / 'store_screenshots/assets', assets)
            small_targets = {name: {"layout": item["layout"], "sizes": [[320, 640] if item["layout"] == 'portrait' else [640, 320]]}
                             for name, item in json.loads((pipeline.ROOT / 'store_screenshots/targets.json').read_text()).items()}
            (root / 'store_screenshots/targets.json').write_text(json.dumps(small_targets), encoding='utf-8')
            incoming = root / 'incoming'
            incoming.mkdir()
            Image.new('RGB', (320, 640), '#143045').save(incoming / 'capture.png')
            Image.new('RGB', (320, 640), '#184254').save(incoming / 'chinese.png')
            renderer = pipeline.renderer
            old = (pipeline.ROOT, pipeline.RUNS, pipeline.TEMPLATE, renderer.ROOT, renderer.TARGETS)
            try:
                pipeline.ROOT = root
                pipeline.RUNS = root / 'store_screenshots/runs'
                pipeline.TEMPLATE = template / 'config.json'
                renderer.ROOT, renderer.TARGETS = root, root / 'store_screenshots/targets.json'
                result = pipeline.generate(incoming, 'Example', 'A real code editor.', style='soft_gradient',
                                           proposal=self.proposal(), run_id=RUN_ID)
                with self.assertRaises(FileExistsError):
                    pipeline.generate(incoming, 'Example', 'A real code editor.', proposal=self.proposal(), run_id=RUN_ID)
            finally:
                pipeline.ROOT, pipeline.RUNS, pipeline.TEMPLATE, renderer.ROOT, renderer.TARGETS = old
            run = root / 'store_screenshots/runs' / RUN_ID
            self.assertEqual(result['style'], 'soft_gradient')
            self.assertTrue((run / f'nimoteshot_{RUN_ID}.zip').is_file())
            generated = json.loads((run / 'config.json').read_text(encoding='utf-8'))
            self.assertEqual(generated['localizations']['zh-CN']['screens']['01_feature.png']['file'], 'chinese.png')
            for language in ('en-US', 'zh-CN'):
                self.assertTrue((run / 'exports' / language / 'android_landscape_640x320/01_feature.png').is_file())


if __name__ == '__main__':
    unittest.main()
