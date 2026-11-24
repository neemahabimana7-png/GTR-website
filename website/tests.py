import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from django.conf import settings
from django.contrib.staticfiles import finders
from django.test import SimpleTestCase
from django.urls import reverse
from .pages import PAGES


class PageIntegrationTests(SimpleTestCase):
    def test_every_public_page_renders(self):
        # Contact uses the database only on POST, so it can be checked here too.
        for name in PAGES:
            with self.subTest(page=name):
                response = self.client.get(reverse('website:' + name))
                self.assertEqual(response.status_code, 200)
                self.assertNotIn(b'{%', response.content)

    def test_contact_renders(self):
        self.assertEqual(self.client.get(reverse('inquiries:contact')).status_code, 200)

    def test_legacy_html_urls_redirect(self):
        for name, (_, source) in PAGES.items():
            with self.subTest(source=source):
                response = self.client.get('/' + source)
                self.assertRedirects(response, reverse('website:' + name), status_code=301, fetch_redirect_response=False)
        self.assertRedirects(self.client.get('/contact.html'), reverse('inquiries:contact'), status_code=301, fetch_redirect_response=False)

    def test_unknown_page_is_404(self):
        self.assertEqual(self.client.get('/services/not-a-service/').status_code, 404)

    def test_public_pages_reject_post(self):
        self.assertEqual(self.client.post('/').status_code, 405)

    def test_local_assets_and_links_resolve(self):
        from django.urls import resolve
        for name in list(PAGES) + ['contact']:
            url = reverse('inquiries:contact') if name == 'contact' else reverse('website:' + name)
            rendered = self.client.get(url).content.decode()
            rendered = re.sub(r'<!--[\s\S]*?-->', '', rendered)
            for ref in re.findall(r'(?:href|src)=["\']([^"\']+)["\']', rendered):
                if urlsplit(ref).scheme or urlsplit(ref).netloc:
                    continue
                path = unquote(urlsplit(ref).path)
                if path.startswith('/static/'):
                    with self.subTest(page=name, asset=path):
                        self.assertIsNotNone(finders.find(path.removeprefix('/static/')))
                elif path.startswith('/'):
                    with self.subTest(page=name, route=path):
                        self.assertIsNotNone(resolve(path))

    def test_copied_static_files_match_original_hashes(self):
        manifest = json.loads((settings.BASE_DIR / 'docs/frontend-original-manifest.json').read_text())
        for item in manifest:
            copied = settings.BASE_DIR / 'static/frontend' / item['path']
            if copied.is_file():
                with self.subTest(asset=item['path']):
                    self.assertEqual(hashlib.sha256(copied.read_bytes()).hexdigest(), item['sha256'])

    def test_original_files_are_still_unchanged(self):
        # This intentionally verifies the preservation requirement on this checkout.
        manifest = json.loads((settings.BASE_DIR / 'docs/frontend-original-manifest.json').read_text())
        root = settings.BASE_DIR.parent
        for item in manifest:
            path = root / item['path']
            with self.subTest(original=item['path']):
                self.assertTrue(path.is_file())
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item['sha256'])
