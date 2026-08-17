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

将仓库中的目录复制到你的 Codex skills 目录：

```text
skills/leetcode-practice-coach/
```

## 开始使用

在你的练习项目目录中执行：

```powershell
python skills/leetcode-practice-coach/scripts/init_data.py --preset hot100
python skills/leetcode-practice-coach/scripts/make_plan.py --count 5
```

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
