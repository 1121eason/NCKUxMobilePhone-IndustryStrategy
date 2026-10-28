#!/usr/bin/env python3
"""Check aggregate arithmetic, internal links and public-file boundaries."""
import json
import re
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise SystemExit('FAIL: ' + message)


def heading_ids(content):
    ids, seen = set(), {}
    for line in content.splitlines():
        if not re.match(r'^#{1,6} ', line):
            continue
        title = re.sub(r'^#{1,6} ', '', line).strip().lower()
        slug = re.sub(r'[^\w\-\s]', '', title, flags=re.UNICODE).replace(' ', '-')
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        ids.add(slug + (f'-{count}' if count else ''))
    return ids


data = json.loads((ROOT / 'data/published-summary.json').read_text())
n = data['sample']['projects']
require(sum(data['sample']['projects_by_year'].values()) == n, 'year counts do not sum to N')
require(sum(q['n'] for q in data['quadrants']) == n, 'group counts do not sum to N')
require(len({q['label'] for q in data['quadrants']}) == 4, 'group labels are not unique')
require(abs(sum(q['mean_PDP'] * q['n'] for q in data['quadrants']) / n) < .01,
        'rounded centered group scores are inconsistent with a near-zero overall mean')
anova = data['anova_reported']
require(anova['between_df'] + anova['within_df'] == n - 1, 'ANOVA degrees of freedom')
require(abs(anova['between_mean_square'] / anova['within_mean_square'] - anova['f']) < .02,
        'ANOVA rounded mean-square ratio is inconsistent with reported F')
for m in data['models']:
    k = len(m['terms'])
    adjusted = 1 - (1 - m['r2']) * (n - 1) / (n - k - 1)
    require(abs(adjusted - m['adjusted_r2']) < .001, f"{m['id']} adjusted R2 inconsistent with N and predictors")
    for term in m['terms'].values():
        require(term['standard_error'] > 0, 'non-positive standard error')
        require(term['stars'] in data['significance_legend'], 'unknown significance marker')

files = sorted(p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts
               and '__pycache__' not in p.parts and p.name != '.DS_Store')
for p in files:
    require(p.suffix.lower() not in {'.pdf', '.pptx', '.xlsx', '.zip'},
            f'Unreviewed source/binary in public folder: {p.relative_to(ROOT)}')
    require('private' not in p.relative_to(ROOT).parts, 'Private source in public tree')

links = 0
for p in ROOT.rglob('*.md'):
    content = p.read_text()
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', content):
        if '://' in target or target.startswith('mailto:'):
            continue
        file_part, _, fragment = unquote(target).partition('#')
        resolved = (p.parent / file_part).resolve() if file_part else p
        require(resolved.is_relative_to(ROOT), f'Link outside public root: {target}')
        require(resolved.exists(), f'Broken link in {p.name}: {target}')
        if fragment and resolved.suffix == '.md':
            require(fragment in heading_ids(resolved.read_text()), f'Broken section link: {target}')
        links += 1
    require('\x00' not in content and '\ufffd' not in content, f'Encoding artifact in {p.name}')
for p in (ROOT / 'assets').glob('*.svg'):
    root = ElementTree.parse(p).getroot()
    require(root.tag.endswith('svg'), f'Invalid SVG root: {p.name}')
    require(root.find('{http://www.w3.org/2000/svg}title') is not None, 'SVG has no accessible title')

print(f'PASS: N={n}; year/group totals; ANOVA rounding; 5 model summaries; {links} local links; {len(files)} reviewed public files')
print('Scope: consistency checks only. No raw-data regression, pairwise test, causal or business validation.')
