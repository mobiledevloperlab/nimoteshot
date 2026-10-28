"""Explicitly regenerate pixel baselines after reviewing intended design changes."""
import sys
import json
import hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from test_visual_regression import visual_cases, ROOT
from nimoteshot.design import TEMPLATES
from scripts import generate_store_screenshots as renderer

if __name__ == '__main__':
    entries={}
    config=renderer.load('demo/nimotecode/config.json')
    for template in TEMPLATES:
        screen=config['screens'][0];screen['template']=template
        image=renderer.render(config,screen,(330,717))
        entries[template]={'size':list(image.size),'sha256':hashlib.sha256(image.tobytes()).hexdigest()}
    for name,image in visual_cases():
        entries[name]={'size':list(image.size),'sha256':hashlib.sha256(image.tobytes()).hexdigest()}
    (ROOT/'tests/visual-baselines.json').write_text(json.dumps(entries,indent=2)+'\n', encoding='utf-8')
    print(f'Updated {len(entries)} pixel baselines; review rendered previews before accepting changes.')
