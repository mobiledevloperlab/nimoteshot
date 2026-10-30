"""Unicode input is rendered from glyph coverage rather than the copy locale."""
import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw, features

from nimoteshot import pipeline

renderer = pipeline.renderer
FONTS = renderer.ROOT / 'store_screenshots/assets/fonts'
SAMPLES = (
    ('English', 'Code tools', 'Edit on the go'),
    ('Chinese', '代码工具', '随身编程'),
    ('Traditional Chinese', '程式工具', '隨身使用'),
    ('Japanese', 'コード編集', '外出先で編集'),
    ('Korean', '코드 도구', '휴대폰에서 편집'),
    ('Spanish', 'Código móvil', 'Edición rápida'),
    ('French', 'Éditez le code', 'Outils mobiles'),
    ('German', 'Code ändern', 'Überall arbeiten'),
    ('Portuguese', 'Código portátil', 'Edição rápida'),
    ('Russian', 'Редактор кода', 'Код под рукой'),
    ('Greek', 'Κώδικας', 'Εργαλεία κώδικα'),
    ('Vietnamese', 'Công cụ mã', 'Chỉnh sửa mã'),
    ('Arabic', 'أدوات الكود', 'تحرير متنقل'),
    ('Hindi', 'कोड उपकरण', 'फोन पर काम'),
    ('Bengali', 'কোড সরঞ্জাম', 'ফোনে কাজ'),
    ('Thai', 'เครื่องมือโค้ด', 'แก้ไขบนมือถือ'),
    ('Hebrew', 'כלי קוד', 'עריכה בנייד'),
    ('Mixed Chinese and English', '代码 Code', '编辑 Git files'),
)


class TypographyTests(unittest.TestCase):
    def test_selected_font_covers_every_character_in_major_language_samples(self):
        for language, title, subtitle in SAMPLES:
            for text in (title, subtitle):
                for weight in ('Regular', 'Bold'):
                    with self.subTest(language=language, text=text, weight=weight):
                        path = renderer.text_font_path(FONTS / 'Inter.ttf', text, weight)
                        self.assertTrue({ord(char) for char in text if not char.isspace()} <= renderer.font_characters(str(path)))
                        face = renderer.load_font(path, 32, weight)
                        self.assertIsNotNone(face.getbbox(text))

    def test_english_keeps_existing_font_and_cjk_really_changes_glyphs(self):
        self.assertEqual(renderer.text_font_path(FONTS / 'Inter.ttf', 'Code tools'), FONTS / 'Inter.ttf')
        path = renderer.text_font_path(FONTS / 'Inter.ttf', '代码工具', 'Bold')
        face = renderer.load_font(path, 32, 'Bold')
        self.assertEqual(path.name, 'NotoSansCJKsc-Bold.otf')
        self.assertNotEqual(bytes(face.getmask('代码工具')), bytes(face.getmask('终端工具')))

    def test_missing_glyphs_report_an_error_instead_of_rendering_boxes(self):
        with self.assertRaisesRegex(ValueError, 'No bundled font'):
            renderer.text_font_path(FONTS / 'Inter.ttf', 'Unicorn 🦄')

    def test_complex_scripts_require_shaping_and_do_not_silently_use_basic_layout(self):
        with patch.object(renderer.features, 'check', return_value=False):
            for text in ('العربية', 'हिन्दी', 'বাংলা', 'ไทย', 'עברית'):
                with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'libraqm shaping'):
                    renderer.validate_text_layout(text)
            renderer.validate_text_layout('Code')
            self.assertEqual(renderer.text_font_path(FONTS / 'Inter.ttf', 'Code'), FONTS / 'Inter.ttf')

    def test_cjk_font_metrics_are_used_for_fitting(self):
        draw = ImageDraw.Draw(Image.new('RGB', (320, 200)))
        font = renderer.fit_text(draw, ['代码工具 Code'], FONTS / 'Inter.ttf', 160, 40, 12)
        self.assertLessEqual(draw.textbbox((0, 0), '代码工具 Code', font=font)[2], 160)
        self.assertIn('Noto', font.getname()[0])
