import argparse, csv, os, sys
from datetime import date, timedelta
from pathlib import Path

DATA = Path(os.environ.get("LEETCODE_COACH_DATA", Path.cwd() / "data")).resolve()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
BLOCKERS = {"algorithm-selection", "state-definition", "transition", "boundary-condition", "implementation-detail", "complexity", "transfer", "none"}
ADJ = {"passed": .25, "debugged": -.15, "failed": -.65}

def rows(path):
    return list(csv.DictReader(path.open(encoding="utf-8-sig"))) if path.exists() else []
def write(path, fields, values):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(values)

p = argparse.ArgumentParser(); p.add_argument("--question", required=True); p.add_argument("--recall", type=int, required=True, choices=range(4)); p.add_argument("--coding", type=int, required=True, choices=range(4)); p.add_argument("--explanation", type=int, required=True, choices=range(4)); p.add_argument("--hints", type=int, required=True, choices=range(4)); p.add_argument("--result", choices=ADJ, required=True); p.add_argument("--minutes", type=int, default=0); p.add_argument("--blocker", choices=sorted(BLOCKERS), default="none"); p.add_argument("--notes", default=""); p.add_argument("--date", default=date.today().isoformat()); a = p.parse_args()
questions = rows(DATA / "questions.csv"); q = next((x for x in questions if x["id"] == a.question or x.get("question_number") == a.question or x["title"].lower() == a.question.lower()), None)
if not q: raise SystemExit("Question not found in data/questions.csv")
reviews = rows(DATA / "reviews.csv"); mastery = rows(DATA / "mastery.csv"); old = next((x for x in mastery if x["question_id"] == q["id"]), {})
quality = max(0, min(3, a.recall*.4 + a.coding*.35 + a.explanation*.25 - a.hints*.22 + ADJ[a.result])); prior = int(old.get("interval_days") or 1)
interval = 1 if quality < 1.25 else 3 if quality < 2 else min(90, max(7, round(prior*1.7))) if quality < 2.65 else min(90, max(14, round(prior*2.2)))
next_date = date.fromisoformat(a.date) + timedelta(days=interval); observed = round(quality / 3 * 100); mastery_score = round(float(old.get("mastery") or 50)*.55 + observed*.45)
if a.result == "failed": mastery_score = min(mastery_score, 45)
reviews.append({"reviewed_on": a.date, "question_id": q["id"], "title": q["title"], "recall": a.recall, "coding": a.coding, "explanation": a.explanation, "hints": a.hints, "result": a.result, "minutes": a.minutes, "blocker": a.blocker, "notes": a.notes, "quality": round(quality, 3), "interval_days": interval, "next_review_date": next_date.isoformat()})
state = {"question_id": q["id"], "mastery": mastery_score, "last_review_date": a.date, "next_review_date": next_date.isoformat(), "interval_days": interval, "last_quality": round(quality, 3), "last_blocker": a.blocker, "review_count": int(old.get("review_count") or 0)+1}
mastery = [x for x in mastery if x["question_id"] != q["id"]] + [state]
write(DATA / "reviews.csv", list(reviews[0]), reviews); write(DATA / "mastery.csv", list(state), mastery)
print(f"Recorded {q['id']} — {q['title']}; next review: {next_date.isoformat()}")
