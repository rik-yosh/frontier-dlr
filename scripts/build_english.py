"""Regenerate the English site from Japanese pages and translations/en.json.
Run from any directory with Python 3. No external dependencies are required.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit, quote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = ('index.html', 'Third.html', 'past.html', 'committee.html', 'contact.html', 'first.html', 'Second.html')
BASE = 'https://rik-yosh.github.io/frontier-dlr/'
TRANSLATIONS = json.loads((ROOT / 'translations/en.json').read_text())
JAPANESE = re.compile(r'[\u3040-\u30ff\u3400-\u9fff]')

def translate(value):
    key = ' '.join(value.split())
    if key in TRANSLATIONS:
        return TRANSLATIONS[key]
    if JAPANESE.search(key):
        raise ValueError('Missing English translation: ' + key)
    return value.replace('。', '.').replace(' ／ ', ' / ')

class EnglishPage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []
        self.raw = 0
    def handle_decl(self, data):
        self.output.append('<!' + data + '>')
    def handle_comment(self, data):
        # Source comments are for maintainers, not part of the translation.
        pass
    def handle_starttag(self, tag, attrs):
        self.start(tag, attrs, False)
    def handle_startendtag(self, tag, attrs):
        self.start(tag, attrs, True)
    def start(self, tag, attrs, closed):
        if tag in ('script', 'style'):
            self.raw += 1
        converted = []
        for key, value in attrs:
            if value is None:
                converted.append(key)
                continue
            if key in ('alt', 'title', 'aria-label', 'content'):
                value = translate(value)
            if tag == 'html' and key == 'lang':
                value = 'en'
            if key in ('src', 'href'):
                url = urlsplit(value)
                if not url.scheme and not url.netloc and url.path and not value.startswith('#'):
                    if url.path not in PAGES:
                        value = '../' + value
                if tag == 'iframe':
                    value = value.replace('!1sja!2sjp', '!1sen!2sjp')
                    value = quote(value, safe=':/?=&!%+,-_.~')
            converted.append(key + '="' + escape(value, quote=True) + '"')
        self.output.append('<' + tag + (' ' if converted else '') + ' '.join(converted) + (' /' if closed else '') + '>')
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.raw -= 1
        self.output.append('</' + tag + '>')
    def handle_data(self, data):
        if self.raw or not data.strip():
            self.output.append(data)
        else:
            lead = data[:len(data) - len(data.lstrip())]
            tail = data[len(data.rstrip()):]
            self.output.append(lead + escape(translate(data.strip()), quote=False) + tail)
    def handle_entityref(self, name):
        self.output.append('&' + name + ';')
    def handle_charref(self, name):
        self.output.append('&#' + name + ';')

def language_switch(name, english):
    ja = ('../' if english else '') + name
    en = ('' if english else 'en/') + name
    return ('<nav class="language-switch" aria-label="' + ('Language' if english else '言語') + '">'
            '<a href="' + ja + '" lang="ja" hreflang="ja"' + (' data-language-link' if english else ' aria-current="true"') + '>日本語</a>'
            '<span aria-hidden="true">/</span>'
            '<a href="' + en + '" lang="en" hreflang="en"' + (' aria-current="true"' if english else ' data-language-link') + '>English</a></nav>')

def metadata(name, english):
    ja = BASE + ('' if name == 'index.html' else name)
    en = BASE + 'en/' + ('' if name == 'index.html' else name)
    return ('  <link rel="canonical" href="' + (en if english else ja) + '">\n'
            '  <link rel="alternate" hreflang="ja" href="' + ja + '">\n'
            '  <link rel="alternate" hreflang="en" href="' + en + '">\n'
            '  <link rel="alternate" hreflang="x-default" href="' + ja + '">\n')

(ROOT / 'en').mkdir(exist_ok=True)
for name in PAGES:
    path = ROOT / name
    source = path.read_text()
    source = re.sub(r'\s*<link rel="canonical"[^>]*>', '', source)
    source = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*"[^>]*>', '', source)
    source = re.sub(r'\s*<nav class="language-switch".*?</nav>', '', source, flags=re.S)
    # Remove generated additions before rebuilding; repeated runs are stable.
    source = re.sub(r'\s*<script src="(?:\.\./)?js/language.js"></script>', '', source)
    parser = EnglishPage()
    parser.feed(source)
    english = ''.join(parser.output)
    english = english.replace('</head>', metadata(name, True) + '</head>')
    english = english.replace('    </header>', '      ' + language_switch(name, True) + '\n    </header>')
    english = english.replace('</body>', '  <script src="../js/language.js"></script>\n</body>')
    # English headings need no duplicate translated Japanese subtitle.
    english = re.sub(r'<span class="hosoku">.*?</span>', '', english)
    english = english.replace('>Sponsors</span>', '>Co-organizers</span>')
    english = english.replace('《Web Design:Template-Party》', 'Web Design: Template-Party')
    # Natural sentence order where the Japanese source spans multiple links.
    english = english.replace('The meeting details</a> are available in ', 'Meeting details</a> are available in ')
    source = source.replace('</head>', metadata(name, False) + '</head>')
    source = source.replace('    </header>', '      ' + language_switch(name, False) + '\n    </header>')
    source = source.replace('</body>', '  <script src="js/language.js"></script>\n</body>')
    path.write_text(source)
    (ROOT / 'en' / name).write_text('\n'.join(line.rstrip() for line in english.splitlines()) + '\n')

urls = [BASE + prefix + ('' if name == 'index.html' else name) for prefix in ('', 'en/') for name in PAGES]
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>' + url + '</loc></url>\n' for url in urls) + '</urlset>\n')
print('Generated all 7 English pages and paired language links.')
