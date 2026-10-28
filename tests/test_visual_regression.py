"""Representative golden renders use only the two approved captures."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

from PIL import Image, ImageChops

from nimoteshot import pipeline

ROOT = Path(__file__).resolve().parents[1]


def visual_cases():
    base=pipeline.renderer.load('demo/nimotecode/config.json')
    for primary,secondary,style,title,subtitle in (
        ('code-editor.png','terminal.png','editorial',['Code navigation'],'Find definitions and references'),
        ('terminal.png','code-editor.png','midnight',['Terminal tools'],'Review shell output')):
        for template in ('showcase','detail','duo'):
            for target,size in (('iphone_portrait',(264,574)),('ipad_landscape',(420,315))):
                config=copy.deepcopy(base)
                config['colors']=copy.deepcopy(pipeline.STYLE_MAP[style]['colors'])
                config['layout'].update(pipeline.STYLE_MAP[style]['layout_overrides'])
                config['landscape_layout']=copy.deepcopy(pipeline.STYLE_MAP[style]['landscape_layout'])
                screen={'file':primary,'output':'01_feature.png','title':title,'subtitle':subtitle,'background':0,'kind':'feature',
                        'template':template,'design':{'template':template,'focus_region':'top','secondary_file':secondary}}
                config['screens']=[screen]
                render=pipeline.renderer.render if target=='iphone_portrait' else pipeline.renderer.render_landscape
                yield f'{Path(primary).stem}-{template}-{target}.png',render(config,screen,size,target)


class VisualRegressionTests(unittest.TestCase):
    def test_representative_light_dark_portrait_and_tablet_layouts(self):
        baseline=json.loads((ROOT/'tests/visual-baselines.json').read_text())
        for name,actual in visual_cases():
            with self.subTest(name=name):
                self.assertEqual(list(actual.size),baseline[name]['size'])
                self.assertEqual(hashlib.sha256(actual.tobytes()).hexdigest(),baseline[name]['sha256'])
