import http.client
import json
import os
import stat
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from nimoteshot import providers, server, settings


class LocalHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.httpd.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join()

    def request(self, method='GET', path='/', body=None, headers=None):
        conn = http.client.HTTPConnection('127.0.0.1', self.port, timeout=3)
        try:
            conn.request(method, path, body=body, headers=headers or {})
            response = conn.getresponse()
            return response.status, response.read()
        finally:
            conn.close()

    def test_local_page_works(self):
        status, body = self.request()
        self.assertEqual(status, 200)
        self.assertIn(b'NimoteShot', body)

    def test_public_documents_are_allowlisted_and_served_as_text(self):
        for slug, filename in server.PUBLIC_DOCUMENTS.items():
            conn = http.client.HTTPConnection('127.0.0.1', self.port, timeout=3)
            try:
                conn.request('GET', '/docs/' + slug)
                response = conn.getresponse()
                self.assertEqual(response.status, 200)
                self.assertEqual(response.getheader('Content-Type'), 'text/plain; charset=utf-8')
                self.assertEqual(response.getheader('X-Content-Type-Options'), 'nosniff')
                self.assertEqual(response.read(), (server.ROOT / filename).read_bytes())
            finally:
                conn.close()
        for path in ('/docs/../LICENSE', '/docs/%2e%2e/.git/config', '/docs/.env', '/docs/nimoteshot/settings.py'):
            self.assertEqual(self.request(path=path)[0], 404)

    def test_rebinding_host_blocks_reads_and_writes_before_provider_calls(self):
        with patch.object(server, 'check_connection') as check:
            for method, path in [('GET', '/api/options'), ('POST', '/api/check-model')]:
                status, _ = self.request(method, path, '{}', {'Host': f'evil.example:{self.port}'})
                self.assertEqual(status, 403)
            check.assert_not_called()

    def test_cross_origin_and_cross_site_blocked(self):
        for headers in ({'Origin': 'https://evil.example'}, {'Origin': 'null'}, {'Sec-Fetch-Site': 'cross-site'}):
            self.assertEqual(self.request('POST', '/api/check-model', '{}', headers)[0], 403)

    def test_invalid_json_shape_and_length_return_client_error(self):
        for body in ('[]', 'null', '"text"', '{'):
            self.assertEqual(self.request('POST', '/api/check-model', body)[0], 400)
        self.assertEqual(self.request('POST', '/api/check-model', '{}', {'Content-Length': 'invalid'})[0], 400)
        self.assertEqual(self.request('POST', '/api/check-model', '{}', {'Content-Length': '10001'})[0], 413)

    def test_same_origin_post_succeeds(self):
        with patch.object(server, 'check_connection', return_value={'ready': True}):
            status, body = self.request('POST', '/api/check-model', '{}', {'Origin': f'http://127.0.0.1:{self.port}'})
            self.assertEqual(status, 200)
            self.assertTrue(json.loads(body)['ready'])

    def test_path_traversal_denied(self):
        for path in ('/files/../../LICENSE', '/%2e%2e/LICENSE', '/assets/demo-previews/../../config.json'):
            self.assertEqual(self.request(path=path)[0], 403)

    def test_public_binding_rejected(self):
        with self.assertRaises(ValueError):
            server.serve('0.0.0.0', open_browser=False)


class CredentialTests(unittest.TestCase):
    def test_ollama_rejects_authority_confusion(self):
        with patch.object(providers, 'profile', return_value={}):
            for url in ('http://localhost:123@evil.example', 'http://127.0.0.1:123@evil.example',
                        'http://localhost:11434/path', 'http://localhost:11434?host=evil',
                        'http://localhost:11434#fragment', 'https://localhost:11434'):
                with self.subTest(url=url), self.assertRaises(ValueError):
                    providers.choice('ollama', base_url=url)
            self.assertEqual(providers.choice('ollama', base_url='http://localhost:11434/')[1], 'http://localhost:11434')

    def test_profile_atomic_replace_failure_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(settings, 'config_path', return_value=Path(temp) / 'config.json'):
            path = settings.save('qwen', api_key='test-value')
            previous = path.read_bytes()
            with patch.object(settings.os, 'replace', side_effect=OSError('failed')):
                with self.assertRaises(OSError):
                    settings.save('qwen', api_key='replacement')
            self.assertEqual(path.read_bytes(), previous)
            self.assertEqual(list(Path(temp).iterdir()), [path])
            if os.name != 'nt':
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

    @unittest.skipIf(os.name == 'nt', 'Unix symlink semantics')
    def test_profile_save_does_not_overwrite_symlink_target(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'other-file'
            target.write_text('untouched')
            path = Path(temp) / 'config.json'
            path.symlink_to(target)
            with patch.object(settings, 'config_path', return_value=path):
                settings.save('qwen', api_key='test-value')
            self.assertEqual(target.read_text(), 'untouched')
            self.assertFalse(path.is_symlink())
