# Work Ledger: Syriac Textbook (The Acts of Mar Yukhannan)

> **Governance Principle (AutomatED Work Ledger / TRACER Protocol):**
> Agents must read this file before acting. Do not reopen settled decisions without explicit user instruction. Do not unilaterally resolve open questions. Check changes against the verification gate before committing.

---

## 1. Source Hierarchy & Authority

1. **Top Authority & Lessons Source:** `Lesson_00_The_Alphabet.md` through `Lesson_12_Fringes_Of_Syntax.md`
2. **Vocabulary Single Source of Truth:** `syriac_vocabulary.tsv` (419 entries)
3. **Interactive Learning Checks:** `interactive/checks/Lesson_NN.json`
4. **Compiled Production Artifacts:**
   - PDF Master: `Syriac_Textbook.pdf` (197 pages)
   - Interactive XML: `interactive/xml/Lesson_NN.xml`
   - Glossary: `Appendix_B_Glossary.md`, `course/moodle/Syriac_Glossary.xml`
   - Flash Pro Deck: `flashpro/syriac_yukhannan.json`
5. **Build Scripts:** `./build.sh`, `make_glossary.py`, `make_flashpro.py`, `interactive/build_interactive.py`

---

## 2. Settled Decisions (Locked Baseline)

- **[2026-10-06] Exercise Item Numbering**: All lesson exercises and their corresponding Answer Key sections reset to `1..N` per exercise. Continuous numbering across exercises within a lesson is prohibited.
- **[2026-10-06] Supplementary Vocabulary Deduping**: Section 11 tables must contain only genuine lesson-specific vocabulary. Do not copy Lesson 1 vocabulary into other lessons.
- **[2026-10-06] Attested Classical Syriac Only**: All vocabulary entries must be verified against Beth Mardutho SEDRA API (`sedra.bethmardutho.org`). Synthetic formations ending in `-ūttā` or `-ānā` without textual attestation are strictly barred.
- **[2026-10-06] TSV Citation Lemmas**: The `Syriac` column in `syriac_vocabulary.tsv` contains only single citation forms. Slashes (e.g. `ܒܪ / ܒܪܐ`) are prohibited; construct and absolute forms are noted in `Notes`.
- **[2026-10-06] Character Rendering**: Estrangela script set with Noto Sans Syriac. Academic transliteration for grammar/paradigms (`š`, `ṭ`, `ḥ`, `Yūḥannan`); "Yukhannan" in English prose.

---

## 3. Active Constraints & Inviolable Policies

- 🔒 **No Emojis**: Strictly no emojis anywhere (commits, prose, markdown, code, logs).
- 🔒 **SEDRA Gate**: Every newly introduced or modified Syriac term must pass SEDRA API check (HTTP 200).
- 🔒 **Derivative Regeneration**: Any modification to `syriac_vocabulary.tsv` requires rebuilding glossary, flashcards, and interactive checks (`make_glossary.py`, `make_flashpro.py`, `interactive/build_interactive.py`).

---

## 4. Open Questions & Unresolved Issues

- ⚠️ **[OPEN - PENDING KEN REVIEW]**: Course weights (10/10/15/25/40) and Moodle shell creation for RELS 4XX.
- ⚠️ **[OPEN - FUTURE PHASE]**: Audio recordings (Ken will record audio; SEDRA has no audio).
- ⚠️ **[OPEN - FUTURE PHASE]**: Copying `flashpro/syriac_yukhannan.json` to the separate `kmpenner/flash-pro` repo upon publication.

---

## 5. Active Milestone & Next Target

- **Current Status**: Complete, audited 197-page textbook PDF, interactive Moodle modules, and derivative assets compiled with 0 errors.
- **Verification Gate**:
  ```bash
  python3 make_glossary.py
  python3 make_flashpro.py
  python3 interactive/build_interactive.py
  ./build.sh
  ```
- **Next Action**: Review by Ken / Course deployment.
