#!/usr/bin/env python3
"""Write index.html, the GitHub Pages home (https://kmpenner.github.io/Syriac/).

Links each lesson's web text, interactive version, PDF and Flash Pro bundle.
Run after build.sh and interactive/build_interactive.py.
"""
import glob, html, os, re, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
FLASH = 'https://kmpenner.github.io/flash-pro/?deck=deck_syriac_yukhannan'
MODULES = [('Module 1 · Foundations: Script, Nouns and the Basic Verb', range(0, 5)),
           ('Module 2 · The Verbal System: Derived Stems, Weak Roots, Future', range(5, 9)),
           ('Module 3 · Advanced Syntax: Commands, Passives, Suffixes, Clauses', range(9, 13))]

lessons = {}
for md in glob.glob(os.path.join(HERE, 'Lesson_[0-9][0-9]_*.md')):
    n = int(re.search(r'Lesson_(\d+)', md).group(1))
    lessons[n] = (os.path.basename(md)[:-3], re.search(r'^### (.+)$', open(md).read(), re.M).group(1).strip())


def row(n):
    stem, title = lessons[n]
    cards = FLASH + '&bundle=' + urllib.parse.quote(f'Lesson {n}:')
    return (f'<tr><td class="n">{n}</td><td><a href="{stem}.html">{html.escape(title)}</a></td>'
            f'<td><a href="interactive/player.html?xml=xml/Lesson_{n:02d}.xml">Interactive</a></td>'
            f'<td><a href="{stem}.pdf">PDF</a></td><td><a href="{cards}">Flashcards</a></td></tr>')


body = ''.join(f'<h2>{html.escape(t)}</h2><table>{"".join(row(n) for n in ns)}</table>' for t, ns in MODULES)
open(os.path.join(HERE, 'index.html'), 'w').write(f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Classical Syriac Lessons</title>
<meta name="description" content="The Acts of Mar Yukhannan: an introduction to Classical Syriac in 13 lessons.">
<style>:root{{--bg:#f4f1ea;--ink:#2a2320;--accent:#7c3a1e;--rule:#d8cfc0}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1d1916;--ink:#eee5d8;--accent:#e0a47f;--rule:#3a332d}}}}
body{{background:var(--bg);color:var(--ink);font-family:Georgia,serif;max-width:860px;margin:0 auto;padding:24px 16px;line-height:1.5}}
h1,h2{{color:var(--accent)}} h2{{font-size:1.1rem;margin-top:1.8em}} a{{color:inherit}}
table{{width:100%;border-collapse:collapse}} td{{padding:6px 8px;border-bottom:1px solid var(--rule);vertical-align:top}}
td.n{{width:2em;color:var(--accent);font-weight:bold}} td:nth-child(n+3){{white-space:nowrap;font-size:.9em}}
.links a{{display:inline-block;margin:0 1.2em .4em 0}}
@media (max-width:600px){{td:nth-child(n+3){{display:block;padding:0 8px 6px 2.6em;border:0}} tr{{display:block;border-bottom:1px solid var(--rule)}} td{{border:0}}}}</style></head>
<body><h1>The Acts of Mar Yukhannan</h1>
<p>An introduction to Classical Syriac. A connected story, told in Syriac, runs through thirteen lessons and
carries the grammar from the alphabet to verbal suffixes.</p>
<p class="links"><a href="Syriac_Textbook.pdf">Whole textbook (PDF)</a><a href="Appendix_A_Paradigms.html">Paradigms</a><a href="Appendix_B_Glossary.html">Glossary</a><a href="interactive/index.html">Interactive lessons</a><a href="{FLASH}">All vocabulary in Flash Pro</a></p>
{body}
<p style="margin-top:2em;font-size:.9em">Flash Pro cards come from <code>syriac_vocabulary.tsv</code> (419 words), one bundle per lesson.
Word lookups: <a href="https://sedra.bethmardutho.org/">SEDRA</a>.</p>
</body></html>
''')
print('index.html written')
