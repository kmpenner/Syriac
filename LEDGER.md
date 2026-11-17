# Work Ledger: Syriac Textbook (The Acts of Mar Yukhannan)

> **Governance Principle (AutomatED Work Ledger / TRACER Protocol):**
> Agents must read this file before acting. Do not reopen settled decisions without explicit user instruction. Do not unilaterally resolve open questions. Check changes against the verification gate before committing.

---

## 1. Source Hierarchy & Authority

1. **Top Authority & Lessons Source:** `Lesson_00_The_Alphabet.md` through `Lesson_12_Fringes_Of_Syntax.md` (all 13 lessons standardized on GFM pipe tables with chapter art)
2. **Vocabulary Single Source of Truth:** `syriac_vocabulary.tsv` (420 entries, SEDRA-verified lemmas and stems)
3. **Interactive Learning Checks:** `interactive/checks/Lesson_NN.json`
4. **Compiled Production Artifacts:**
   - PDF Master: `Syriac_Textbook.pdf` (223 pages)
   - Interactive XML: `interactive/xml/Lesson_NN.xml`
   - Glossary: `Appendix_B_Glossary.md`, `course/moodle/Syriac_Glossary.xml`
   - Flash Pro Deck: `flashpro/syriac_yukhannan.json`
5. **Build Scripts:** `./build.sh` (with table cell-count lint check), `make_glossary.py`, `make_flashpro.py`, `interactive/build_interactive.py`, `course/make_assessments.py`, `make_site.py`

---

## 2. Settled Decisions (Locked Baseline)

- **[2026-10-06] Exercise Item Numbering**: All lesson exercises and their corresponding Answer Key sections reset to `1..N` per exercise. Continuous numbering across exercises within a lesson is prohibited.
- **[2026-10-06] Supplementary Vocabulary Deduping**: Section 11 tables must contain only genuine lesson-specific vocabulary. Do not copy Lesson 1 vocabulary into other lessons.
- **[2026-10-06] Attested Classical Syriac Only**: All vocabulary entries must be verified against Beth Mardutho SEDRA API (`sedra.bethmardutho.org`). Synthetic formations ending in `-ūttā` or `-ānā` without textual attestation are strictly barred.
- **[2026-10-06] TSV Citation Lemmas**: The `Syriac` column in `syriac_vocabulary.tsv` contains only single citation forms. Slashes (e.g. `ܒܪ / ܒܪܐ`) are prohibited; construct and absolute forms are noted in `Notes`.
- **[2026-10-06] Character Rendering**: Estrangela script set with Noto Sans Syriac. Academic transliteration for grammar/paradigms (`š`, `ṭ`, `ḥ`, `Yūḥannan`); "Yukhannan" in English prose.
- **[2026-10-21] Table Format**: All tables across all 13 lessons are standardized as GitHub-Flavored Markdown (GFM) pipe tables (`| col | col |`). Fragile space-aligned Pandoc multiline tables are deprecated. Enforced by automated cell-count lint check in `./build.sh`.
- **[2026-10-21] Classical Morphology & Grammar Realignment**:
  - Abstract nouns in `-ūtā` (not `-ūttā`).
  - Model Aphel verb in Lesson 5 changed to `ʾaqreb` / `maqreb` (Peal `qreb` "draw near" -> Aphel "bring near, offer"); `ʾallep` / `mallep` correctly treated as I-Alaph Paael in Lesson 6. Non-existent `*yallep` and `*ʾetyallap` removed.
  - Aphel "he gave life" vocalized `ʾaḥī` (not `ʾaḥyī`); Aphel "he revealed" spelled `ܐܓܠܝ` (*ʾaglī*).
  - Masculine singular construct of `malkā` is `melek` (bound stem before suffixes: `malk-`).
  - Guards in gate scenes designated `nāṭōrē` (not `qašīšē`).
  - Verbal suffixes aligned with Classical Syriac: unmarked pronominal object on verbs; 3rd person plural objects use enclitic `qṭal ʾennōn` / `qṭal ʾennēn` (not non-classical `*qṭalhūn`). Imperatives with 1st person object suffix use `-aynī` (`ʾassaynī`, `pruqaynī`).
- **[2026-11-17] Follow-up fixes**: Stem names are Ethpeel / Ethpaal / Ettaphal everywhere (Etpaael retired). L4 story ends with Sentence 10 *w-ʿal Yūḥannan l-mdīttā* ("entered the city"), bridging to the L5 preaching scene; ʿal added to the TSV (L4). L9 and L10 warm-ups use the same numbered-list format as the other lessons, with answers in Section 9. `course/make_assessments.py` (new) builds `course/moodle/{Module1_Test,Module2_Test,Final_Exam}.xml` and `course/*_Key.md`: MC items drawn from the lesson checks that pass the 0.85-1.15 distractor gate and stand alone without the story, no item reused between tests, key position rotated A-D; translation passages are hand-written in the script with every word SEDRA-checked. The generator, the exam XML and the keys are gitignored on purpose (public repo), so they reach other machines only through Syncthing; the earlier copy of the generator was lost that way.
- **[2026-11-17] Flash Pro card ids** are a hash of headword, transliteration and part of speech (`make_flashpro.py`), so TSV insertions no longer renumber cards. L11 story s.6 is now ܐܠܗܐ ܦܪܘܩܝܢܝ ܗܫܐ *ʾAlāhā, pruqayn(y) hāšā* (SEDRA-attested), replacing unattested suffixed imperfects.
- **[2026-11-17] Audit corrections (Ken: "fix everything"; see `REVIEW_2026-11-16.md`)**. These supersede the 2026-10-21 entries where they conflict:
  - "Reveal" is the Peal `ܓܠܐ` *glā*. `ܐܓܠܝ` is removed (404 in SEDRA; the Aphel means "exile").
  - Imperative + "me": strong verbs `-ayn(y)` (*pruqayn(y)*); III-Yodh attach directly: `ܐܣܢܝ` *ʾassān(y)* (not *ʾassaynī*).
  - Irregular imperatives: `ܙܠ` *zel*, `ܬܐ` *tā*, `ܗܒ` *hab*. "Show!" is Paael `ܚܘܐ` *ḥawwā*. "Bring him!" is `ܐܝܬܐܘܗܝ`.
  - Predicate adjectives stand in the absolute (*malkā ṭāb hū*); attributive adjectives take the noun's state.
  - Written-but-silent letters go in parentheses in transliteration: *ktab(w)*, *malk(y)*, *qaṭlan(y)*, *talmīdaw(hy)*, *ya(h)b*.
  - Every plural noun and adjective, and feminine plural participles, carry *syāmē*.
  - Transliteration: no spirant marking (*k*, not *ḵ*); *ū* in closed syllables except before a doubled consonant (*šūbḥā*, *šuddārā*); vowel-initial words carry *ʾ* (*ʾīdaʿ*).
  - Ethpeel shifts its vowel before vocalic endings (*ʾetqaṭlat*, *metqaṭlā*). Hollow verbs use the Ettaphal as passive (`ܐܬܬܩܝܡ` *ʾettqīm*).
  - Lessons 6 and 9 now have Sections 1–11 / 1–10 in sequence; the checks' `after` values were shifted to match.
- **[2026-10-21] Chapter Visuals**: Curated public-domain / CC-licensed manuscript illuminations and historical artwork placed under the title of each chapter (Lessons 00–12) with captions, responsive styling for HTML/interactive view, and page-break optimization for print PDF.

---

## 3. Active Constraints & Inviolable Policies

- **[LOCKED] No Emojis**: Strictly no emojis anywhere (commits, prose, markdown, code, logs).
- **[LOCKED] SEDRA Gate**: Every newly introduced or modified Syriac term must pass SEDRA verification for lemma, stem, and vocalization.
- **[LOCKED] Derivative Regeneration**: Any modification to lessons or `syriac_vocabulary.tsv` requires running the full build pipeline (`make_glossary.py`, `make_flashpro.py`, `interactive/build_interactive.py`, `course/make_assessments.py`, `make_site.py`, `./build.sh`).
- **[LOCKED] Table Integrity Lint**: Every table must pass the automated column count validator in `./build.sh`.

---

## 4. Open Questions & Unresolved Issues

- **[OPEN - PENDING KEN REVIEW]**: Course weights (10/10/15/25/40) and Moodle shell creation for RELS 4XX.
- **[OPEN - FUTURE PHASE]**: Audio recordings (Ken will record audio; SEDRA has no audio).
- **[2026-11-17] Flash Pro deck published**: corrected 420-card deck pushed to kmpenner/flash-pro (commit bf6cb8b; catalog totalCards 420). Browsers that loaded the October copy keep it until the deck is deleted and reloaded. After any TSV change, copy `flashpro/syriac_yukhannan.json` to flash-pro `data/` and update `totalCards` in both catalog files.
- **[OPEN - KEN]**: The syllabus promises weekly vocabulary quizzes (10%, lowest two dropped), but no quiz bank exists; decide the format (e.g. 10 items per lesson from the TSV, Syriac to English).

---

## 5. Active Milestone & Next Target

- **Current Status**: Complete 223-page textbook PDF (`Syriac_Textbook.pdf`), full HTML & DOCX outputs, interactive Moodle XML modules, Moodle assessment quizzes, and Flash Pro vocabulary decks compiled with 0 errors. All Opus review items resolved, table cell lint passed, and chapter artwork integrated across all 13 lessons.
- **Verification Gate**:
  ```bash
  python3 make_glossary.py
  python3 make_flashpro.py
  python3 interactive/build_interactive.py
  python3 course/make_assessments.py
  python3 make_site.py
  ./build.sh
  ```
- **Next Action**: Review by Ken / Course deployment.
