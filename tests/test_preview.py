"""Preview API renders only requested screens, preserving full layout context."""
import base64
import http.client
import io
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from unittest.mock import patch

from PIL import Image

from nimoteshot import server


class PreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join()

    def setUp(self):
        buffer = io.BytesIO()
        Image.new('RGB', (100, 200), 'navy').save(buffer, format='PNG')
        self.payload = {
            'brand': 'Preview app', 'description': 'Real product screens',
            'locales': ['zh-CN'], 'targets': ['iphone_portrait', 'iphone_landscape'],
            'files': [{'name': f'{index}.png', 'data': base64.b64encode(buffer.getvalue()).decode()}
                      for index in range(2)],
            'proposal': {'schema_version': 1, 'screens': [
                {'file': f'{index}.png', 'title_en': [f'Feature {index}'], 'subtitle_en': 'Visible tools',
                 'title_zh': [f'功能 {index}'], 'subtitle_zh': '可见工具',
                 'design': {'template': 'balanced', 'background': index}} for index in range(2)]},
        }

    def request(self, **overrides):
        conn = http.client.HTTPConnection('127.0.0.1', self.httpd.server_port, timeout=30)
        try:
            conn.request('POST', '/api/preview', json.dumps({**self.payload, **overrides}),
                         {'Content-Type': 'application/json'})
            response = conn.getresponse()
            return response.status, json.loads(response.read())
        finally:
            conn.close()

    def test_subset_matches_full_render_and_keeps_numbering_language_and_duo_sources(self):
        self.payload['proposal']['screens'][1]['design'] = {
            'template': 'duo', 'background': 1, 'secondary_file': '0.png'}
        for target in self.payload['targets']:
            for language in ('en-US', 'zh-CN'):
                with self.subTest(target=target, language=language):
                    status, full = self.request(preview_target=target, preview_locale=language)
                    self.assertEqual(status, 200, full)
                    self.assertEqual(full['indices'], [0, 1])
                    name = 'render' if target == 'iphone_portrait' else 'render_landscape'
                    with patch.object(server.renderer, name, wraps=getattr(server.renderer, name)) as render:
                        status, subset = self.request(preview_indices=[1], preview_target=target, preview_locale=language)
                    self.assertEqual(status, 200, subset)
                    self.assertEqual(subset['indices'], [1])
                    self.assertEqual(subset['images'], [full['images'][1]])
                    self.assertEqual(render.call_count, 1)
                    config, screen = render.call_args.args[:2]
                    self.assertEqual(len(config['screens']), 2)
                    self.assertEqual(config['screens'].index(screen), 1)

    def test_requested_order_is_explicit(self):
        status, full = self.request()
        self.assertEqual(status, 200, full)
        status, reverse = self.request(preview_indices=[1, 0])
        self.assertEqual(status, 200, reverse)
        self.assertEqual(reverse['indices'], [1, 0])
        self.assertEqual(reverse['images'], list(reversed(full['images'])))

    def test_invalid_indices_are_rejected_before_rendering(self):
        for indices in (None, [], '0', [True], [-1], [2], [0, 0], [0.5], [{}]):
            with self.subTest(indices=indices), patch.object(server.renderer, 'render') as render:
                status, result = self.request(preview_indices=indices)
                self.assertEqual(status, 400, result)
                render.assert_not_called()
