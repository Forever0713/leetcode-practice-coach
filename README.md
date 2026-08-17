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

## 推荐使用流程

第一次使用时，可以直接告诉 Codex 你的目标，例如：

```text
我想从力扣 Hot100 开始练习，帮我准备今天的复习。
先帮我生成一个合理的计划，然后从第一题开始带着我思考，不要直接给答案。
```

如果还没有初始化本地题库，Codex 会先完成初始化；默认计划包含 5 道题，并展示每道题的力扣链接。

之后每天可以用自然语言继续，例如：

```text
今天继续刷题，先看看安排了哪些题。
```

```text
刚才那道题记录一下，我们继续下一题。
```

如果想调整当天的题量，可以说：

```text
今天时间不多，只安排 3 道题，并重新生成计划。
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
