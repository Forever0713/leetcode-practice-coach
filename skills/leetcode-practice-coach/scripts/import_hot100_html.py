"""Extract the official study-plan questions from saved LeetCode HTML."""
import argparse, csv, json, os, re, sys
from html.parser import HTMLParser
from pathlib import Path

DATA = Path(os.environ.get("LEETCODE_COACH_DATA", Path.cwd() / "data")).resolve()
FIELDS = ["id", "question_number", "title", "title_slug", "difficulty", "topics", "url", "active", "notes", "source"]
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

class NextData(HTMLParser):
    def __init__(self): super().__init__(); self.inside=False; self.parts=[]
    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("id") == "__NEXT_DATA__": self.inside=True
    def handle_endtag(self, tag):
        if tag == "script" and self.inside: self.inside=False
    def handle_data(self, data):
        if self.inside: self.parts.append(data)

def walk(value):
    if isinstance(value, dict):
        if value.get("titleSlug") and value.get("questionFrontendId"):
            yield value
        for child in value.values(): yield from walk(child)
    elif isinstance(value, list):
        for child in value: yield from walk(child)

p = argparse.ArgumentParser(); p.add_argument("html", type=Path); p.add_argument("--output", type=Path); a = p.parse_args()
parser = NextData(); parser.feed(a.html.read_text(encoding="utf-8"));
if not parser.parts: raise SystemExit("No __NEXT_DATA__ script found")
payload = json.loads("".join(parser.parts)); found = list(walk(payload)); seen = set(); rows=[]
for item in found:
    slug = item["titleSlug"]
    if slug in seen: continue
    seen.add(slug)
    title = item.get("translatedTitle") or item.get("titleCn") or item.get("title") or slug
    difficulty = item.get("difficulty", "")
    if isinstance(difficulty, int): difficulty = {1:"简单",2:"中等",3:"困难"}.get(difficulty, "")
    rows.append({"id": slug, "question_number": str(item["questionFrontendId"]), "title": title, "title_slug": slug, "difficulty": difficulty, "topics": ",".join(x.get("translatedName", x.get("name", "")) for x in item.get("topicTags", []) if isinstance(x, dict)), "url": f"https://leetcode.cn/problems/{slug}/", "active": "true", "notes": "", "source": "leetcode-hot100"})
if not rows: raise SystemExit("No question objects found in __NEXT_DATA__")
out = (a.output or DATA / "questions.csv").resolve(); out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", newline="", encoding="utf-8-sig") as f: csv.DictWriter(f, fieldnames=FIELDS).writeheader(); csv.DictWriter(f, fieldnames=FIELDS).writerows(rows)
print(f"Extracted {len(rows)} questions to {out}")
