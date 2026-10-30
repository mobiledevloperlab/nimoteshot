#!/usr/bin/env python3
"""Render store artwork from archived, verified application screenshots."""
import argparse
import json
import hashlib
import copy
import unicodedata
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor, ImageOps, features
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_REGISTRY = json.loads((ROOT / 'nimoteshot/templates.json').read_text(encoding='utf-8'))
APPLE_SIZES = {tuple(size) for size in json.loads((ROOT / 'store_screenshots/targets.json').read_text(encoding='utf-8'))['iphone_portrait']['sizes']}
TARGETS = ROOT / 'store_screenshots/targets.json'

def targets(c):
    presets=json.loads(TARGETS.read_text(encoding='utf-8'))
    # Older archives keep their exact iPhone size list as the source of truth.
    presets['iphone_portrait']['sizes']=c['sizes']
    for name, target in presets.items():
        sizes=[tuple(size) for size in target['sizes']]
        assert sizes and len(sizes)==len(set(sizes)), f'Invalid sizes for {name}'
        for w,h in sizes:
            assert isinstance(w,int) and isinstance(h,int) and w>0 and h>0
            assert (w<h)==(target['layout']=='portrait'), f'Wrong orientation: {name} {w}x{h}'
            if name.startswith('android_'):
                assert 320<=min(w,h) and max(w,h)<=3840 and max(w,h)<=2*min(w,h), f'Google Play size limit: {w}x{h}'
    selected=c.get('targets')
    if selected is not None:
        assert isinstance(selected,list) and selected and set(selected).issubset(presets), 'Invalid selected targets'
        presets={name: presets[name] for name in selected}
    return presets

def load(config_path):
    config = ROOT/config_path
    assert config.is_file(), f'Missing config: {config}'
    c=json.loads(config.read_text(encoding='utf-8'))
    assert 1 <= len(c['screens']) <= 10 and len({s['output'] for s in c['screens']}) == len(c['screens'])
    assert {tuple(x) for x in c['sizes']} <= APPLE_SIZES
    for key in ('regular','bold'):
        assert (ROOT/c['fonts'][key]).is_file(), f'Missing font: {c["fonts"][key]}'
    manifest_path = config.parent / 'source_manifest.json'
    assert manifest_path.is_file(), f'Missing source manifest: {manifest_path}'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    used={s['file'] for s in c['screens'] if s.get('file')} | {p['file'] for s in c['screens'] for p in s.get('components',[])}
    used|={name for s in c['screens'] for name in s.get('target_files',{}).values()}
    used|={s['design']['secondary_file'] for s in c['screens'] if s.get('design',{}).get('secondary_file')}
    for translation in c.get('localizations',{}).values():
        for override in translation.get('screens',{}).values():
            if override.get('file'): used.add(override['file'])
            used.update(override.get('target_files',{}).values())
    assert used <= set(manifest), 'Screenshot mapping contains an unarchived source'
    for name, expected in manifest.items():
        p=ROOT/c['source_dir']/name
        assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==expected, f'Archived source changed: {p}'
    for name in used:
        p=ROOT/c['source_dir']/name
        assert p.is_file(), f'Missing screenshot: {p}'
        with Image.open(p) as im: im.verify()
    return c

def locales(c):
    return [c.get('locale','en-US'),*c.get('localizations',{})]

def localized(c,locale):
    base=c.get('locale','en-US')
    if locale==base: return c
    assert locale in c.get('localizations',{}), f'Unknown locale: {locale}'
    result=copy.deepcopy(c); override=c['localizations'][locale]
    result['locale']=locale
    result['brand']=override.get('brand',c.get('brand','NIMOTECODE'))
    result['fonts']=override.get('fonts',c['fonts'])
    by_output={s['output']:s for s in result['screens']}
    assert set(override['screens'])==set(by_output), f'Incomplete translations for {locale}'
    for output, fields in override['screens'].items():
        for key in ('target_files','target_crops'):
            if key in fields:
                by_output[output][key]={**by_output[output].get(key,{}),**fields[key]}
        fields={key:value for key,value in fields.items() if key not in ('target_files','target_crops')}
        by_output[output].update(fields)
        assert by_output[output].get('title') and by_output[output].get('subtitle')
    for path in result['fonts'].values():assert (ROOT/path).is_file(),f'Missing font: {path}'
    return result

@lru_cache(maxsize=32)
def font_characters(path):
    with TTFont(path, lazy=True) as face:
        return frozenset(face.getBestCmap() or {})


def needs_complex_layout(text):
    return any(unicodedata.bidirectional(char) in ('R','AL')
               or any(script in unicodedata.name(char,'') for script in ('DEVANAGARI','BENGALI','THAI'))
               for char in text)


def validate_text_layout(text):
    if needs_complex_layout(text) and not features.check('raqm'):
        raise ValueError('Complex text requires Pillow with libraqm shaping support')


def text_font_path(preferred, text, weight='Regular'):
    # Language selectors choose copy variants, not which scripts a user may type.
    characters={ord(char) for char in text if not char.isspace()
                and unicodedata.category(char) != 'Cf'
                and not 0xFE00 <= ord(char) <= 0xFE0F}
    directory=ROOT/'store_screenshots/assets/fonts'
    candidates=[Path(preferred), directory/f'NotoSansCJKsc-{weight}.otf', directory/'Inter.ttf',
                *(directory/f'NotoSans{script}.ttf' for script in ('Arabic','Devanagari','Thai','Hebrew','Bengali'))]
    for path in dict.fromkeys(candidates):
        if path.is_file() and characters <= font_characters(str(path)):
            return path
    raise ValueError('No bundled font covers text characters: '+', '.join(f'U+{code:04X}' for code in sorted(characters)))


def load_font(path, size, weight):
    face=ImageFont.truetype(path,size)
    try:face.set_variation_by_name(weight)
    except OSError:pass
    return face


def fit_text(draw, lines, font_path, max_width, initial, minimum, weight='Bold'):
    validate_text_layout(''.join(lines))
    font_path=text_font_path(font_path,''.join(lines),weight)
    for size in range(initial,minimum-1,-1):
        f=load_font(font_path,size,weight)
        if all(draw.textbbox((0,0),line,font=f)[2]<=max_width for line in lines): return f
    raise ValueError(f'Text does not fit: {lines}')


def font(c,key,size,text=''):
    validate_text_layout(text)
    weight='Bold' if key=='bold' else 'Regular'
    path=text_font_path(ROOT/c['fonts'][key],text,weight)
    return load_font(path,size,weight)

def px(v,w): return round(v*w)

def background(c,s,size):
    colors=c['colors']; index=s['background']; start=colors['backgrounds'][index]
    ends=colors.get('gradient_ends')
    if not ends:return Image.new('RGB',size,start)
    a=ImageColor.getrgb(start); b=ImageColor.getrgb(ends[index % len(ends)])
    strip=Image.new('RGB',(1,size[1])); pixels=strip.load()
    for y in range(size[1]):
        t=y/max(1,size[1]-1)
        pixels[0,y]=tuple(round(a[i]*(1-t)+b[i]*t) for i in range(3))
    return strip.resize(size)

def card(canvas,source,box,radius,shadow=True):
    x,y,iw,ih=box; w,h=canvas.size
    im=source.resize((iw,ih),Image.Resampling.LANCZOS)
    mask=Image.new('L',(iw,ih),0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,iw-1,ih-1),radius=radius,fill=255)
    if shadow:
        sm=Image.new('L',(w,h),0);sm.paste(mask,(x,y+round(w*.015)))
        sm=sm.filter(ImageFilter.GaussianBlur(round(w*.025)))
        layer=Image.new('RGBA',(w,h),(18,21,27,0)); layer.putalpha(sm.point(lambda v: round(v*.25)))
        canvas=Image.alpha_composite(canvas.convert('RGBA'),layer)
    canvas.paste(im,(x,y),mask)
    ImageDraw.Draw(canvas).rounded_rectangle((x,y,x+iw-1,y+ih-1),radius=radius,outline='#3F444B',width=max(1,round(w*.0015)))
    return canvas

def contained_card(canvas, source, box, radius, alignment='center', anchor='center'):
    x,y,width,height=map(round,box)
    if width<1 or height<1: raise ValueError('No space remains for the screenshot')
    image=ImageOps.contain(source,(width,height),Image.Resampling.LANCZOS)
    ix=x if alignment=='left' else x+width-image.width if alignment=='right' else x+(width-image.width)//2
    iy=y if anchor=='top' else y+height-image.height if anchor=='bottom' else y+(height-image.height)//2
    if ix<0 or iy<0 or ix+image.width>canvas.width or iy+image.height>canvas.height:
        raise ValueError('Screenshot exceeds canvas safe area')
    return card(canvas,image,(ix,iy,image.width,image.height),radius)


def render_composition(canvas,c,s,source,box,target):
    """Show an unchanged full capture alongside another capture or a real crop."""
    x,y,width,height=box; gap=round(canvas.width*.035); design=s.get('design',{})
    if s.get('template')=='duo':
        filename=design.get('secondary_file')
        if not filename: return contained_card(canvas,source,box,round(canvas.width*.02)).convert('RGB')
        with Image.open(ROOT/c['source_dir']/filename) as raw: second=raw.convert('RGB')
    else:
        region=design.get('focus_region','center')
        start={'top':.08,'center':.30,'bottom':.55}[region]
        second=source.crop((0,round(source.height*start),source.width,round(source.height*min(1,start+.35))))
    # Store-style staged composition: one dominant full capture, a subordinate
    # second capture/detail, deliberate overlap, and top alignment below copy.
    # Both remain within the safe stage; only the rear capture can be occluded.
    tokens=TEMPLATE_REGISTRY[s['template']]['composition']
    def stage_box(name):
        bx,by,bw,bh=tokens[name]
        return (x+width*bx,y+height*by,width*bw,height*bh)
    primary=stage_box('primary'); secondary=stage_box('secondary')
    radius=max(3,round(canvas.width*.026))
    if s.get('template')=='duo':
        canvas=contained_card(canvas,second,secondary,radius,alignment='right',anchor='top')
        canvas=contained_card(canvas,source,primary,radius,alignment='left',anchor='top')
    else:
        canvas=contained_card(canvas,source,primary,radius,alignment='left',anchor='top')
        canvas=contained_card(canvas,second,secondary,max(3,round(canvas.width*.018)),alignment='right',anchor='top')
    return canvas.convert('RGB')


def source_for(s,target):
    fallback=s.get('file') or s['components'][0]['file']
    return s.get('target_files',{}).get(target,fallback)

def crop_for(s,target):
    fallback=s.get('crop') or (s.get('components') or [{}])[0].get('crop')
    return s.get('target_crops',{}).get(target,fallback)

def render(c,s,size,target='iphone_portrait'):
    w,h=size; k=w/1320; L=dict(c['layout']); C=c['colors']
    L.update(TEMPLATE_REGISTRY.get(s.get('template'), {}).get('portrait', {}))
    if s.get('design',{}).get('typography') == 'compact':
        L['title_size'] *= .86
    canvas=background(c,s,size); d=ImageDraw.Draw(canvas)
    margin=px(L['side_margin'],w); by=round(h*L['brand_y'])
    mark=round(31*k)
    d.rounded_rectangle((margin,by,margin+mark,by+mark),radius=round(8*k),fill=C['accent'])
    brand=c.get('brand','NIMOTECODE')
    bf=fit_text(d,[brand],ROOT/c['fonts']['bold'],round(w*.53),max(12,round(28*k)),max(10,round(13*k)))
    d.text((margin+round(46*k),by-round(3*k)),brand,font=bf,fill=C['ink'])
    number=f"{c['screens'].index(s)+1:02d} / {len(c['screens']):02d}"; nf=font(c,'regular',round(27*k))
    bb=d.textbbox((0,0),number,font=nf); d.text((w-margin-(bb[2]-bb[0]),by),number,font=nf,fill=C['muted'])
    ty=round(h*L['title_y'])
    tf=fit_text(d,s['title'],ROOT/c['fonts']['bold'],w-2*margin,round(L['title_size']*k),max(12,round(L['title_size']*k*(.55 if c.get('design_schema_version') else .25))))
    for line in s['title']:
        bb=d.textbbox((0,0),line,font=tf)
        assert bb[2]-bb[0]<=w-2*margin,f'Title overflow: {line}'
        d.text((margin,ty),line,font=tf,fill=C['ink'])
        ty+=round(L['title_line_height']*k*tf.size/max(1,round(L['title_size']*k)))
    subfont=fit_text(d,[s['subtitle']],ROOT/c['fonts']['regular'],w-2*margin,round(L['subtitle_size']*k),max(10,round(L['subtitle_size']*k*(.55 if c.get('design_schema_version') else .18))),'Regular'); suby=ty+round(11*k)
    bb=d.textbbox((0,0),s['subtitle'],font=subfont)
    assert bb[2]-bb[0]<=w-2*margin,f'Subtitle overflow: {s["output"]}'
    d.text((margin,suby),s['subtitle'],font=subfont,fill=C['muted'])
    if s.get('kind')=='overview':
        return render_overview(c,s,size)
    with Image.open(ROOT/c['source_dir']/source_for(s,target)) as source:
        if crop_for(s,target):
            a,b,e,f=crop_for(s,target); sw,sh=source.size
            source=source.crop((round(a*sw),round(b*sh),round(e*sw),round(f*sh)))
        source=source.convert('RGB')
        if s.get('template') in ('detail', 'duo'):
            top = max(round(h*L['image_y']), d.textbbox((margin,suby),s['subtitle'],font=subfont)[3]+round(w*.04))
            return render_composition(canvas, c, s, source, (margin, top, w-2*margin, h-top-round(w*.04)), target)
        scale = {'small': .88, 'standard': 1, 'large': 1.08}.get(s.get('design',{}).get('scale'), 1)
        iw=min(w-2*margin,px(L['image_width']*scale,w))
        ih=round(iw*source.height/source.width)
        subtitle_bottom=d.textbbox((margin,suby),s['subtitle'],font=subfont)[3]
        iy=max(round(h*L['image_y']),subtitle_bottom+round(45*k))
        if iy+ih>h-round(40*k):
            iw=round(iw*(h-round(40*k)-iy)/ih);ih=round(iw*source.height/source.width)
        alignment=s.get('design',{}).get('alignment','center')
        ix=margin if alignment=='left' else w-margin-iw if alignment=='right' else (w-iw)//2
        assert ix>=margin-2 and iy>subtitle_bottom and iy+ih<=h
        canvas=card(canvas,source,(ix,iy,iw,ih),round(w*L['radius']))
    if s.get('secondary'):
        with Image.open(ROOT/c['source_dir']/s['secondary']) as second:
            x1,y1,x2,y2=s['secondary_crop']; sw,sh=second.size
            crop=second.crop((round(x1*sw),round(y1*sh),round(x2*sw),round(y2*sh)))
            cw=round(w*.43);ch=round(cw*crop.height/crop.width)
            cx=margin;cy=round(h*.585)
            assert cy+ch<h-round(90*k)
            canvas=card(canvas,crop,(cx,cy,cw,ch),round(w*.018))
    return canvas.convert('RGB')

def render_landscape(c,s,size,target='android_landscape'):
    """Editorial landscape layout: copy at left, real application UI at right."""
    w,h=size; C=c['colors']; margin=round(w*.052); style=dict(c.get('landscape_layout',{}))
    style.update(TEMPLATE_REGISTRY.get(s.get('template'), {}).get('landscape', {}))
    if s.get('design',{}).get('typography')=='compact':
        style['title_scale']=style.get('title_scale',.087)*.86
    canvas=background(c,s,size); d=ImageDraw.Draw(canvas)
    scale=h/2048
    brand_y=round(h*.09); mark=round(38*scale)
    d.rounded_rectangle((margin,brand_y,margin+mark,brand_y+mark),radius=max(2,round(9*scale)),fill=C['accent'])
    brand=c.get('brand','NIMOTECODE')
    bf=fit_text(d,[brand],ROOT/c['fonts']['bold'],round(w*.45),max(12,round(35*scale)),max(10,round(15*scale)))
    d.text((margin+round(56*scale),brand_y-round(4*scale)),brand,font=bf,fill=C['ink'])
    number=f"{c['screens'].index(s)+1:02d} / {len(c['screens']):02d}"
    nf=font(c,'regular',max(12,round(30*scale)))
    nb=d.textbbox((0,0),number,font=nf)
    d.text((w-margin-(nb[2]-nb[0]),brand_y),number,font=nf,fill=C['muted'])
    left_width=round(w*style.get('left_width',.36))
    title=s['title']
    tf=fit_text(d,title,ROOT/c['fonts']['bold'],left_width,round(h*style.get('title_scale',.087)),round(h*.04))
    line_height=round(tf.size*1.12)
    sub=s['subtitle']; sf=font(c,'regular',max(12,round(h*.038)),sub)
    while d.textbbox((0,0),sub,font=sf)[2]>left_width and sf.size>round(h*.02):
        sf=font(c,'regular',sf.size-1,sub)
    assert d.textbbox((0,0),sub,font=sf)[2]<=left_width, f'Subtitle overflow: {s["output"]}'
    text_height=len(title)*line_height+round(h*.045)+sf.size
    ty=max(round((h-text_height)*.48),brand_y+round(h*.10))
    if ty+text_height>h-round(h*.06):
        raise ValueError('Copy exceeds landscape safe area; shorten the title or subtitle')
    for line in title:
        d.text((margin,ty),line,font=tf,fill=C['ink']);ty+=line_height
    d.text((margin,ty+round(h*.045)),sub,font=sf,fill=C['muted'])
    # Keep the entire source UI visible. A portrait source becomes a large,
    # centered card within the right-hand panel, never a stretched landscape UI.
    with Image.open(ROOT/c['source_dir']/source_for(s,target)) as raw:
        if crop_for(s,target):
            a,b,e,f=crop_for(s,target); sw,sh=raw.size
            raw=raw.crop((round(a*sw),round(b*sh),round(e*sw),round(f*sh)))
        source=raw.convert('RGB')
        if s.get('template') in ('detail','duo'):
            return render_composition(canvas,c,s,source,(round(w*.46),round(h*.16),round(w*.488),round(h*.68)),target)
        scale={'small':.88,'standard':1,'large':1.08}.get(s.get('design',{}).get('scale'),1)
        max_w=round(w*style.get('image_width',.49)); max_h=round(h*.79*min(1,scale))
        factor=min(max_w/source.width,max_h/source.height)
        iw=max(1,round(source.width*factor)); ih=max(1,round(source.height*factor))
        panel_x=round(w*(.948-style.get('image_width',.49)))
        ix=round(panel_x+(max_w-iw)/2); iy=round((h-ih)/2)
        assert ix>=round(w*.43) and ix+iw<=w-margin and iy>=0 and iy+ih<=h
        canvas=card(canvas,source,(ix,iy,iw,ih),max(4,round(h*style.get('radius',.018))))
    return canvas.convert('RGB')

def render_overview(c,s,size):
    w,h=size;k=w/1320;L=c['layout'];C=c['colors'];margin=round(w*L['side_margin'])
    canvas=background(c,s,size);d=ImageDraw.Draw(canvas)
    by=round(h*L['brand_y']); mark=round(31*k)
    d.rounded_rectangle((margin,by,margin+mark,by+mark),radius=round(8*k),fill=C['accent'])
    brand=c.get('brand','NIMOTECODE')
    bf=fit_text(d,[brand],ROOT/c['fonts']['bold'],round(w*.53),max(12,round(28*k)),max(10,round(13*k)))
    d.text((margin+round(46*k),by-round(3*k)),brand,font=bf,fill=C['ink'])
    num=f"01 / {len(c['screens']):02d}";nf=font(c,'regular',round(27*k));bb=d.textbbox((0,0),num,font=nf)
    d.text((w-margin-(bb[2]-bb[0]),by),num,font=nf,fill=C['muted'])
    ty=round(h*L['title_y']);tf=font(c,'bold',round(L['title_size']*k),''.join(s['title']))
    for line in s['title']:
        bb=d.textbbox((0,0),line,font=tf);assert bb[2]-bb[0]<=w-2*margin
        d.text((margin,ty),line,font=tf,fill=C['ink']);ty+=round(L['title_line_height']*k)
    sf=font(c,'regular',round(L['subtitle_size']*k),s['subtitle']);suby=ty+round(11*k)
    assert d.textbbox((0,0),s['subtitle'],font=sf)[2]<w-2*margin
    d.text((margin,suby),s['subtitle'],font=sf,fill=C['muted'])
    roww=w-2*margin;rowh=round(h*.175);start=round(h*.302);gap=round(h*.044)
    for i,part in enumerate(s['components']):
        label_y=start+i*(rowh+gap)-round(65*k)
        d.text((margin,label_y),part['label'],font=font(c,'bold',round(46*k),part['label']),fill=C['muted'])
        with Image.open(ROOT/c['source_dir']/part['file']) as raw:
            a,b,e,f=part['crop'];sw,sh=raw.size
            crop=raw.crop((round(a*sw),round(b*sh),round(e*sw),round(f*sh))).convert('RGB')
            target_ratio=roww/rowh; actual=crop.width/crop.height
            if actual>target_ratio:
                neww=round(crop.height*target_ratio);left=(crop.width-neww)//2;crop=crop.crop((left,0,left+neww,crop.height))
            else:
                newh=round(crop.width/target_ratio);top=(crop.height-newh)//2;crop=crop.crop((0,top,crop.width,top+newh))
            canvas=card(canvas,crop,(margin,start+i*(rowh+gap),roww,rowh),round(w*L['radius']))
    assert start+2*(rowh+gap)+rowh<h-round(60*k)
    return canvas.convert('RGB')

def output_path(c,target,size,s):
    folder=f'iphone_{size[0]}x{size[1]}' if target=='iphone_portrait' else f'{target}_{size[0]}x{size[1]}'
    return ROOT/c['output_dir']/c['locale']/folder/s['output']

def save(c,target,size):
    for s in c['screens']:
        p=output_path(c,target,size,s);p.parent.mkdir(parents=True,exist_ok=True)
        im=render(c,s,size,target) if targets(c)[target]['layout']=='portrait' else render_landscape(c,s,size,target)
        profile=(ROOT/'store_screenshots/assets/sRGB.icc').read_bytes()
        im.save(p,format='PNG',icc_profile=profile,optimize=True)
    print(f'Generated {len(c["screens"])} {target} PNGs at {size[0]}x{size[1]}')

def preview(c,target):
    size=tuple(targets(c)[target]['sizes'][0]); thumbs=[]
    for s in c['screens']:
        p=output_path(c,target,size,s)
        if not p.exists(): save(c,target,size)
        with Image.open(p) as im:
            tw=264 if size[0]<size[1] else 420
            th=round(tw*size[1]/size[0]);thumbs.append(im.resize((tw,th),Image.Resampling.LANCZOS))
    tw,th=thumbs[0].size;columns=min(4,len(thumbs));rows=(len(thumbs)+columns-1)//columns
    sheet=Image.new('RGB',(16+columns*(tw+12),16+rows*(th+12)),'#E6E8EB')
    for i,im in enumerate(thumbs):sheet.paste(im,(16+(i%columns)*(tw+12),16+(i//columns)*(th+12)))
    name=f'overview_{len(c["screens"])}.png' if target=='iphone_portrait' else f'{target}_overview.png'
    p=ROOT/c['preview_dir']/c['locale']/name;p.parent.mkdir(parents=True,exist_ok=True);sheet.save(p)
    print(p)

def validate(c,selected):
    count=0
    for target in selected:
      for size in map(tuple,targets(c)[target]['sizes']):
        for s in c['screens']:
            p=output_path(c,target,size,s)
            assert p.is_file(),f'Missing {p}'
            with Image.open(p) as im:
                im.load()
                assert im.format=='PNG' and im.mode=='RGB' and im.size==size and 'A' not in im.getbands(),p
                assert im.info.get('icc_profile'),f'Missing sRGB profile: {p}'
            count+=1
    print(f'Validated {count} RGB/sRGB PNGs across {len(selected)} target groups.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--all',action='store_true');g.add_argument('--size');g.add_argument('--preview',action='store_true');g.add_argument('--validate',action='store_true')
    ap.add_argument('--config', required=True, help='Config JSON to render, for example demo/nimotecode/config.json')
    ap.add_argument('--target',choices=['iphone_portrait','android_portrait','android_landscape','ipad_landscape'],help='One target group (default: all groups)')
    ap.add_argument('--locale',help='One language (default: all configured languages)')
    a=ap.parse_args()
    base=load(a.config);selected=[a.target] if a.target else list(targets(base))
    languages=[a.locale] if a.locale else locales(base)
    configs=[localized(base,language) for language in languages]
    if a.all:
        for c in configs:
            for target in selected:
                for size in map(tuple,targets(c)[target]['sizes']):save(c,target,size)
                preview(c,target)
            validate(c,selected)
    elif a.size:
        size=tuple(map(int,a.size.lower().split('x')))
        matches=[t for t in selected if size in set(map(tuple,targets(base)[t]['sizes']))]
        assert len(matches)==1, f'Select a matching --target for {size}'
        for c in configs:save(c,matches[0],size)
    elif a.preview:
        for c in configs:
            for target in selected:preview(c,target)
    else:
        for c in configs:validate(c,selected)
