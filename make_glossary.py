#!/usr/bin/env python3
"""Build Appendix_B_Glossary.md and course/moodle/Syriac_Glossary.xml from syriac_vocabulary.tsv."""
import csv, html, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ORDER = 'ܐܒܓܕܗܘܙܚܛܝܟܠܡܢܣܥܦܨܩܪܫܬ'
key = lambda r: [ORDER.index(c) if c in ORDER else 99 for c in r['Syriac']]
rows = [r for r in csv.DictReader(open('syriac_vocabulary.tsv'), delimiter='\t') if r['Syriac'].strip()]
rows.sort(key=key)
def gram(r):
    bits = [r['PartOfSpeech'], r['Gender'], r['Stem']]
    if r['Root']: bits.append('root ' + r['Root'])
    return ', '.join(b for b in bits if b)
out = ['### Appendix B: Syriac–English Glossary', '', '',
       f'All {len(rows)} words taught in Lessons 0–12, in Syriac alphabetical order. '
       'The last column gives the lesson where the word is introduced.', '']
cur = None
for r in rows:
    first = r['Syriac'][0]
    if first != cur:
        cur = first
        out += ['', f'#### {first}', '', '| Syriac | Transliteration | English | Grammar | L. |', '| :--- | :--- | :--- | :--- | :--- |']
    eng = r['English'].replace('|', '/').replace('\n', ' ')
    out.append(f"| {r['Syriac']} | {r['Transliteration']} | {eng} | {gram(r)} | {r['Lesson']} |")
open('Appendix_B_Glossary.md', 'w').write('\n'.join(out) + '\n')
os.makedirs('course/moodle', exist_ok=True)
x = ['<?xml version="1.0" encoding="UTF-8"?>', '<GLOSSARY><INFO><NAME>Syriac Vocabulary</NAME>',
     '<INTRO>Every word from Lessons 0–12 of The Acts of Mar Yukhannan.</INTRO><INTROFORMAT>1</INTROFORMAT>',
     '<ALLOWDUPLICATEDENTRIES>1</ALLOWDUPLICATEDENTRIES><DISPLAYFORMAT>dictionary</DISPLAYFORMAT>',
     '<SHOWSPECIAL>1</SHOWSPECIAL><SHOWALPHABET>1</SHOWALPHABET><SHOWALL>1</SHOWALL>',
     '<USEDYNALINK>0</USEDYNALINK><DEFAULTAPPROVAL>1</DEFAULTAPPROVAL><GLOBALGLOSSARY>0</GLOBALGLOSSARY>',
     '<ENTBYPAGE>20</ENTBYPAGE><ENTRIES>']
for r in rows:
    d = f"<p><i>{html.escape(r['Transliteration'])}</i> — {html.escape(r['English'])}</p><p>{html.escape(gram(r))}; Lesson {r['Lesson']}</p>"
    if r['Notes']: d += f"<p>{html.escape(r['Notes'])}</p>"
    x.append(f"<ENTRY><CONCEPT>{html.escape(r['Syriac'])}</CONCEPT><DEFINITION><![CDATA[{d}]]></DEFINITION>"
             f"<FORMAT>1</FORMAT><USEDYNALINK>0</USEDYNALINK><CASESENSITIVE>0</CASESENSITIVE><FULLMATCH>0</FULLMATCH><TEACHERENTRY>1</TEACHERENTRY>"
             f"<ALIASES><ALIAS><NAME>{html.escape(r['Transliteration'])}</NAME></ALIAS></ALIASES></ENTRY>")
x.append('</ENTRIES></INFO></GLOSSARY>')
open('course/moodle/Syriac_Glossary.xml', 'w').write('\n'.join(x))
print(len(rows), 'entries')
