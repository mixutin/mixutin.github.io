"""Dependency-free validation of generated pages and their local references."""
import importlib.util
import json
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build', ROOT / 'tools/build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
PAGES = build.generate()
INHERITED = {
    'apple-touch-icon.png', '.well-known/security.txt',
    'assets/og/og-home.png', 'assets/og/og-home-fi.png',
    'projects/dauntless-revived/index.html', 'fi/projects/dauntless-revived/index.html',
    'blog/back-in-ctfs/index.html', 'fi/blog/back-in-ctfs/index.html',
}

class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

class SiteTests(unittest.TestCase):
    def test_generated_output_is_current(self):
        for path, html in PAGES.items():
            self.assertEqual((ROOT / path).read_text(encoding='utf-8'), html, path)

    def test_every_page_has_one_heading_and_language(self):
        for path, html in PAGES.items():
            if not path.endswith('.html'): continue
            parsed = Page(html)
            self.assertEqual(sum(tag == 'h1' for tag, _ in parsed.tags), 1, path)
            languages = [a.get('lang') for tag,a in parsed.tags if tag == 'html']
            self.assertEqual(languages, ['fi' if path.startswith('fi/') else 'en'])
            self.assertEqual(sum(a.get('id') == 'main' for _,a in parsed.tags), 1)

    def test_local_links_and_unique_ids(self):
        for path, html in PAGES.items():
            if not path.endswith('.html'): continue
            parsed = Page(html)
            ids = [a['id'] for _,a in parsed.tags if 'id' in a]
            self.assertEqual(len(ids), len(set(ids)), path)
            for tag, attrs in parsed.tags:
                raw = attrs.get('href', attrs.get('src', ''))
                url = urlparse(raw)
                if url.scheme or url.netloc or not raw: continue
                if raw.startswith('#'):
                    self.assertIn(url.fragment, ids, (path,raw))
                    continue
                self.assertTrue(raw.startswith('/'), (path, raw))
                target = url.path.lstrip('/')
                if not target or target.endswith('/'): target += 'index.html'
                self.assertTrue((ROOT / target).is_file() or target in INHERITED, (path, raw))

    def test_csp_and_progressive_enhancement(self):
        for path, html in PAGES.items():
            if not path.endswith('.html'): continue
            parsed = Page(html)
            self.assertIn("script-src 'self'", html)
            self.assertNotIn('unsafe-inline', html)
            self.assertNotIn('https://fonts.googleapis.com', html)
            for tag,attrs in parsed.tags:
                self.assertFalse(any(k.startswith('on') for k in attrs), (path,attrs))
                self.assertNotIn('style', attrs)
                if tag == 'script': self.assertTrue(attrs.get('src','').startswith('/assets/js/'))
            if path.endswith('projects/index.html'):
                self.assertIn('data-filter-controls hidden', html)
                cards = [a for _,a in parsed.tags if 'data-project' in a]
                self.assertEqual(len(cards), 5)
                self.assertTrue(all('hidden' not in a for a in cards))

    def test_public_project_provenance(self):
        data = json.loads((ROOT/'data/projects.json').read_text(encoding='utf-8'))
        self.assertEqual(len(data['projects']), 5)
        for project in data['projects']:
            self.assertTrue(project['source'].startswith('https://github.com/mixutin/'))
            self.assertEqual(set(project['description']), {'en','fi'})
            self.assertTrue(project['note']['en'])
        self.assertIn('does not run windows programs yet', next(p for p in data['projects'] if p['slug']=='mallow')['note']['en'].lower())

    def test_rankings_are_snapshots_not_fake_live_data(self):
        for path in ['ctf/index.html','fi/ctf/index.html','index.html','fi/index.html']:
            self.assertIn('Globally', PAGES[path])
            self.assertIn('In Finland', PAGES[path])
            self.assertIn('https://cryptohack.org/user/nurminen/', PAGES[path])
        self.assertIn('not a live ranking feed',PAGES['ctf/index.html'])

if __name__ == '__main__':
    unittest.main()
