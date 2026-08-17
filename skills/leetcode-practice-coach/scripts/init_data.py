from pathlib import Path
import sys
import os
import csv
import argparse
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATA = Path(os.environ.get("LEETCODE_COACH_DATA", Path.cwd() / "data")).resolve()
parser = argparse.ArgumentParser(); parser.add_argument("--preset", choices=["hot100"]); args = parser.parse_args()
DATA.mkdir(parents=True, exist_ok=True)
(DATA / "plans").mkdir(exist_ok=True)
files = {
    "questions.csv": ["id", "question_number", "title", "title_slug", "difficulty", "topics", "url", "active", "notes", "source"],
    "reviews.csv": ["reviewed_on", "question_id", "title", "recall", "coding", "explanation", "hints", "result", "minutes", "blocker", "notes", "quality", "interval_days", "next_review_date"],
    "mastery.csv": ["question_id", "mastery", "last_review_date", "next_review_date", "interval_days", "last_quality", "last_blocker", "review_count"],
}
for name, fields in files.items():
    path = DATA / name
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=fields).writeheader()
if args.preset == "hot100":
    preset = Path(__file__).resolve().parents[1] / "assets" / "hot100.csv"
    if not preset.exists(): raise SystemExit("Bundled Hot100 catalog is missing")
    DATA.joinpath("questions.csv").write_bytes(preset.read_bytes())
    print("Loaded bundled Hot100 catalog")
print(f"Initialized local LeetCode data in {DATA}")
