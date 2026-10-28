#!/usr/bin/env python3
"""Build deterministic SVG figures from the published aggregate summaries."""
import argparse
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT = "system-ui, -apple-system, 'Noto Sans', sans-serif"


def text(x, y, content, size=20, fill="#172f42", weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{escape(str(content))}</text>')


def svg(title, desc, body, height):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" '
            f'viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">\n'
            f'<title id="title">{escape(title)}</title>\n<desc id="desc">{escape(desc)}</desc>\n'
            f'<rect width="1200" height="{height}" rx="18" fill="#f5f8fa"/>\n'
            f'<g font-family="{FONT}">\n' + "\n".join(body) + '\n</g>\n</svg>\n')


def competition_map():
    body = [
        text(48, 45, "INDUSTRY COMPETITION & STRATEGY", 16, "#337d80", 700),
        text(48, 91, "Who controls knowledge, decisions and value?", 34, weight=700),
        text(48, 125, "Historical mobile phone case | Research projects: 2012-2014", 18, "#526b7a"),
        '<rect x="345" y="160" width="510" height="135" rx="14" fill="#193e53"/>',
        text(600, 201, "PLATFORM PROVIDERS", 24, "white", 700, "middle"),
        text(600, 236, "Core components + architecture knowledge", 20, "#d7eaed", anchor="middle"),
        text(600, 267, "Road maps | Reference designs | Technical support", 17, "#d7eaed", anchor="middle"),
        '<path d="M440 295 L300 352 M760 295 L900 352" stroke="#739ca9" stroke-width="3" fill="none"/>',
        '<path d="M303 338 L300 352 L315 350 M885 350 L900 352 L897 338" stroke="#739ca9" stroke-width="3" fill="none"/>',
        '<rect x="48" y="365" width="500" height="166" rx="14" fill="white" stroke="#ccdbe2"/>',
        '<rect x="652" y="365" width="500" height="166" rx="14" fill="white" stroke="#ccdbe2"/>',
        text(76, 408, "BRAND FIRMS", 24, weight=700),
        text(76, 445, "Customer needs + core component knowledge", 18),
        text(76, 478, "Define concepts, functions and key trade-offs", 18),
        text(76, 510, "Strategic focus: differentiated product definition", 17, "#337d80", 600),
        text(680, 408, "CONTRACT MANUFACTURERS", 24, weight=700),
        text(680, 445, "Architecture + integration + implementation", 18),
        text(680, 478, "Connect components, test and solve problems", 18),
        text(680, 510, "Strategic focus: value-added development services", 17, "#337d80", 600),
        '<path d="M556 446 H644" stroke="#337d80" stroke-width="3"/>',
        '<path d="M568 438 L556 446 L568 454 M632 438 L644 446 L632 454" stroke="#337d80" stroke-width="3" fill="none"/>',
        '<rect x="48" y="564" width="1104" height="112" rx="14" fill="#e2efed"/>',
        text(76, 602, "GOVERNANCE SUPPORTS SPECIALIZATION", 19, "#245d60", 700),
        text(76, 635, "Early problem solving + clear decision rights + change control + ongoing communication", 20),
        text(48, 714, "Source: Shiu & Yasumoto (2018), pp. 374-382, 390-391. Diagram: new case synthesis.", 16, "#526b7a"),
        text(48, 741, "Strategic outcomes and actions shown here are interpretations; no intervention effects were measured.", 16, "#526b7a"),
    ]
    return svg("Platform knowledge and industry strategy", "A triadic knowledge relationship links platform providers, brands and contract manufacturers. Governance supports specialization.", body, 770)


def published_performance(data):
    body = [
        text(48, 45, "PUBLISHED EVIDENCE | 50 PROJECTS", 16, "#337d80", 700),
        text(48, 91, "Decision rights and product development performance", 31, weight=700),
        text(48, 126, "Group means of centered PDP scores; these values are not percentages.", 20, "#526b7a"),
        text(48, 168, "Source group / relative decision rights", 17, "#526b7a"),
    ]
    origin, scale = 820, 350
    for tick in [-.8, -.6, -.4, -.2, 0, .2, .4, .6]:
        x = origin + tick * scale
        body.append(f'<line x1="{x}" x2="{x}" y1="198" y2="528" stroke="{"#6b8390" if tick == 0 else "#dbe4e9"}"/>')
        body.append(text(x, 558, f"{tick:.1f}", 16, "#526b7a", anchor="middle"))
    for i, q in enumerate(data['quadrants']):
        y, mean = 227 + i * 85, q['mean_PDP']
        label = f"{q['label']} | Brand CDR {q['brand_CDR']} / Mfr IDR {q['manufacturer_IDR']}"
        body.append(text(48, y - 6, label, 18, weight=600))
        body.append(text(48, y + 21, f"n = {q['n']} | SD = {q['sd_PDP']:.2f}", 17, "#526b7a"))
        x, width = min(origin, origin + mean * scale), abs(mean * scale)
        color = '#276f73' if mean >= 0 else '#ac6962'
        body.append(f'<rect x="{x:.2f}" y="{y-24}" width="{width:.2f}" height="42" rx="5" fill="{color}"/>')
        tx, anchor = (origin + mean * scale + 12, 'start') if mean >= 0 else (origin + mean * scale - 12, 'end')
        body.append(text(round(tx, 2), y + 4, f"{mean:+.2f}", 21, color, 700, anchor))
    body.extend([
        '<rect x="48" y="595" width="1104" height="105" rx="12" fill="#e8eff3"/>',
        text(72, 630, "Interpretation", 19, weight=700),
        text(72, 662, "Group II has the highest mean. Omnibus ANOVA does not establish II > I in a pairwise test.", 19),
        text(48, 740, "Source: Shiu & Yasumoto (2018), Fig. 3 and footnote 6, pp. 387-388. Projects: 2012-2014.", 16, "#526b7a"),
        text(48, 768, "Redrawn from published aggregates. No individual project observations or confidence intervals are shown.", 16, "#526b7a"),
    ])
    return svg("Published performance by decision-rights group", "Group I n=16 mean=0.31; II n=11 mean=0.38; III n=9 mean=-0.62; IV n=14 mean=-0.26. Descriptive comparisons only.", body, 800)


def outputs():
    data = json.loads((ROOT / 'data/published-summary.json').read_text())
    return {'competition-map.svg': competition_map(),
            'published-performance.svg': published_performance(data)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check without changing files')
    args = parser.parse_args()
    for name, content in outputs().items():
        target = ROOT / 'assets' / name
        if args.check:
            if not target.exists() or target.read_text() != content:
                raise SystemExit(f'Figure differs from source: {name}')
        else:
            target.write_text(content)
    print('PASS: 2 deterministic SVG figures' if args.check else 'Built 2 SVG figures')
