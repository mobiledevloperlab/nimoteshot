import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from nimoteshot.design import validate_design, TEMPLATES
from nimoteshot import providers
from scripts import generate_store_screenshots as renderer

ROOT = Path(__file__).resolve().parents[1]


class DesignTests(unittest.TestCase):
    def test_schema_rejects_instructions_and_future_versions(self):
        for proposal in ({'schema_version': 2}, {'screens': [{'design': {'css': 'bad'}}]},
                         {'screens': [{'analysis': {'priority': True}}]}):
            with self.assertRaises(ValueError):
                validate_design(proposal)

    def test_invalid_template_falls_back_without_mutation(self):
        proposal = {'screens': [{'file': 'a.png', 'title_en': ['Feature'], 'subtitle_en': 'Visible', 'design': {'template': 'javascript'}}]}
        self.assertEqual(validate_design(proposal)['screens'][0]['design']['template'], 'balanced')
        self.assertEqual(proposal['screens'][0]['design']['template'], 'javascript')

    def test_real_images_are_sent_together(self):
        files = [ROOT / 'demo/nimotecode/originals' / name for name in ('code-editor.png', 'terminal.png')]
        with patch.object(providers, '_openai_request', return_value='{"screens": []}') as request:
            providers.analyze(files, 'Return JSON', 'deepseek', api_key='test')
        content = request.call_args.args[3]
        images = [part for part in content if part['type'] == 'image_url']
        self.assertEqual(len(images), 2)
        self.assertTrue(all(part['image_url']['url'].startswith('data:image/jpeg;base64,') for part in images))

    def test_invalid_json_is_reported(self):
        with patch.object(providers, '_openai_request', return_value='invalid'):
            with self.assertRaisesRegex(ValueError, 'valid JSON'):
                providers.analyze([], 'JSON', 'deepseek', api_key='test')

    def test_templates_render_all_portrait_ratios(self):
        config = renderer.load('demo/nimotecode/config.json')
        for template in TEMPLATES:
            for size in ((330, 717), (384, 512), (270, 480)):
                screen = copy.deepcopy(config['screens'][0])
                screen['template'] = template
                config['screens'][0] = screen
                image = renderer.render(config, screen, size)
                self.assertEqual(image.size, size)
                self.assertEqual(image.mode, 'RGB')

    def test_visual_baselines(self):
        import hashlib
        baseline=json.loads((ROOT/'tests/visual-baselines.json').read_text())
        config=renderer.load('demo/nimotecode/config.json')
        for template in TEMPLATES:
            screen=config['screens'][0];screen['template']=template
            actual=renderer.render(config,screen,(330,717))
            self.assertEqual(hashlib.sha256(actual.tobytes()).hexdigest(),baseline[template]['sha256'])
