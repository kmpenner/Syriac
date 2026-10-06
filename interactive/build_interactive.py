#!/usr/bin/env python3
"""Build the interactive lessons: textbook Markdown + authored checks -> Moodle XML.

Every textbook section becomes one or more content slides (pandoc HTML, the
same text as the PDF). The Exercises and Answer Key sections are replaced by
learning checks from checks/Lesson_NN.json, which cover the same drills with
the answer-key answers, so the quizzes can stand in for the textbook.

checks/Lesson_NN.json:
  [{"after": 1, "q": "...", "opts": [["correct", "feedback"], ["wrong", "feedback"], ...],
    "explain": "general feedback"}]
The first option is correct; the player shuffles. "after" is the textbook
section number the check follows.

Output: xml/Lesson_NN.xml, played by player.html?xml=xml/Lesson_NN.xml
(player.html is a copy of shared/moodle-lesson-player/index.html).
"""
import glob, html, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PLAYER = os.path.join(ROOT, '..', 'shared', 'moodle-lesson-player', 'index.html')
MODULES = [  # (module title, lesson numbers)
    ('Module 1 · Foundations: Script, Nouns and the Basic Verb', [0, 1, 2, 3, 4]),
    ('Module 2 · The Verbal System: Derived Stems, Weak Roots, Future', [5, 6, 7, 8]),
    ('Module 3 · Advanced Syntax: Commands, Passives, Suffixes, Clauses', [9, 10, 11, 12]),
]
MODULE_OF = {n: i + 1 for i, (_, ls) in enumerate(MODULES) for n in ls}
SKIP = re.compile(r'Exercises|Answer Key', re.I)
MAX_SLIDE = 5000  # characters of HTML before a section is split


def md2html(md):
    out = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'html5', '--no-highlight'],
                         input=md, capture_output=True, text=True, check=True).stdout
    return re.sub(r'(<table.*?</table>)', r'<div class="tablewrap">\1</div>', out, flags=re.S)


def split_html(h):
    """Split a long section at top-level blocks, preferring bold-label paragraphs."""
    blocks = re.split(r'\n(?=<(?:p|h\d|div|table|ol|ul|blockquote|hr)\b)', h)
    slides, cur = [], ''
    for b in blocks:
        heading = b.startswith('<p><strong>') or b.startswith('<h')
        if cur and len(cur) + len(b) > MAX_SLIDE and (heading or len(cur) > MAX_SLIDE * 1.4):
            slides.append(cur); cur = ''
        cur += b + '\n'
    if cur.strip():
        slides.append(cur)
    return slides


def cdata(s):
    return '<![CDATA[' + s.replace(']]>', ']]]]><![CDATA[>') + ']]>'


def desc(name, body):
    return (f'<question type="description"><name><text>{html.escape(name)}</text></name>'
            f'<questiontext format="html"><text>{cdata(body)}</text></questiontext></question>\n')


def mcq(name, c):
    ans = ''.join(
        f'<answer fraction="{100 if i == 0 else 0}" format="html"><text>{cdata(t)}</text>'
        f'<feedback format="html"><text>{cdata(fb)}</text></feedback></answer>'
        for i, (t, fb) in enumerate(c['opts']))
    return (f'<question type="multichoice"><name><text>{html.escape(name)}</text></name>'
            f'<questiontext format="html"><text>{cdata(c["q"])}</text></questiontext>'
            f'<generalfeedback format="html"><text>{cdata(c.get("explain", ""))}</text></generalfeedback>'
            f'<single>true</single><shuffleanswers>true</shuffleanswers>{ans}</question>\n')


def build(md_path):
    num = int(re.search(r'Lesson_(\d+)', md_path).group(1))
    mod = MODULE_OF[num]
    src = open(md_path).read()
    title = re.search(r'^### (.+)$', src, re.M).group(1).strip()
    parts = re.split(r'^#### ', src, flags=re.M)
    checks_path = os.path.join(HERE, 'checks', f'Lesson_{num:02d}.json')
    checks = json.load(open(checks_path)) if os.path.exists(checks_path) else []
    tag = f'Module {mod} · Lesson {num}'
    intro = md2html(re.sub(r'^##+ .*$', '', parts[0], flags=re.M))
    out = [desc(tag, f'<h3><strong>{html.escape(title)}</strong></h3>\n{intro}')]
    used = set()
    nq = 0
    for p in parts[1:]:
        head, _, body = p.partition('\n')
        m = re.match(r'Section (\d+)', head)
        sec = int(m.group(1)) if m else None
        if not SKIP.search(head):
            slides = split_html(md2html(body))
            for i, h in enumerate(slides):
                cont = ' (continued)' if i else ''
                out.append(desc(f'{tag} · {head.strip()}{cont}',
                                f'<h3>{html.escape(head.strip())}{cont}</h3>\n{h}'))
        for k, c in enumerate(checks):
            if c['after'] == sec and k not in used:
                used.add(k); nq += 1
                out.append(mcq(f'{tag} · Check {nq}', c))
    missing = [k for k in range(len(checks)) if k not in used]
    if missing:
        sys.exit(f'{md_path}: checks {missing} name a section that does not exist')
    os.makedirs(os.path.join(HERE, 'xml'), exist_ok=True)
    dest = os.path.join(HERE, 'xml', f'Lesson_{num:02d}.xml')
    open(dest, 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n' + ''.join(out) + '</quiz>\n')
    return num, title, len(out) - nq, nq


def main():
    mds = sorted(glob.glob(os.path.join(ROOT, 'Lesson_[0-9][0-9]_*.md')))
    if len(sys.argv) > 1:
        mds = [m for m in mds if any(a in m for a in sys.argv[1:])]
    info = {}
    for m in mds:
        n, t, s, q = build(m)
        info[n] = t
        print(f'✓ Lesson {n:2d}: {s} slides, {q} checks')
    shutil.copy(PLAYER, os.path.join(HERE, 'player.html'))
    titles = {int(re.search(r'Lesson_(\d+)', m).group(1)): re.search(r'^### (.+)$', open(m).read(), re.M).group(1)
              for m in glob.glob(os.path.join(ROOT, 'Lesson_[0-9][0-9]_*.md'))}
    rows = ''.join(
        f'<h2>{html.escape(mt)}</h2><ol start="{ls[0]}">' + ''.join(
            f'<li value="{n}"><a href="player.html?xml=xml/Lesson_{n:02d}.xml">Lesson {n}: {html.escape(titles[n])}</a></li>'
            for n in ls) + '</ol>' for mt, ls in MODULES)
    open(os.path.join(HERE, 'index.html'), 'w').write(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Syriac Interactive Lessons</title>
<style>:root{{--bg:#f4f1ea;--ink:#2a2320;--accent:#7c3a1e}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1d1916;--ink:#eee5d8;--accent:#e0a47f}}}}
body{{background:var(--bg);color:var(--ink);font-family:Georgia,serif;max-width:760px;margin:0 auto;padding:24px 16px;line-height:1.6}}
h1,h2{{color:var(--accent)}} h2{{font-size:1.15rem;margin-top:1.6em}} a{{color:inherit}}</style></head>
<body><h1>The Acts of Mar Yukhannan</h1><p>Interactive lessons in Classical Syriac. Each lesson contains the full
textbook text, with learning checks in place of the exercises.</p>{rows}</body></html>
''')


if __name__ == '__main__':
    main()
