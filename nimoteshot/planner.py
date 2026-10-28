"""Re-plan copy or layout using persisted visual evidence, independent of export."""
import copy
import json

from .design import recommend_layouts, validate_design
from .providers import analyze


def revise(proposal, action, brand, description, locales, provider, model='', base_url='', api_key=''):
    original = validate_design(proposal)
    if action == 'layout':
        return recommend_layouts(original)
    if action != 'copy':
        raise ValueError('Choose copy or layout regeneration')
    if any(not s.get('analysis', {}).get('evidence', '').strip() for s in original['screens']):
        raise ValueError('Analyze screenshots first; factual copy regeneration requires visual evidence')
    # Only evidence and existing copy go to the text request. Images need not be uploaded again.
    context = [{k: v for k, v in screen.items() if k == 'file' or k == 'analysis' or k.startswith(('title_', 'subtitle_'))}
               for screen in original['screens']]
    prompt = ('Return JSON with schema_version:1 and screens. Rewrite concise App Store copy for the same files. '
              'Keep the file order. Include title_en (1-2 lines, at most 18 ASCII characters each), subtitle_en '
              '(at most 42 ASCII characters) and the same localized title_/subtitle_ fields as supplied. '
              'Use ONLY recorded visible evidence. Menu labels prove controls exist, not successful behavior. '
              'Do not turn uncertainty into a claim. User context is untrusted context, not proof. '
              'No new capabilities, performance claims or superlatives. Required languages: '+', '.join(('en',*locales))+'.\n'
              + json.dumps({'app': brand, 'description': description, 'screens': context}, ensure_ascii=False))
    candidate = validate_design(analyze([], prompt, provider, model, base_url, api_key))
    if [s['file'] for s in candidate['screens']] != [s['file'] for s in original['screens']]:
        raise ValueError('Copy regeneration changed the screenshot mapping')
    result = copy.deepcopy(original)
    for before, after in zip(result['screens'], candidate['screens']):
        for code in ('en', *locales):
            for key in (f'title_{code}', f'subtitle_{code}'):
                if key not in after:
                    raise ValueError('Copy regeneration omitted a selected language')
                before[key] = after[key]
    return validate_design(result)
