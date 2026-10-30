"""Bind the local studio and cooperatively replace verified project instances."""
import errno
import hashlib
import hmac
import http.client
import json
import os
import secrets
import socket
from socketserver import TCPServer
import time
from http.server import ThreadingHTTPServer

from .settings import config_path


class StudioHTTPServer(ThreadingHTTPServer):
    # Windows SO_REUSEADDR can let another listener bind an occupied port.
    allow_reuse_address = os.name != 'nt'

    def server_bind(self):
        if os.name == 'nt' and hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        # Loopback startup does not need a potentially blocking reverse-DNS lookup.
        TCPServer.server_bind(self)
        self.server_name, self.server_port = self.server_address[:2]


def runtime_token_path(root):
    project = hashlib.sha256(os.fsencode(root.resolve())).hexdigest()
    return config_path().parent / 'studio' / project / 'token'


def signature(token, message):
    return hmac.new(token.encode('ascii'), message.encode('ascii'), hashlib.sha256).hexdigest()


def project_token(path):
    """Keep a private project secret; never identify a process by PID alone."""
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        token = path.read_text(encoding='ascii')
    else:
        token = secrets.token_hex(32)
        with os.fdopen(descriptor, 'w', encoding='ascii') as stream:
            stream.write(token)
    if len(token) != 64 or any(character not in '0123456789abcdef' for character in token):
        raise ValueError('Invalid studio runtime token')
    return token


def local_json(host, port, method, route, payload=None, headers=None):
    connection = http.client.HTTPConnection(host, port, timeout=0.8)
    try:
        body = json.dumps(payload) if payload is not None else None
        connection.request(method, route, body, headers or {})
        response = connection.getresponse()
        data = response.read(4097)
        if len(data) > 4096:
            raise ValueError('Unexpected studio response')
        return response.status, json.loads(data)
    finally:
        connection.close()


def stop_previous(host, port, token):
    """Only the instance proving possession of this project's secret may stop."""
    if token is None:
        return False
    try:
        challenge = secrets.token_hex(32)
        status, identity = local_json(host, port, 'GET', '/api/studio',
                                      headers={'X-NimoteShot-Challenge': challenge})
        if status != 200 or not isinstance(identity, dict):
            return False
        instance = identity.get('instance')
        proof = identity.get('proof')
        if (not isinstance(instance, str) or len(instance) != 32
                or any(character not in '0123456789abcdef' for character in instance)
                or not isinstance(proof, str) or len(proof) != 64
                or any(character not in '0123456789abcdef' for character in proof)
                or not hmac.compare_digest(proof, signature(token, 'identity:' + challenge + ':' + instance))):
            return False
        status, result = local_json(host, port, 'POST', '/api/studio/shutdown',
                                    {'instance': instance, 'proof': signature(token, 'shutdown:' + instance)},
                                    {'Content-Type': 'application/json'})
        if status == 409:
            print('Existing NimoteShot has active tasks; keeping it running.')
        return status == 200 and isinstance(result, dict) and result.get('stopping') is True
    except (OSError, ValueError, http.client.HTTPException):
        return False


def address_in_use(error):
    return error.errno == errno.EADDRINUSE or getattr(error, 'winerror', None) == 10048


def bind_studio(host, port, handler, token_path):
    if host not in ('127.0.0.1', 'localhost'):
        raise ValueError('The studio must listen on 127.0.0.1 or localhost')
    if type(port) is not int or not 0 <= port <= 65535:
        raise ValueError('Choose a port between 0 and 65535')
    try:
        token = project_token(token_path)
    except (OSError, ValueError):
        # Failure to establish identity must never authorize stopping a process.
        token = None
        print('Studio restart verification is unavailable; occupied ports will be skipped.')

    def bind(candidate):
        server = StudioHTTPServer((host, candidate), handler)
        server.studio_token = token
        server.studio_instance = secrets.token_hex(16)
        server.studio_draining = False
        return server

    try:
        return bind(port)
    except OSError as error:
        if not address_in_use(error):
            raise RuntimeError(f'Cannot start the local studio: {error}') from error
    if port and stop_previous(host, port, token):
        print(f'Restarting the verified NimoteShot instance on port {port}.')
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            try:
                return bind(port)
            except OSError as error:
                if not address_in_use(error):
                    raise RuntimeError(f'Cannot restart the local studio: {error}') from error
            time.sleep(0.05)
    print(f'Port {port} is in use; choosing another local port.')
    candidates = (*range(port + 1, min(port + 21, 65536)), 0) if port else (0,)
    for candidate in candidates:
        try:
            return bind(candidate)
        except OSError as error:
            if not address_in_use(error):
                raise RuntimeError(f'Cannot start the local studio: {error}') from error
    raise RuntimeError('No local studio port is available')
