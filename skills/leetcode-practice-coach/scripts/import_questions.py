"""Import a question catalog from CSV or a JSON export without touching review state."""
import argparse, csv, json, os, re, sys
from pathlib import Path

DATA = Path(os.environ.get("LEETCODE_COACH_DATA", Path.cwd() / "data")).resolve()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
FIELDS = ["id", "question_number", "title", "title_slug", "difficulty", "topics", "url", "active", "notes", "source"]

def normalize(item, source):
    topics = item.get("topics", item.get("topicTags", ""))
    if isinstance(topics, list): topics = ",".join(str(x.get("name", x)) if isinstance(x, dict) else str(x) for x in topics)
    url = item.get("url", item.get("link", "")); slug = item.get("title_slug", item.get("titleSlug", ""))
    if not slug and url:
        match = re.search(r"/problems/([^/?#]+)", url); slug = match.group(1) if match else ""
    raw_id = str(item.get("id", item.get("questionFrontendId", "")))
    number = str(item.get("question_number", item.get("questionFrontendId", "")))
    if not number:
        match = re.match(r"\s*(\d+)", raw_id); number = match.group(1) if match else ""
    title = item.get("title", item.get("titleCn", "")); stable_id = slug or raw_id
    return {"id": stable_id, "question_number": number, "title": title, "title_slug": slug, "difficulty": item.get("difficulty", ""), "topics": topics, "url": url, "active": str(item.get("active", True)).lower(), "notes": item.get("notes", ""), "source": item.get("source", source)}

p = argparse.ArgumentParser(); p.add_argument("input", type=Path); p.add_argument("--source", default="imported"); a = p.parse_args()
if a.input.suffix.lower() == ".csv":
    items = list(csv.DictReader(a.input.open(encoding="utf-8-sig")))
else:
    raw = json.loads(a.input.read_text(encoding="utf-8")); items = raw if isinstance(raw, list) else raw.get("questions", raw.get("data", []))
items = [normalize(x, a.source) for x in items if normalize(x, a.source)["id"] and normalize(x, a.source)["title"]]
DATA.mkdir(parents=True, exist_ok=True); path = DATA / "questions.csv"; existing = {}
if path.exists():
    existing = {x["id"]: x for x in csv.DictReader(path.open(encoding="utf-8-sig"))}
for item in items: existing[item["id"]] = item
with path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(existing.values())
print(f"Imported {len(items)} questions; catalog now contains {len(existing)} questions: {path}")
