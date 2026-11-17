# NEXT — Syriac

**Updated 2026-11-17 by Claude** after the November audit and its fixes.
Settled decisions and conventions are in `LEDGER.md`; the audit findings are in
`REVIEW_2026-11-16.md`. Older audit notes (October) are in git history.

## State

- All 13 lessons, Appendix A, the interactive checks and `syriac_vocabulary.tsv`
  (420 entries) are corrected per `REVIEW_2026-11-16.md`. The full pipeline rebuilds
  clean: table lint passes, `Syriac_Textbook.pdf` is 223 pages.
- Stem names: Ethpeel / Ethpaal / Ettaphal. Silent letters in parentheses
  (`ktab(w)`, `malk(y)`), predicate adjectives in the absolute, syāmē on plurals.
- Tests and final exam: `course/make_assessments.py` (rewritten 2026-11-17) builds
  `course/moodle/{Module1_Test,Module2_Test,Final_Exam}.xml` and `course/*_Key.md`.
  These files are gitignored on purpose (public repo) and travel only by Syncthing;
  keep a private backup, since the previous generator was lost that way.
- Flash Pro: the corrected deck is live (kmpenner/flash-pro commit bf6cb8b). Card ids
  are stable hashes. Browsers that loaded the October copy keep it until the deck is
  deleted and reloaded in Flash Pro.
- Syriac repo commits from 2026-11-17 are local only; the GitHub Pages site
  (https://kmpenner.github.io/Syriac/) still shows the pre-audit build until `/stand` pushes.

## Next (decisions for Ken)

1. Course number (still RELS 4XX) and the Moodle shell. The StFX calendar shows 499
   Directed Study in other departments, but that is for individual students; ask the
   Registrar or department which number to run this under.
2. Confirm the course weights 10/10/15/25/40 (syllabus and ledger agree; RELS 114
   uses 20/20/25/35 for comparison).
3. Weekly vocabulary quizzes (10%, lowest two dropped) are promised in the syllabus
   but no bank exists. Pick a format (suggested: 10 items per lesson from the TSV,
   Syriac to English) and the generator can be written.
4. Audio: Ken records it; SEDRA has no pronunciation audio.
5. Proofreading by a strong reader of Syriac is still worth doing. Some forms added
   in November rest on grammar, not SEDRA (the ʾalbeš paradigm, malk- with plural
   suffixes, ktabūn, ʾassān(y)).

## Rebuild after any lesson or TSV edit

```bash
python3 make_glossary.py
python3 make_flashpro.py
python3 interactive/build_interactive.py
python3 course/make_assessments.py
python3 make_site.py
bash build.sh
```

`bash build.sh Lesson_05` rebuilds one lesson plus the textbook. When a key answer
changes, update `interactive/checks/Lesson_NN.json` too. The TSV has CRLF line endings;
read and write it with `newline=''`.

## Interactive version

`interactive/` holds the Moodle-XML lessons, grouped into Module 1 (L0–4), Module 2
(L5–8) and Module 3 (L9–12). Checks live in `interactive/checks/Lesson_NN.json`, keyed
by `"after": <section number>`; renumbering a lesson's sections means shifting these.
Preview with `cd interactive && python3 -m http.server`, then open `index.html`.

## Checking Syriac forms (for agents)

- SEDRA: `curl -s "https://sedra.bethmardutho.org/api/word/<unvocalized Syriac>.json"`
  (200 = attested, 404 = not listed). SEDRA often lacks prefixed forms (w-, d-, l-),
  so check the bare form too.
- Bulk `str.replace` on paradigm forms: replace longest forms first (ʾeštadar is a
  prefix of ʾeštadart).

## Web site and flashcards

- GitHub Pages: https://kmpenner.github.io/Syriac/ (main, root). `python3 make_site.py`
  rewrites `index.html`.
- Flash Pro: after any TSV change, copy `flashpro/syriac_yukhannan.json` to kmpenner/flash-pro
  `data/` and update `totalCards` in both `data/catalog.json` and `data/catalog-data.js`.
  Deep link: `https://kmpenner.github.io/flash-pro/?deck=deck_syriac_yukhannan&bundle=Lesson%203:`
