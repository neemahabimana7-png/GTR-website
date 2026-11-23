r"""Verify original bytes, copied assets, page DOM/content and unchanged scripts.

Run from django_backend: .venv\Scripts\python.exe scripts\verify_frontend.py
This is structural equivalence, not a browser screenshot comparison.
"""
import hashlib
import json
import os
import posixpath
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
import django
django.setup()
from django.test import Client
from django.urls import reverse
from website.pages import PAGES

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
ROUTES = {source: reverse('website:' + name) for name, (_, source) in PAGES.items()}
ROUTES['contact.html'] = reverse('inquiries:contact')
ROUTES['services/services-details-quality/services-details-supply.html'] = reverse('website:supply')


class PageDOM(HTMLParser):
    def __init__(self, source=None):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.tokens = []
        self.skipping = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.skipping:
            if tag not in VOID:
                self.skipping += 1
            return
        if 'hidden' in attrs:
            self.skipping = 0 if tag in VOID else 1
            return
        if tag == 'input' and attrs.get('type') == 'hidden':
            return
        # Only form transport/validation bindings may differ.
        if tag in {'form', 'input', 'textarea'}:
            for key in ['method', 'action', 'name', 'value', 'required', 'maxlength', 'aria-describedby']:
                attrs.pop(key, None)
        if self.source:
            for key in ['src', 'href', 'poster']:
                value = attrs.get(key)
                if not value or value.startswith(('#', '//')) or urlsplit(value).scheme:
                    continue
                path = re.split('[?#]', value)[0]
                suffix = value[len(path):]
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(self.source), path)) if not path.startswith('/') else path.lstrip('/')
                if resolved in ROUTES:
                    attrs[key] = ROUTES[resolved] + suffix
                elif (BASE.parent / resolved).is_file():
                    attrs[key] = '/static/frontend/' + resolved + suffix
        for key in ['src', 'href', 'poster']:
            if key in attrs:
                attrs[key] = unquote(attrs[key])
        self.tokens.append(('start', tag, sorted(attrs.items())))

    def handle_endtag(self, tag):
        if self.skipping:
            self.skipping -= 1
            return
        if tag not in VOID:
            self.tokens.append(('end', tag))

    def handle_data(self, data):
        if not self.skipping and data.strip():
            self.tokens.append(('text', re.sub(r'\s+', ' ', data).strip()))


def main():
    manifest = json.loads((BASE / 'docs/frontend-original-manifest.json').read_text())
    original_failures = []
    static_failures = []
    copied = 0
    for item in manifest:
        path = BASE.parent / item['path']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            original_failures.append(item['path'])
        static = BASE / 'static/frontend' / item['path']
        if static.is_file():
            copied += 1
            if hashlib.sha256(static.read_bytes()).hexdigest() != item['sha256']:
                static_failures.append(item['path'])
    pages = []
    client = Client()
    mapping = list(PAGES.items()) + [('contact', ('contact/', 'contact.html'))]
    for name, (route, source) in mapping:
        original = (BASE.parent / source).read_text(encoding='utf-8-sig')
        response = client.get('/' + route)
        rendered = response.content.decode()
        a, b = PageDOM(source), PageDOM()
        a.feed(original)
        b.feed(rendered)
        scripts_a = re.findall(r'<script\b[^>]*>([\s\S]*?)</script>', original)
        scripts_b = re.findall(r'<script\b[^>]*>([\s\S]*?)</script>', rendered)
        row = {'page': name, 'status': response.status_code, 'dom_equal': a.tokens == b.tokens, 'inline_js_equal': scripts_a == scripts_b}
        if not row['dom_equal']:
            for index, (left, right) in enumerate(zip(a.tokens, b.tokens)):
                if left != right:
                    row['first_difference'] = {'index': index, 'original': left, 'django': right}
                    break
            row['token_counts'] = [len(a.tokens), len(b.tokens)]
        pages.append(row)
    result = {'original_files_checked': len(manifest), 'original_changes': original_failures,
              'static_copies_checked': copied, 'static_changes': static_failures, 'pages': pages,
              'browser_pixel_comparison': 'not performed by this script'}
    (BASE / 'docs/frontend-verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    return int(bool(original_failures or static_failures or any(p['status'] != 200 or not p['dom_equal'] or not p['inline_js_equal'] for p in pages)))


if __name__ == '__main__':
    raise SystemExit(main())
