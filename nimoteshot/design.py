"""Versioned, closed design vocabulary shared by planning and rendering."""
import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

SCHEMA = json.loads(Path(__file__).with_name("design.schema.json").read_text(encoding="utf-8"))

VERSION = 1
TEMPLATES = json.loads(Path(__file__).with_name("templates.json").read_text(encoding="utf-8"))
PAGE_TYPES = ('editor', 'terminal', 'git', 'agent', 'files', 'settings', 'other', 'unknown')


def validate_design(proposal):
    """Validate optional v1 metadata; old proposals remain supported."""
    result = copy.deepcopy(proposal)
    # Repair only finite design tokens; never drop unknown instructions or fabricate evidence.
    if isinstance(result, dict) and isinstance(result.get('screens'), list):
        for screen in result['screens']:
            if not isinstance(screen, dict):
                continue
            analysis = screen.get('analysis')
            if isinstance(analysis, dict):
                for field in ('evidence', 'uncertainty', 'theme'):
                    value = analysis.get(field)
                    if isinstance(value, list) and all(isinstance(line, str) for line in value):
                        analysis[field] = '\n'.join(value)
            design = screen.setdefault('design', {})
            if not isinstance(design, dict):
                continue
            template = design.get('template', 'balanced')
            if isinstance(template, str):
                design['template'] = template if template in TEMPLATES else 'balanced'
            if type(design.get('background', 0)) is int and not 0 <= design.get('background', 0) <= 3:
                design['background'] = 0
            if design.get('template') == 'duo' and not design.get('secondary_file'):
                design['template'] = 'balanced'
            if design.get('template') == 'detail' and not design.get('focus_region'):
                design['template'] = 'balanced'
    try:
        Draft202012Validator(SCHEMA).validate(result)
    except ValidationError as error:
        raise ValueError(f'Invalid design at {list(error.absolute_path)}: {error.message}') from error
    result['schema_version'] = VERSION
    return result


def recommend_layouts(proposal):
    """Re-plan from reusable visual evidence; no image or model call needed."""
    result = validate_design(proposal)
    for screen in result['screens']:
        page = screen.get('analysis', {}).get('page_type', 'unknown')
        screen['design']['template'] = {'editor': 'compact', 'terminal': 'showcase',
                                        'git': 'balanced', 'files': 'balanced',
                                        'agent': 'showcase', 'settings': 'compact'}.get(page, 'balanced')
    return result
