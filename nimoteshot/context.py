"""Fetch bounded, public website text as optional app context."""
import ipaddress
import socket
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlsplit


def _public_https(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Website URL must be a public HTTPS address")
    try:
        addresses = socket.getaddrinfo(parsed.hostname, parsed.port or 443, type=socket.SOCK_STREAM)
    except socket.gaierror as error:
        raise ValueError("Website hostname could not be resolved") from error
    if not addresses or any(not ipaddress.ip_address(item[4][0]).is_global for item in addresses):
        raise ValueError("Website must resolve only to public addresses")


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        _public_https(newurl)
        return super().redirect_request(request, fp, code, msg, headers, newurl)


class _Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip += 1
        if tag == "meta":
            attrs = dict(attrs)
            if attrs.get("name", "").lower() == "description":
                self.parts.append(attrs.get("content", ""))

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())


def fetch_website(url):
    if not url:
        return ""
    _public_https(url)
    opener = urllib.request.build_opener(_SafeRedirect())
    request = urllib.request.Request(url, headers={"User-Agent": "NimoteShot/1.0", "Accept": "text/html"})
    try:
        with opener.open(request, timeout=12) as response:
            if "html" not in response.headers.get("Content-Type", "").lower():
                raise ValueError("Website must return an HTML page")
            raw = response.read(250001)
    except ValueError:
        raise
    except Exception as error:
        raise ValueError(f"Could not read website: {error}") from error
    if len(raw) > 250000:
        raw = raw[:250000]
    parser = _Text()
    parser.feed(raw.decode("utf-8", "replace"))
    return " ".join(parser.parts)[:4000]
