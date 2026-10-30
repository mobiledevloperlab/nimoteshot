"""Output selection, closed schema, copy revision and ZIP share one locale registry."""
import copy
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from nimoteshot import pipeline, planner
from nimoteshot.design import validate_design
from nimoteshot.export_service import export


class OutputLocaleTests(unittest.TestCase):
    def setUp(self):
        self.source = pipeline.ROOT / 'demo/nimotecode/originals/code-editor.png'
        screen = {'file': self.source.name, 'design': {'template': 'balanced', 'background': 0},
                  'analysis': {'page_type': 'editor', 'evidence': 'Visible code editor'}}
        for options in pipeline.OUTPUT_LOCALES.values():
            screen['title_' + options['code']] = [options['placeholder_title']]
            screen['subtitle_' + options['code']] = options['placeholder_subtitle']
        self.proposal = {'screens': [screen]}

    def test_registry_fields_pass_closed_schema_and_unknown_fields_still_fail(self):
        self.assertEqual(len(pipeline.OUTPUT_LOCALES), 17)
        validate_design(self.proposal)
        for key in ('title_unsupported', 'title_fr_extra', 'css'):
            invalid = copy.deepcopy(self.proposal)
            invalid['screens'][0][key] = 'untrusted'
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_design(invalid)

    def test_prompt_and_config_include_each_selected_copy_version(self):
        prompt = pipeline.prompt_for([self.source], 'App', 'Visible tools', '', locales=tuple(pipeline.LOCALES))
        config = pipeline.build_config('20000101-000000-abcdef', 'App', [self.source], self.proposal,
                                       locales=tuple(pipeline.LOCALES), targets=('iphone_portrait',))
        for locale, options in pipeline.LOCALES.items():
            with self.subTest(locale=locale):
                self.assertIn('title_' + options['code'], prompt)
                localized = pipeline.renderer.localized(config, locale)
                self.assertEqual(localized['screens'][0]['title'], [options['placeholder_title']])
                self.assertEqual(localized['screens'][0]['subtitle'], options['placeholder_subtitle'])

    def test_copy_regeneration_preserves_all_selected_language_versions(self):
        revised = copy.deepcopy(self.proposal)
        for options in pipeline.OUTPUT_LOCALES.values():
            revised['screens'][0]['title_' + options['code']] = ['Updated']
        with patch.object(planner, 'analyze', return_value=revised) as analyze:
            result = planner.revise(self.proposal, 'copy', 'App', 'Visible tools',
                                    [options['code'] for options in pipeline.LOCALES.values()], 'deepseek')
        self.assertEqual(analyze.call_args.args[0], [])
        for options in pipeline.OUTPUT_LOCALES.values():
            self.assertEqual(result['screens'][0]['title_' + options['code']], ['Updated'])
        self.assertEqual(result['screens'][0]['design'], self.proposal['screens'][0]['design'])

    def test_available_output_locales_export_real_portrait_landscape_pngs_and_valid_zip(self):
        available = {locale: options for locale, options in pipeline.OUTPUT_LOCALES.items()
                     if not options['requires_shaping'] or pipeline.renderer.features.check('raqm')}
        config = pipeline.build_config('20000101-000000-abcdef', '代码 Studio', [self.source], self.proposal,
                                       locales=tuple(locale for locale in available if locale!='en-US'), targets=('iphone_portrait', 'iphone_landscape'))
        config['source_dir'] = str(self.source.parent)
        presets = {'iphone_portrait': {'layout': 'portrait', 'sizes': [[320, 640]]},
                   'iphone_landscape': {'layout': 'landscape', 'sizes': [[640, 320]]}}
        with tempfile.TemporaryDirectory() as folder, patch.object(pipeline.renderer, 'targets', return_value=presets):
            directory = Path(folder)
            config['output_dir'] = str(directory / 'exports')
            config['preview_dir'] = str(directory / 'previews')
            archive = export(config, directory, pipeline.renderer, lambda message: None)
            with zipfile.ZipFile(archive) as package:
                self.assertIsNone(package.testzip())
                pngs = [name for name in package.namelist() if name.endswith('.png')]
                self.assertEqual(len(pngs), 2*len(available))
                languages = {name.split('/')[1] for name in pngs}
                self.assertEqual(languages, set(available))
            self.assertEqual(len(list((directory / 'previews').rglob('*.png'))), 2*len(available))

    def test_missing_shaping_rejects_complex_export_without_creating_a_zip(self):
        config = pipeline.build_config('20000101-000000-abcdef', 'App', [self.source], self.proposal,
                                       locales=('ar-SA',), targets=('iphone_portrait',))
        config['source_dir'] = str(self.source.parent)
        presets = {'iphone_portrait': {'layout': 'portrait', 'sizes': [[320, 640]]}}
        with tempfile.TemporaryDirectory() as folder, patch.object(pipeline.renderer, 'targets', return_value=presets), \
                patch.object(pipeline.renderer.features, 'check', return_value=False):
            directory = Path(folder)
            config['output_dir'] = str(directory / 'exports')
            config['preview_dir'] = str(directory / 'previews')
            with self.assertRaisesRegex(ValueError, 'libraqm shaping'):
                export(config, directory, pipeline.renderer, lambda message: None)
            self.assertEqual(list(directory.glob('*.zip')), [])
