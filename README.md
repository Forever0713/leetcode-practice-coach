# LeetCode Practice Coach

一个通用的 LeetCode 练习与间隔复习 skill，帮助你从 Hot100 开始刷题，并持续记录每道题的掌握度、复习结果和下次复习时间。

它不依赖 Notion，也不要求登录力扣。数据默认保存在本地 CSV 文件中。

## 提供什么

- 内置官方 Hot100 题库
- 根据到期时间、掌握度和历史卡点生成每日计划
- 苏格拉底式引导：一次只给一个针对性的思考问题
- 渐进式提示：方向提示 → 结构化思路 → 完整解法
- 记录回忆、编码、讲解、提示次数、用时和主要卡点
- 自动计算掌握度和下一次复习日期
- 支持从力扣 Hot100 页面源代码提取最新题单
- 支持导入 CSV/JSON 题目目录或其他工具导出的力扣记录

## 安装

最简单的方式是把下面这段话直接发送给 Codex：

```text
请从 https://github.com/Forever0713/leetcode-practice-coach 安装 leetcode-practice-coach skill。
安装完成后告诉我 skill 的安装位置，并确认它可以用于生成 LeetCode Hot100 复习计划。
```

如果需要手动安装，将仓库中的 `skills/leetcode-practice-coach/` 目录复制到 Codex skills 目录。

## 开始使用

在你的练习项目目录中执行：

```powershell
python skills/leetcode-practice-coach/scripts/init_data.py --preset hot100
python skills/leetcode-practice-coach/scripts/make_plan.py
```

`make_plan.py` 默认每天安排 5 道题。也可以指定数量：

```powershell
python skills/leetcode-practice-coach/scripts/make_plan.py --count 3
```

同一天已经生成过计划时，脚本会复用原计划，保证计划稳定。只有明确需要重新安排时才使用：

```powershell
python skills/leetcode-practice-coach/scripts/make_plan.py --count 5 --refresh
```

初始化命令适合第一次使用时运行；如果本地已经有 `data/questions.csv`，不要随意重复使用 `--preset hot100`，以免覆盖现有题目目录。

初始化后会创建：

```text
data/questions.csv   题目目录
data/reviews.csv     每次复习记录
data/mastery.csv     当前掌握度和下次复习日期
data/plans/          每日计划快照
```

## 记录一次复习

```powershell
python skills/leetcode-practice-coach/scripts/record_review.py `
  --question 1 `
  --recall 2 `
  --coding 2 `
  --explanation 2 `
  --hints 1 `
  --result passed `
  --minutes 25 `
  --blocker none
```

题目可以使用题号、标题或 `titleSlug` 查找。评分范围为 0–3，结果可以是 `passed`、`debugged` 或 `failed`。

## 实际使用流程

这个 skill 的使用流程很简单，主要围绕一轮对话循环：

### 1. 生成今日计划

你可以直接说：

```text
生成今天的复习计划。
```

skill 会根据本地题库、到期时间、掌握度和历史卡点生成计划。默认安排 5 道题，并展示题目链接。如果当天已经生成过计划，会继续使用原计划；想重新安排时再说“重新生成今天的计划”。

### 2. 逐题复习

从计划中的第一题开始，skill 会通过一次一个问题的方式引导思考，而不是直接展示答案。你可以先分析思路、写代码，再根据提示逐步修正。

### 3. 记录并复习下一题

当前题目完成后，你可以说：

```text
记录这道题，复习下一题。
```

skill 会总结本次表现，记录复习结果、掌握度、用时和下一次复习日期，然后继续当天计划中的下一道题。

因此，一个典型的使用过程就是：

```text
生成今天的复习计划
→ 逐题思考和编码
→ 记录这道题，复习下一题
```

## 从官方页面更新 Hot100

在力扣 Hot100 页面查看网页源代码并保存为 HTML：

<https://leetcode.cn/studyplan/top-100-liked/>

然后执行：

```powershell
python skills/leetcode-practice-coach/scripts/import_hot100_html.py `
  .\leetcode-hot100.html `
  --output data/questions.csv
```

脚本读取页面内嵌的 `__NEXT_DATA__`，使用 `titleSlug` 作为稳定 ID，不依赖第三方题单或 Cookie。

## 数据隐私

本项目不会要求或保存力扣 Cookie，也不会自动上传本地复习数据。不要将 `.env.local`、`data/` 或包含个人记录的文件提交到公开仓库。
