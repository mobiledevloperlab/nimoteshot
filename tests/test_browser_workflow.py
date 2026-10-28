"""Chromium E2E: SHOTNIMOTE_BROWSER_TEST=1 python -m unittest discover -s tests -p test_browser_workflow.py -v.

Optional live test uses test.md only when SHOTNIMOTE_LIVE_TEST=1, and sends exactly
code-editor.png and terminal.png. No credentials, network traces or profile changes are saved.
"""
import json
import os
import re
import tempfile
import threading
import unittest
import zipfile
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from nimoteshot import pipeline, server

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.environ.get('SHOTNIMOTE_BROWSER_TEST') == '1', 'Browser tests run in the dedicated Chromium job')
class BrowserWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.httpd = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f'http://127.0.0.1:{cls.httpd.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown(); cls.httpd.server_close(); cls.thread.join()
        cls.browser.close(); cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width':1280,'height':900})
        self.page = self.context.new_page()
        self.errors = []
        self.page.on('pageerror',lambda error:self.errors.append(str(error)))
        self.page.on('response',lambda response:print('Preview error:',response.text()) if '/api/preview' in response.url and response.status>=400 else None)
        self.page.goto(self.url)
        self.page.wait_for_function("document.getElementById('generate').disabled === false")
        self.page.select_option('#language','en')
        self.page.fill('#brand','NimoteCode')
        self.page.fill('#description','Mobile development workspace. Only describe features visible in each screenshot.')
        # Two languages and two real source captures; no other source is used.
        for item in self.page.locator('#locale-list input:not(:disabled)').all():
            item.set_checked(item.get_attribute('value') == 'zh-CN')
        self.page.click('#step-next')
        self.page.set_input_files('#files',[str(ROOT/'demo/nimotecode/originals'/name) for name in ('code-editor.png','terminal.png')])
        for item in self.page.locator('.export-targets input').all():
            item.set_checked(item.get_attribute('value') == 'iphone_portrait')
        self.page.click('#step-next'); self.page.click('#step-next')

    def tearDown(self):
        self.context.close()

    def wait_preview(self):
        self.page.wait_for_function("['ready','error'].includes(document.getElementById('preview-status')?.dataset.state)",timeout=60000)
        self.assertEqual(self.page.locator('#preview-status').get_attribute('data-state'),'ready',self.page.locator('#preview-status').inner_text())
        self.assertEqual(self.page.locator('#live-design-preview img').count(),2)

    def edit_and_export(self):
        self.page.wait_for_selector('#design-editor')
        self.wait_preview()
        self.page.locator('[data-copy-key=title_en][data-screen-index="1"]').fill('Code tools\nOn your phone')
        self.wait_preview()
        self.page.get_by_label('Copy and preview language',exact=True).select_option('zh')
        self.wait_preview()
        self.page.locator('[data-copy-key=title_zh][data-screen-index="1"]').fill('代码工具\n随身使用')
        self.wait_preview()
        # Cover new compositions, safe crop tokens and ordering through actual DOM events.
        self.page.get_by_label('Template',exact=True).nth(0).select_option('detail')
        self.wait_preview()
        self.page.get_by_label('Template',exact=True).nth(1).select_option('duo')
        self.wait_preview()
        self.page.get_by_label('Move up 2',exact=True).click(); self.wait_preview()
        self.page.set_viewport_size({'width':390,'height':844})
        self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'))
        for theme in ('light','dark'):
            self.page.evaluate('(theme)=>document.documentElement.dataset.theme=theme',theme)
            for selector in ('.brand-icon','.footer-logo'):
                self.assertTrue(self.page.locator(selector).evaluate('(image)=>image.complete && image.naturalWidth > 0'))
        self.page.click('#export-design')
        self.page.wait_for_function("!document.getElementById('download').classList.contains('hidden') || !document.getElementById('error').classList.contains('hidden')",timeout=180000)
        self.assertTrue(self.page.locator('#error').evaluate('(e)=>e.classList.contains("hidden")'),self.page.locator('#error').inner_text())
        href=self.page.locator('#download').get_attribute('href')
        response=self.context.request.get(self.url+href)
        self.assertEqual(response.status,200)
        import io
        with zipfile.ZipFile(io.BytesIO(response.body())) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(len([name for name in archive.namelist() if name.endswith('.png')]),28)
        self.assertEqual(self.errors,[])
        return href

    def test_manual_design_edit_preview_reorder_and_zip_without_ai_key(self):
        with patch.object(pipeline,'analyze',side_effect=AssertionError('Manual editing must not call AI')):
            self.page.check('#manual-mode');self.page.click('#generate')
            self.page.wait_for_selector('#design-editor')
            self.assertEqual(self.page.locator('.design-screen-body').count(),2)
            self.assertEqual(self.page.locator('.design-source img').count(),2)
            positions=self.page.locator('.design-screen-body').first.evaluate("node=>({source:node.querySelector('.design-source').getBoundingClientRect().left,configuration:node.querySelector('.design-configuration').getBoundingClientRect().left})")
            self.assertLess(positions['source'],positions['configuration'])
            self.edit_and_export()
            self.assertTrue(self.page.locator('#export-location').is_visible())
            self.assertTrue(self.page.locator('#export-path').inner_text().endswith('/exports'))
            self.assertTrue(self.page.locator('#open-export').is_visible())
            self.assertEqual(self.page.locator('#export-progress-value').inner_text(),'100%')

    def test_ai_failure_keeps_manual_workflow_available(self):
        with patch.object(pipeline,'cached_analysis',side_effect=lambda directory,identity,produce,validate,*args,**kwargs:validate(produce())), patch.object(pipeline,'analyze',side_effect=ValueError('Vision model did not return valid JSON')):
            self.page.fill('#api-key','fake-test-key');self.page.click('#generate')
            self.page.wait_for_function("document.getElementById('error').textContent.includes('invalid design')",timeout=30000)
            self.page.check('#manual-mode');self.page.click('#generate');self.wait_preview()
        self.assertEqual(self.errors,[])

    def test_new_editor_controls_follow_all_five_interface_languages(self):
        self.page.check('#manual-mode');self.page.click('#generate');self.wait_preview()
        self.page.locator('[data-copy-key=title_en][data-screen-index="1"]').fill('Keep my copy')
        for language in ('zh','en','ja','ko','es'):
            self.page.select_option('#language',language)
            labels=self.page.evaluate('(language)=>editorMessages[language]',language)
            for key in ('regenerateCopy','recommendLayouts','reanalyze','exportDesign'):
                self.assertEqual(self.page.get_by_role('button',name=labels[key],exact=True).count(),1)
            self.assertEqual(self.page.get_by_label(labels['editTemplate'],exact=True).count(),2)
            self.assertEqual(self.page.locator('[data-i18n=manualMode]').inner_text(),labels['manualMode'])
            self.assertEqual(self.page.locator('[data-copy-key=title_en][data-screen-index="1"]').input_value(),'Keep my copy')
            self.assertEqual(self.page.get_by_label(labels['editTemplate'],exact=True).first.locator('option[value=duo]').inner_text(),labels['duo'])
        self.assertEqual(self.errors,[])

    @unittest.skipUnless(os.environ.get('SHOTNIMOTE_LIVE_TEST') == '1','Live API testing is explicitly opt-in')
    def test_live_two_image_analysis_copy_layout_and_export(self):
        text=(ROOT/'test.md').read_text()
        match=re.search(r'(?im)^\s*apikey\s*[:：]\s*(.+?)\s*$',text)
        self.assertIsNotNone(match,'test.md requires an apikey field')
        self.page.select_option('#provider','deepseek')
        self.page.fill('#api-key',match.group(1).strip().strip('`\"\''))
        self.page.click('#generate');self.page.wait_for_selector('#design-editor',timeout=180000)
        self.wait_preview()
        self.page.get_by_role('button',name='Regenerate copy',exact=True).click()
        self.page.wait_for_function("document.getElementById('generate').disabled === false",timeout=180000)
        self.assertTrue(self.page.locator('#error').evaluate('(e)=>e.classList.contains("hidden")'))
        self.page.get_by_role('button',name='Recommend layouts',exact=True).click()
        self.page.wait_for_function("document.getElementById('generate').disabled === false",timeout=30000)
        self.wait_preview()
        templates=self.page.get_by_label('Template',exact=True).evaluate_all('(items)=>items.map(item=>item.value)')
        self.assertEqual(set(templates),{'compact','showcase'})
        href=self.edit_and_export()
        output=ROOT/'test_outputs';output.mkdir(exist_ok=True)
        (output/'browser-live-result.json').write_text(json.dumps({'download':href,'templates':templates,'source_count':2,'pngs':28,'browser_errors':self.errors},indent=2))
        self.page.screenshot(path=str(output/'browser-live-mobile.png'),full_page=True)
