"""Validated multi-resolution export using the existing renderer and ZIP library."""
import shutil
import zipfile


def export(config, directory, renderer, progress):
    expected = 0
    for language in renderer.locales(config):
        localized = renderer.localized(config, language)
        presets = renderer.targets(localized)
        for name, preset in presets.items():
            progress(f'Rendering {language} / {name}')
            for size in map(tuple, preset['sizes']):
                renderer.save(localized, name, size)
                expected += len(localized['screens'])
            renderer.preview(localized, name)
        renderer.validate(localized, list(presets))
    progress('Packaging and validating ZIP')
    archive = shutil.make_archive(str(directory / f"nimoteshot_{config['task_id']}"), 'zip', root_dir=directory, base_dir='exports')
    with zipfile.ZipFile(archive) as package:
        pngs = [name for name in package.namelist() if name.endswith('.png')]
        if len(pngs) != expected or len(set(pngs)) != expected or package.testzip() is not None:
            raise ValueError('Export archive failed completeness or CRC validation')
    return archive
