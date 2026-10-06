#!/usr/bin/env python3
"""Build the Flash Pro deck (flashpro/syriac_yukhannan.json) from syriac_vocabulary.tsv.

One bundle per lesson. Front = Syriac (Estrangela, RTL); back = English with
transliteration and grammar. Flash Pro's page font stack includes
Noto Sans Syriac, so no card template is needed. Copy the output into kmpenner/flash-pro data/.
"""
import csv, json, pathlib

DECK_ID = "deck_syriac_yukhannan"
LESSONS = ["The Alphabet", "Core Architecture", "Narrative Present", "Narrative Past",
           "Personalizing the Text", "Aphel Stem", "Paael Stem", "Weak Roots",
           "The Imperfect", "Commands and Intentions", "Passive Voice",
           "Verbal Suffixes", "Fringes of Syntax"]
EPOCH = 946684800000
STATS = dict(timesRight=0, timesWrong=0, timesRightSinceWrong=0,
             dateLastRight=EPOCH, dateLastWrong=EPOCH)

here = pathlib.Path(__file__).parent
rows = list(csv.DictReader(open(here / "syriac_vocabulary.tsv", encoding="utf-8"), delimiter="\t"))
pos = sorted({r["PartOfSpeech"] or "other" for r in rows})
cats = [{"id": f"cat_{p}", "name": p} for p in pos]
cards, bundles = [], [{"id": f"b_l{n:02d}", "name": f"Lesson {n}: {t}", "cardIds": []}
                      for n, t in enumerate(LESSONS)]
for i, r in enumerate(rows, 1):
    gram = ", ".join(x for x in (r["PartOfSpeech"], r["Gender"], r["Stem"],
                                 r["Root"] and f"root {r['Root']}") if x)
    cid = f"syr{i:04d}"
    p = r["PartOfSpeech"] or "other"
    cards.append({"id": cid, "num": i, "front": r["Syriac"],
                  "back": f"{r['English']} — {r['Transliteration']}" + (f" ({gram})" if gram else ""),
                  "categoryId": f"cat_{p}", "category": p, "frequency": 0,
                  "fb": dict(STATS), "bf": dict(STATS)})
    bundles[int(r["Lesson"])]["cardIds"].append(cid)

deck = {
    "id": DECK_ID, "name": "Syriac: The Acts of Mar Yukhannan", "createdDate": 1791244800000,
    "src": {"kind": "syriac_yukhannan", "cardsCount": len(cards)},
    "language": "Syriac", "categoryGroup": "Part of speech",
    "settings": {"fontSize": 26, "maximumSelected": 20,
                 "headTmpl": "", "frontTmpl": "", "backTmpl": ""},
    "categories": cats, "bundles": bundles,
    "criteria": [
        {"id": "crit_timed", "name": "Timed (Spaced Repetition)", "logic": "(NOW - LastRightTime) > (LastRightTime - LastWrongTime)"},
        {"id": "crit_all", "name": "All Cards", "logic": ""},
        {"id": "crit_new", "name": "Never Studied", "logic": "TimesRight == 0 AND TimesWrong == 0"},
        {"id": "crit_review", "name": "Needs Review (Streak < 3)", "logic": "TimesRightSinceWrong < 3"}],
    "cards": cards,
}
out = here / "flashpro" / "syriac_yukhannan.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(deck, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{out}: {len(cards)} cards, {len(bundles)} bundles")
