"""Import a locally exported LeetCode history/catalog. It deliberately does not log in or handle cookies."""
import argparse, csv, json, os
from pathlib import Path
DATA = Path(os.environ.get("LEETCODE_COACH_DATA", Path.cwd() / "data")).resolve()
p = argparse.ArgumentParser(description="Import a LeetCode JSON/CSV export produced by a compatible tool")
p.add_argument("input", type=Path); p.add_argument("--source", default="leetcode-history"); a = p.parse_args()
target = Path(__file__).with_name("import_questions.py")
os.system(f'python "{target}" "{a.input}" --source "{a.source}"')
print("Platform history is stored as question metadata only; AI mastery is created by record_review.py.")
