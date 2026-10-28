"""Shared verified capture loading for CLI, planning and browser previews."""
import base64
from pathlib import Path

from PIL import Image, UnidentifiedImageError

EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}
MAX_IMAGE_BYTES = 32 * 1024 * 1024


def verify(path):
    try:
        if path.stat().st_size > MAX_IMAGE_BYTES:
            raise ValueError('Each capture must be at most 32 MiB')
        with Image.open(path) as image:
            if image.format not in ('PNG', 'JPEG', 'WEBP') or max(image.size) > 8192:
                raise ValueError('Use PNG/JPEG/WebP captures up to 8192 pixels per side')
            image.verify()
    except (UnidentifiedImageError, Image.DecompressionBombError, OSError) as error:
        raise ValueError('Capture is not a valid supported image') from error


def collect(directory):
    files = sorted(p for p in Path(directory).iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS)
    if not 1 <= len(files) <= 40:
        raise ValueError('Provide 1-40 PNG, JPEG or WebP captures')
    for path in files:
        verify(path)
    return files


def unpack(items, directory):
    if not isinstance(items, list) or not 1 <= len(items) <= 40:
        raise ValueError('Upload 1-40 captures')
    names = set()
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get('name'), str) or not isinstance(item.get('data'), str):
            raise ValueError('Each capture needs a name and base64 data')
        name = item['name']
        if (not name or Path(name).name != name or '\\' in name or '\x00' in name
                or Path(name).suffix.lower() not in EXTENSIONS or name.casefold() in names):
            raise ValueError('Use unique PNG/JPEG/WebP filenames without paths')
        names.add(name.casefold())
        raw = base64.b64decode(item['data'], validate=True)
        path = Path(directory) / name
        path.write_bytes(raw)
        verify(path)
    return collect(directory)
