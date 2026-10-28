import importlib.util
import io
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('generator', ROOT / 'scripts/generate_store_screenshots.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = generator.load(config_path='demo/nimotecode/config.json')

    def test_each_language_and_layout_renders_real_pixels(self):
        self.assertEqual(generator.locales(self.base), ['en-US', 'zh-CN'])
        for language in generator.locales(self.base):
            config = generator.localized(self.base, language)
            for target, preset in generator.targets(config).items():
                size = tuple(preset['sizes'][0])
                screen = config['screens'][0]
                render = generator.render if preset['layout'] == 'portrait' else generator.render_landscape
                image = render(config, screen, size, target)
                self.assertEqual(image.size, size)
                self.assertEqual(image.mode, 'RGB')
                buffer = io.BytesIO()
                image.save(buffer, format='PNG', icc_profile=(ROOT / 'store_screenshots/assets/sRGB.icc').read_bytes())
                buffer.seek(0)
                with Image.open(buffer) as stored:
                    self.assertEqual(stored.size, size)
                    self.assertTrue(stored.info.get('icc_profile'))

    def test_language_and_device_source_overrides(self):
        config = generator.localized(self.base, 'zh-CN')
        screen = config['screens'][0].copy()
        screen['target_files'] = {'ipad_landscape': config['screens'][1]['file']}
        self.assertEqual(generator.source_for(screen, 'ipad_landscape'), config['screens'][1]['file'])
        self.assertEqual(generator.source_for(screen, 'iphone_portrait'), screen['file'])
        self.assertNotEqual(generator.output_path(config, 'ipad_landscape', (2752, 2064), screen),
                            generator.output_path(self.base, 'ipad_landscape', (2752, 2064), screen))

if __name__ == '__main__':
    unittest.main()
