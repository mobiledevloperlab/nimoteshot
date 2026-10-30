"""Real loopback tests for verified restarts and unrelated listener preservation."""
import errno
import http.client
import json
import os
import queue
import subprocess
import sys
import stat
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from nimoteshot import server, web_runtime


class WebRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.token_path = Path(self.directory.name) / 'project' / 'token'
        jobs = patch.object(server, 'JOBS', {})
        jobs.start()
        self.addCleanup(jobs.stop)

    def start(self, httpd):
        def run():
            try:
                httpd.serve_forever(poll_interval=0.02)
            finally:
                httpd.server_close()
        thread = threading.Thread(target=run, daemon=True)
        thread.start()

        def cleanup():
            if thread.is_alive():
                httpd.shutdown()
            thread.join(timeout=5)
            httpd.server_close()
        self.addCleanup(cleanup)
        return thread

    def bind(self, port=0, token_path=None):
        httpd = web_runtime.bind_studio('127.0.0.1', port, server.Handler, token_path or self.token_path)
        self.addCleanup(httpd.server_close)
        return httpd

    def request(self, httpd, method='GET', route='/api/studio', payload=None, headers=None):
        connection = http.client.HTTPConnection('127.0.0.1', httpd.server_port, timeout=3)
        try:
            connection.request(method, route, json.dumps(payload) if payload is not None else None, headers or {})
            response = connection.getresponse()
            return response.status, response.read()
        finally:
            connection.close()

    def test_verified_idle_studio_is_replaced(self):
        old = self.bind()
        old_thread = self.start(old)
        replacement = self.bind(old.server_port)
        if os.name != 'nt':
            self.assertEqual(replacement.server_port, old.server_port)
        old_thread.join(timeout=3)
        self.assertFalse(old_thread.is_alive())
        self.assertNotEqual(replacement.studio_instance, old.studio_instance)
        self.start(replacement)
        self.assertEqual(self.request(replacement, route='/')[0], 200)

    def test_different_project_is_preserved(self):
        old = self.bind()
        thread = self.start(old)
        replacement = self.bind(old.server_port, Path(self.directory.name) / 'another-project' / 'token')
        self.assertNotEqual(replacement.server_port, old.server_port)
        self.assertTrue(thread.is_alive())
        self.assertFalse(old.studio_draining)
        self.assertEqual(self.request(old, route='/')[0], 200)

    def test_active_generation_is_preserved_and_new_studio_uses_another_port(self):
        old = self.bind()
        thread = self.start(old)
        for state in ('queued', 'running'):
            with self.subTest(state=state):
                server.JOBS['working'] = {'status': state}
                replacement = self.bind(old.server_port)
                self.assertNotEqual(replacement.server_port, old.server_port)
                self.assertTrue(thread.is_alive())
                self.assertFalse(old.studio_draining)

    def test_unrelated_listener_is_not_sent_a_shutdown_request(self):
        requests = []

        class OtherHandler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                requests.append(('GET', self.path))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"instance":"00000000000000000000000000000000","proof":"wrong"}')

            def do_POST(self):
                requests.append(('POST', self.path))
                self.send_response(500)
                self.end_headers()

        old = ThreadingHTTPServer(('127.0.0.1', 0), OtherHandler)
        thread = self.start(old)
        replacement = self.bind(old.server_port)
        self.assertNotEqual(replacement.server_port, old.server_port)
        self.assertTrue(thread.is_alive())
        self.assertEqual(requests, [('GET', '/api/studio')])

    def test_missing_corrupt_or_unreadable_identity_never_authorizes_shutdown(self):
        old = self.bind()
        thread = self.start(old)
        self.token_path.write_text('corrupted', encoding='ascii')
        replacement = self.bind(old.server_port)
        self.assertNotEqual(replacement.server_port, old.server_port)
        with patch.object(web_runtime, 'project_token', side_effect=PermissionError('unreadable')):
            another = self.bind(old.server_port)
        self.assertNotEqual(another.server_port, old.server_port)
        self.assertTrue(thread.is_alive())
        self.assertFalse(old.studio_draining)

    def test_shutdown_requires_current_instance_proof_and_local_origin(self):
        httpd = self.bind()
        self.start(httpd)
        for payload in ({}, {'instance': 'old', 'proof': '0' * 64},
                        {'instance': httpd.studio_instance, 'proof': '非' * 64}):
            with self.subTest(payload=payload):
                self.assertEqual(self.request(httpd, 'POST', '/api/studio/shutdown', payload)[0], 403)
        valid = {'instance': httpd.studio_instance,
                 'proof': web_runtime.signature(httpd.studio_token, 'shutdown:' + httpd.studio_instance)}
        self.assertEqual(self.request(httpd, 'POST', '/api/studio/shutdown', valid,
                                      {'Origin': 'https://evil.example'})[0], 403)
        self.assertFalse(httpd.studio_draining)

    def test_restart_race_cannot_enqueue_a_new_job_after_shutdown_begins(self):
        httpd = self.bind()
        self.start(httpd)
        httpd.studio_draining = True
        with patch.object(server, 'plan') as plan:
            status, _ = self.request(httpd, 'POST', '/api/plan',
                                     {'brand': 'App', 'description': 'Visible interface'})
        self.assertEqual(status, 409)
        self.assertEqual(server.JOBS, {})
        plan.assert_not_called()

    def test_invalid_ports_and_non_loopback_hosts_are_rejected_before_binding(self):
        for host, port in (('0.0.0.0', 8765), ('127.0.0.1', -1), ('localhost', 65536), ('localhost', True)):
            with self.subTest(host=host, port=port), self.assertRaises(ValueError):
                web_runtime.bind_studio(host, port, server.Handler, self.token_path)
        self.assertFalse(self.token_path.exists())

    def test_non_conflict_bind_error_is_reported_without_stopping_any_service(self):
        with patch.object(web_runtime, 'StudioHTTPServer', side_effect=PermissionError(errno.EACCES, 'denied')), \
                patch.object(web_runtime, 'stop_previous') as stop:
            with self.assertRaisesRegex(RuntimeError, 'Cannot start'):
                self.bind(8765)
            stop.assert_not_called()

    def test_untrusted_malformed_identity_is_ignored(self):
        for identity in (None, [], {'instance': 123}, {'instance': 'f' * 32, 'proof': '非' * 64}):
            with self.subTest(identity=identity), patch.object(web_runtime, 'local_json', return_value=(200, identity)) as request:
                self.assertFalse(web_runtime.stop_previous('127.0.0.1', 1234, 'a' * 64))
                self.assertEqual(request.call_count, 1)

    def test_cli_restart_exits_old_process_and_prints_actual_live_address(self):
        environment = {**os.environ, 'XDG_CONFIG_HOME': self.directory.name, 'APPDATA': self.directory.name}

        def start(port):
            process = subprocess.Popen(
                [sys.executable, '-u', str(server.ROOT / 'scripts/nimoteshot.py'),
                 'web', '--no-browser', '--port', str(port)], cwd=server.ROOT,
                env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            def cleanup():
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait(timeout=5)
                process.stdout.close()
            self.addCleanup(cleanup)
            output = queue.Queue()

            def read():
                for line in process.stdout:
                    output.put(line.strip())
                    if line.startswith('NimoteShot ready at '):
                        break
            reader = threading.Thread(target=read, daemon=True)
            reader.start()
            lines = []
            while True:
                line = output.get(timeout=20)
                lines.append(line)
                if line.startswith('NimoteShot ready at '):
                    reader.join(timeout=2)
                    return process, int(line.rsplit(':', 1)[1]), lines

        old, port, _ = start(0)
        replacement, replacement_port, lines = start(port)
        self.assertEqual(old.wait(timeout=5), 0)
        self.assertIsNone(replacement.poll())
        self.assertTrue(any('Restarting the verified NimoteShot' in line for line in lines))
        status, _ = web_runtime.local_json('127.0.0.1', replacement_port, 'GET', '/api/studio',
                                          headers={'X-NimoteShot-Challenge': 'f' * 64})
        self.assertEqual(status, 200)
        # Legacy instances have no private identity endpoint. The CLI must
        # preserve them and print the replacement's actual fallback address.
        legacy = ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        legacy_thread = self.start(legacy)
        fallback, fallback_port, lines = start(legacy.server_port)
        self.assertIsNone(fallback.poll())
        self.assertNotEqual(fallback_port, legacy.server_port)
        self.assertTrue(legacy_thread.is_alive())
        self.assertTrue(any('choosing another local port' in line for line in lines))
        self.assertEqual(self.request(legacy, route='/')[0], 200)
        status, _ = web_runtime.local_json('127.0.0.1', fallback_port, 'GET', '/api/studio',
                                          headers={'X-NimoteShot-Challenge': 'f' * 64})
        self.assertEqual(status, 200)

    def test_token_is_stable_private_and_outside_served_project_files(self):
        token = web_runtime.project_token(self.token_path)
        self.assertEqual(web_runtime.project_token(self.token_path), token)
        if os.name != 'nt':
            self.assertEqual(stat.S_IMODE(self.token_path.stat().st_mode), 0o600)
        with patch.object(web_runtime, 'config_path', return_value=Path(self.directory.name) / 'config.json'):
            first = web_runtime.runtime_token_path(Path('/project-a'))
            second = web_runtime.runtime_token_path(Path('/project-b'))
        self.assertNotEqual(first, second)
        self.assertFalse(first.is_relative_to(server.RUNS))
