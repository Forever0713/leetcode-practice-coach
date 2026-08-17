---
name: leetcode-practice-coach
description: Run a standalone, local-first LeetCode practice and spaced-review workflow. Use when Codex should guide a learner with Socratic questions and progressive hints, create a review plan, evaluate an attempt, and record review status and next review dates without requiring Notion or another external service.
---

# LeetCode Practice Coach

This skill is self-contained. It uses a small local CSV workbook under the caller's `data/` directory and does not require Notion, an account, or an existing export. Set `LEETCODE_COACH_DATA` to choose another writable directory.

## First-time setup

Run:

```powershell
python scripts/init_data.py --preset hot100
```

This creates:

- `data/questions.csv`: the learner's question catalog.
- `data/reviews.csv`: one row per settled review session.
- `data/mastery.csv`: derived scheduling state.
- `data/plans/`: stable daily plan snapshots.

Add questions to `questions.csv` using the documented columns. The only required fields are `id` and `title`; topics, difficulty, URL, and notes are optional. Use `title_slug` as the stable `id` when available, and keep the numeric question number in `question_number` for display.

Import a Hot100 CSV or a compatible JSON catalog with:

```powershell
python scripts/import_questions.py .\hot100.csv --source leetcode-hot100
```

For an exact official study-plan snapshot, save the page source as HTML and run:

```powershell
python scripts/import_hot100_html.py .\leetcode-hot100.html --output data/questions.csv
```

This reads the page's embedded `__NEXT_DATA__` payload, not third-party lists or visible DOM links.

Import a locally exported platform history with:

```powershell
python scripts/import_leetcode.py .\leetcode-export.json
```

The platform importer is intentionally file-based: it never asks for, stores, or prints cookies. The external `leetcode-skill` or another exporter can be used to produce the file; this coach only normalizes its question metadata. Read `references/imports.md` when adapting a new export format.

## Choose a question source

The coach never silently invents a question list. Before planning, choose one source:

1. **Hot100 starter catalog**: prepare or copy a CSV catalog of the Hot100 you want to follow into `data/questions.csv`. Keep `source=leetcode-hot100` in the optional source column so the catalog can later be replaced without losing review history.
2. **Your own list**: import any CSV with `id,question_number,title,title_slug,difficulty,topics,url,active,notes,source` columns.
3. **Small manual start**: add 5–10 questions yourself, then grow the catalog as you practice.

For a Hot100 learner, start with 3–5 questions per day, mixing arrays/strings, linked lists, trees, graphs, backtracking, and dynamic programming. Do not require all 100 questions to be present before the first session; add the next batch whenever the catalog becomes small.

The source list is separate from review state: replacing or expanding `questions.csv` does not erase `reviews.csv` or `mastery.csv`, as long as question IDs remain stable.

## Make a plan

For “开始今天复习”, “给我安排几道题”, or similar requests, run:

```powershell
python scripts/make_plan.py --count 5
```

Reuse an existing plan for the same date. Only use `--refresh` when the learner explicitly asks to replan. Prefer overdue and weak questions, keep topic diversity, and show each item's mode:

Always include the LeetCode URL when presenting a planned question or moving to the next question. If no URL is stored, say so instead of inventing one.

- `full-code`: independently derive and implement.
- `outline`: explain the algorithm, invariant, complexity, and edge cases.
- `debug`: repair a known blocker or previous implementation.
- `transfer`: compare a related problem and explain what transfers.

## Conduct a review

Begin with one focused diagnostic question that helps the learner choose a direction. Do not turn problem restatement into a mandatory ritual; ask for it only when the learner appears to misunderstand the task or when the statement has an important modeling ambiguity. Do not reveal stored solutions before the attempt. After the learner responds, choose the next question based on the observed gap. Ask about the approach first, then invariant/state, transitions, edge cases, and complexity as appropriate. Never request all of these answers in one message. Use progressive hints:

1. Ask a diagnostic question.
2. Point toward the relevant invariant or data structure.
3. Give structured pseudocode.
4. Discuss a full solution only after an explicit request or sustained inability to progress.

Good opening questions are problem-specific, for example:

- “如果先写一个最直接的解法，你会怎么枚举？”
- “这道题里哪些信息需要被快速查询？”
- “你觉得这里的状态应该表示什么？”
- “如果沿用你刚才的方法，输入规模大时最可能慢在哪里？”

Use the learner's answer to decide whether to ask for a hint, an invariant, a boundary case, or complexity analysis.

Classify the main blocker as one of: `algorithm-selection`, `state-definition`, `transition`, `boundary-condition`, `implementation-detail`, `complexity`, `transfer`, or `none`. Review reasoning, correctness, edge cases, complexity, and whether the learner can explain why the solution works.

## Record a settled review

When the learner says “下一题”, “这题差不多了”, “今天结束”, or asks to save progress, summarize the assessment and run:

```powershell
python scripts/record_review.py --question 1 --recall 2 --coding 2 --explanation 2 --hints 1 --result debugged --minutes 25 --blocker boundary-condition --notes "边界条件需要复习"
```

Ratings are 0–3. `result` is `passed`, `debugged`, or `failed`. The script appends to `reviews.csv` and updates `mastery.csv`; never edit historical review rows. Record only after the assessment is settled, and never claim persistence unless the command succeeds.

## Learning principles

- Guided learning is the default; complete code is a last resort.
- Passing code is not proof of durable mastery.
- Forgotten core ideas return quickly; independent success expands the interval.
- Keep sessions realistic, normally five items or fewer.
- Use deterministic scripts for dates and scheduling; use model judgment for ratings and blocker labels.
