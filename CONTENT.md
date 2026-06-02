# 内容维护指南 · Content Guide

本站内容与模板分离，**所有可更新内容都在 `src/content/` 下的 markdown / YAML**，由 Astro Content Collections 校验。改内容不需要懂前端：照下面的字段填即可。

## 目录结构

```
src/content/
  research/   研究方向（首页 6 张卡 + 研究页），一方向一个 .md
  tools/      开源工具（首页旗舰 + 工具页），一工具一个 .md
  people/     成员（团队页），一人一个 .md
  news/zh/    中文资讯    news/en/  英文资讯（一篇一个 .md）
```

站点级信息（组名、GitHub/HF 链接、统计数字、地址）在 `src/config.ts` 的 `SITE` 和 `STATS`。

---

## 加一个研究方向 → `src/content/research/NN-slug.md`

```yaml
---
order: 7                      # 排序（数字）
icon: "🧠"                    # 卡片图标（emoji 或符号）
titleZh: 中文标题
titleEn: English Title
summaryZh: 中文一句话简介
summaryEn: One-line English summary
highlights:                  # 代表作（可选，列表）
  - Paper Name (Venue Year)
---
```

## 加一个工具 → `src/content/tools/slug.md`

```yaml
---
order: 4
name: 工具名
badge: "ACL 2025 Demo · MIT"  # 可选：会议/许可证标签
stars: "★ 14"                 # 可选：自由文本（star 数或 benchmark/toolkit）
url: https://github.com/nlpkeg/xxx
flagship: true                # true 才会出现在首页旗舰区
descZh: 中文描述
descEn: English description
---
```

## 论文（自动爬取，不用手写）

论文数据由爬虫维护，**不要手写**：`src/data/publications.json` 来自 `scripts/fetch_publications.py`（从 DBLP 按作者爬取、去重、同名过滤、按"主会→arXiv→期刊"选链接）。

```bash
python3 scripts/fetch_publications.py            # 增量更新（推荐，日常用）
python3 scripts/fetch_publications.py --refresh  # 全量重建
```

- 加新老师：编辑脚本顶部 `AUTHORS`（加 name/email/DBLP pid），跑增量。
- 想给某篇加 `highlight`（如 Spotlight/Oral）：直接在 `publications.json` 里那条加 `"highlight": "Spotlight"`；增量更新会保留你的手工编辑。
- 想隐藏个别误入的同名论文：从 json 删掉该条即可（下次增量不会重新加回，因为增量只补新 id——但 `--refresh` 会；误判请优先调脚本的过滤规则）。

## 加一个成员 → `src/content/people/slug.md`

```yaml
---
order: 5
nameZh: 张三
nameEn: Zhang San
roleZh: 博士生
roleEn: PhD Student
group: phd                    # faculty | phd | master
interestsZh: 方向一 · 方向二
interestsEn: Topic one · Topic two
bioZh: 中文简介（可选；老师建议填，会显示在成员详情页 /team/<slug>）
bioEn: English bio (optional)
photo: /people/zhangsan.jpg   # 可选；放 public/people/ 下；不填则显示姓氏首字
active: true
links:                        # 全部可选
  homepage: https://...
  scholar: https://...
  dblp: https://...
  github: https://...
  email: name@ia.ac.cn
---
```

> 团队页目前只展示 `group: faculty` 的成员。要展示博士/硕士分组，加好人后告诉开发者开启对应分组即可。

## 加一篇资讯 → `src/content/news/zh/2026-xx.md`（英文放 `news/en/`）

```yaml
---
lang: zh                      # zh 或 en，要和所在目录一致
title: 标题
date: 2026-06-01              # YYYY-MM-DD
tag: ICLR Spotlight           # 可选：标签
summary: 列表页显示的摘要
cover: /news/cover.jpg        # 可选：封面图
draft: false                  # true 则不发布
---

正文 markdown 写在这里。
```

公众号文章迁移：把正文转成 markdown 放进对应语言目录，图片放 `public/news/` 并在正文用 `/news/xxx.jpg` 引用。

---

## 本地预览

```bash
npm install      # 首次
npm run dev      # http://localhost:4321
```

## 换主题（给老板挑 A/B/C）

主题在 `src/config.ts` 的 `ACTIVE_THEME`：`'constellation'`（A 知识星图·深色，当前）/ `'circuit'`（B 学术电路·浅色）/ `'flow'`（C 神经流形·渐变）。令牌定义在 `src/styles/themes.css`。切主题只改这一行 + 对应 CSS 块，内容不动。
