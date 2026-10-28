import json
import unittest
from pathlib import Path


class EditorI18nTests(unittest.TestCase):
    def test_all_new_labels_have_five_translations(self):
        script=(Path(__file__).resolve().parents[1]/'web/editor-i18n.js').read_text(encoding='utf-8')
        dictionaries=json.loads(script.split('const editorMessages = ',1)[1].removesuffix(';\n'))
        self.assertEqual(set(dictionaries),{'en','zh','ja','ko','es'})
        keys=set(dictionaries['en'])
        for language,labels in dictionaries.items():
            with self.subTest(language=language):
                self.assertEqual(set(labels),keys)
                self.assertTrue(all(isinstance(value,str) and value.strip() for value in labels.values()))
                for key in ('regenerateCopy','recommendLayouts','reanalyze','exportDesign','manualMode'):
                    self.assertTrue(labels[key])
