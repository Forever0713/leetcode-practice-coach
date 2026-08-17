import argparse, csv, json, os, sys
from collections import Counter
from datetime import date
from pathlib import Path

DATA = Path(os.environ.get("LEETCODE_COACH_DATA", Path.cwd() / "data")).resolve()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
def read(name):
    p = DATA / name
    return list(csv.DictReader(p.open(encoding="utf-8-sig"))) if p.exists() else []
def main():
    p = argparse.ArgumentParser(); p.add_argument("--count", type=int, default=5); p.add_argument("--date", default=date.today().isoformat()); p.add_argument("--refresh", action="store_true"); p.add_argument("--topic"); a = p.parse_args()
    if not 1 <= a.count <= 30: raise SystemExit("--count must be between 1 and 30")
    plans = DATA / "plans"; plans.mkdir(exist_ok=True); path = plans / f"{a.date}.json"
    if path.exists() and not a.refresh:
        print(path.read_text(encoding="utf-8")); return
    states = {x["question_id"]: x for x in read("mastery.csv")}; ranked = []
    today = date.fromisoformat(a.date)
    for q in read("questions.csv"):
        if q.get("active", "true").lower() in {"false", "0", "no"}: continue
        topics = [x.strip() for x in q.get("topics", "").replace("，", ",").split(",") if x.strip()]
        if a.topic and a.topic not in topics: continue
        s = states.get(q["id"], {}); due = s.get("next_review_date"); score = 18 + max(0, 60 - float(s.get("mastery") or 50))*.45
        reason = ["尚未建立复习记录"] if not due else []
        if due:
            delta = (today - date.fromisoformat(due)).days; score += 45 + min(delta, 30)*2 if delta >= 0 else max(0, 12 + delta); reason.append("已到期" if delta >= 0 else f"{abs(delta)}天后到期")
        if s.get("last_blocker") and s["last_blocker"] != "none": score += 8; reason.append(f"上次卡点：{s['last_blocker']}")
        quality = float(s.get("last_quality") or 3); mode = "debug" if s.get("last_blocker") in {"boundary-condition", "implementation-detail", "transition"} else "outline" if quality < 1.25 or float(s.get("mastery") or 0) >= 75 else "transfer" if int(s.get("review_count") or 0) >= 4 else "full-code"
        ranked.append({"id": q["id"], "title": q["title"], "difficulty": q.get("difficulty", ""), "topics": topics, "mode": mode, "score": round(score, 1), "reasons": reason or ["维持长期记忆"], "url": q.get("url", "")})
    ranked.sort(key=lambda x: (-x["score"], x["title"])); chosen=[]; counts=Counter()
    while ranked and len(chosen) < a.count:
        item = max(ranked, key=lambda x: x["score"] - counts[x["topics"][0] if x["topics"] else "未分类"]*12); ranked.remove(item); chosen.append(item); counts[item["topics"][0] if item["topics"] else "未分类"] += 1
    out = {"date": a.date, "items": chosen}; path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"); print(json.dumps(out, ensure_ascii=False, indent=2))
if __name__ == "__main__": main()
