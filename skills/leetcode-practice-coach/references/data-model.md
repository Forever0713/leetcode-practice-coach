# Local data model

`questions.csv` columns:

`id,question_number,title,title_slug,difficulty,topics,url,active,notes,source`

`id` should equal `title_slug` when available. `question_number` is display metadata. `source` identifies where the question entered the catalog, for example `leetcode-hot100`, `custom`, or `company-list`. It is metadata, not a scheduling signal.

`reviews.csv` is append-only and contains the review date, ratings, hint level, result, minutes, blocker, quality, interval, and next review date.

`mastery.csv` contains the current derived state per question: mastery, last review date, next review date, interval, last quality, last blocker, and review count.

Ratings use 0–3: 0 means no useful recall / unable to implement / unable to explain; 3 means immediate recall / robust implementation / invariant-based explanation. Hint levels are 0 none, 1 directional, 2 pseudocode, 3 near-complete.
