"""Check paired languages, local links, assets, anchors and program structure."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('index.html', 'Third.html', 'past.html', 'committee.html', 'contact.html', 'first.html', 'Second.html')

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set(); self.links = []; self.text = []; self.raw = 0
        self.language = None; self.alternates = {}; self.switches = []; self.counts = Counter()
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); self.counts[tag] += 1
        if tag in ('script', 'style'): self.raw += 1
        if tag == 'html': self.language = a.get('lang')
        if 'id' in a:
            assert a['id'] not in self.ids, ('Duplicate ID', a['id'])
            self.ids.add(a['id'])
        for k in ('src', 'href'):
            if k in a: self.links.append(a[k])
        for k in ('alt', 'aria-label', 'title'):
            if k in a: self.text.append(a[k])
        if tag == 'link' and 'hreflang' in a: self.alternates[a['hreflang']] = a['href']
        if 'data-language-link' in a: self.switches.append(a['href'])
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.raw -= 1
    def handle_data(self, data):
        if not self.raw: self.text.append(data)

pages = {p:Page(p.read_text()) for name in NAMES for p in (ROOT/name, ROOT/'en'/name)}
for path, page in pages.items():
    english = path.parent.name == 'en'
    assert page.language == ('en' if english else 'ja'), path
    assert set(page.alternates) == {'en', 'ja', 'x-default'}, path
    assert page.switches == [('../' if english else 'en/') + path.name], path
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc: continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        assert target.exists(), (path, link)
        if url.fragment and target in pages:
            assert url.fragment in pages[target].ids, (path, link)
    if english:
        # The Japanese-language selector intentionally reads 日本語.
        remaining = [t for t in page.text if re.search(r'[\u3040-\u30ff\u3400-\u9fff]', t.replace('日本語',''))]
        assert not remaining, (path, remaining)
    else:
        other = pages[ROOT/'en'/path.name]
        assert page.ids == other.ids, path
        for tag in ('table', 'tr', 'td', 'th', 'time', 'img'):
            assert page.counts[tag] == other.counts[tag], (path, tag)
        a = re.findall(r'\b\d{1,2}:\d{2}\b', path.read_text())
        b = re.findall(r'\b\d{1,2}:\d{2}\b', (ROOT/'en'/path.name).read_text())
        assert a == b, ('Program times differ', path)
assert len(ET.parse(ROOT/'sitemap.xml').getroot()) == 14
print('PASS: 14 pages; full text coverage; paired language links; all local assets and anchors; matching program structures and times; sitemap.')
