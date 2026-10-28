"""Render the public policy from the same JSON bundled in CalyxRandom."""
from pathlib import Path
import html
import json

root = Path(__file__).resolve().parents[1]
source = root / 'privacy/calyx-random/policy.json'
policy = json.loads(source.read_text(encoding='utf-8'))
escape = html.escape
sections = []
for locale, copy in policy['localizations'].items():
    body = ''.join('<section><h3>' + escape(item['heading']) + '</h3><p>' +
                   escape(item['text']) + '</p></section>' for item in copy['sections'])
    label = {'en': 'English', 'pt': 'Português (Brasil)', 'es': 'Español', 'id': 'Bahasa Indonesia'}[locale]
    sections.append('<details lang="' + locale + '" id="' + locale + '"' +
                    (' open' if locale == 'en' else '') + '><summary>' + escape(label) +
                    '</summary><h2>' + escape(copy['title']) + '</h2>' + body + '</details>')
page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Privacy Policy — CalyxRandom</title><meta name="description" content="CalyxRandom privacy policy: local lists and results, advertising, privacy choices, retention and deletion.">
<link rel="canonical" href="https://calyxharbor.com/privacy/calyx-random/">
<style>body{font:16px/1.7 system-ui,sans-serif;color:#1a2929;background:#f7faf9;max-width:800px;margin:auto;padding:32px 20px 64px}a{color:#0e6e6e}h1{font-size:2rem;line-height:1.2}h2{font-size:1.4rem}h3{font-size:1.08rem;margin-top:28px}p{overflow-wrap:anywhere}details{background:white;border:1px solid #d6e3df;padding:18px 22px;margin:16px 0;border-radius:12px}summary{cursor:pointer;font-weight:600;min-height:36px}.meta{color:#526463;font-size:.9rem}nav{display:flex;gap:20px;flex-wrap:wrap}footer{border-top:1px solid #d6e3df;padding-top:24px;margin-top:32px}@media(max-width:420px){body{padding:24px 14px}details{padding:14px}}</style></head><body>
<nav><a href="/">Cold Harbor of Calyx</a><a href="/privacy/">All privacy policies</a></nav>
<h1>CalyxRandom Privacy Policy</h1><p class="meta">Version ''' + policy['version'] + ' · Effective date: ' + policy['effectiveDate'] + '''<br>Android app: com.calyxharbor.calyxrandom</p>
<p>Your lists and results stay on your device. Advertising and consent services may process device data. Choose a language to read the complete policy.</p>
''' + ''.join(sections) + '''<footer>Privacy contact: <a href="mailto:support@calyxharbor.com">support@calyxharbor.com</a><br>Cold Harbor of Calyx (Yangzhou) Network Technology Co., Ltd.</footer></body></html>
'''
(source.parent / 'index.html').write_text(page, encoding='utf-8')
print('Rendered CalyxRandom policy: 4 languages, 7 sections each')
