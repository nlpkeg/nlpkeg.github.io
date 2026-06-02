# NLPKE@CASIA 课题组官网 / Research Group Website

自然语言处理与知识工程研究组（NLP & Knowledge Engineering Research Group, 中国科学院自动化研究所 CASIA）官方网站。

> **本 README 面向 AI 编码代理（如 Claude Code）**：先读这里，再读 `CONTENT.md`（内容维护）和 `docs/superpowers/specs/2026-06-02-nlpke-website-design.md`（设计与决策的唯一真实来源）。

## TL;DR

- 框架：**Astro 5 + Tailwind v4 + Content Collections**，纯静态站点（SSG）。
- 语言：**中文默认（`/`）+ 英文（`/en/`）**，Astro 内置 i18n。
- 部署：推送到 `main` → GitHub Actions（`.github/workflows/deploy.yml`）`astro build` → 发布 `dist/` 到 **GitHub Pages（https://nlpkeg.github.io/）**。
- **只有 `dist/` 会被发布**：本仓库里的 README、`docs/`、`CONTENT.md`、`src/` 源码都不会作为网页提供，可放心提交。

## 命令

```bash
npm install        # 首次
npm run dev        # 本地开发 http://localhost:4321
npm run build      # 生产构建 → dist/
npm run preview    # 预览构建产物
```

远程开发预览（服务器跑 dev，本地 Windows 用 SSH 隧道）：`ssh -L 4321:localhost:4321 <user>@<host>`。

## 内容怎么改（重要）

**内容与模板分离。所有可更新内容都是 `src/content/` 下的 markdown / frontmatter，组件只消费数据，不要把内容硬编码进 `.astro`。** 字段说明、如何加一个人/工具/论文/资讯，全部见 **`CONTENT.md`**。

```
src/content/
  research/       6 个研究方向（首页卡 + 研究页）
  tools/          开源工具（flagship=true 才上首页；url 直链具体 GitHub 仓库）
  people/         成员（group: faculty | engineer | secretary | phd | master）
  publications/   论文（links.paper 必须指向会议官方页：aclanthology / openreview / ojs.aaai.org）
  news/zh/ news/en/   资讯（WP 式，含 date/tag，自动生成 /news/<slug> 详情页）
```

约定（来自用户明确要求）：
- 站点内容（成员简介、论文、bio 等）只放仓库，**不写进 AI 记忆**。
- 工具卡的 `url` 必须是**具体仓库**（如 `github.com/nlpkeg/Know-MRI`），不是组织主页。
- 论文 `links.paper` 用**会议官方链接**，不是 arXiv（arXiv 放 `links.arxiv`）。
- 团队页：导师=大卡（照片无边框、卡片保留）；工程师/秘书=小卡（左侧圆角方形头像）；研究生**只显示人数**（`src/config.ts` 的 `GRAD_STUDENTS`），不列名字。`advisor: false` 可去掉某位 faculty 的「研究生导师」标注。

## 架构地图

| 关注点 | 位置 |
|---|---|
| 站点级配置（组名/链接/统计/学生数） | `src/config.ts`（`SITE`、`STATS`、`GRAD_STUDENTS`） |
| **主题切换**（A/B/C 视觉方案） | `src/config.ts` 的 `ACTIVE_THEME` + `src/styles/themes.css`。改一行即换主题，内容不动 |
| 暗/亮模式（独立于主题） | `<html data-mode>` 轴，`ThemeToggle.astro` + BaseLayout 内联无闪烁脚本；令牌见 themes.css 各主题块 |
| i18n 文案 | `src/i18n/ui.ts`（zh/en 字典）、`src/i18n/utils.ts`（`useTranslations`/`localizedPath`） |
| 内容集合 schema（Zod 校验） | `src/content.config.ts` |
| 布局 / 组件 | `src/layouts/BaseLayout.astro`、`src/components/*.astro` |
| 页面（每页 zh + `/en/` 两版） | `src/pages/**`（含 `team/[slug]`、`news/[slug]` 动态路由） |
| 静态资源 | `public/`（`logos/`、`people/`、`group-photo.jpg`） |

主题令牌契约：每个主题在 `themes.css` 定义同一组 CSS 变量（`--bg/--ink/--accent/--accent-grad/--shadow/--font-*` 等），组件全部走变量，因此主题与暗亮模式都是换变量、不改组件。

## 部署

- `.github/workflows/deploy.yml`：push `main` → `withastro/action` 构建 → `actions/deploy-pages` 发布。
- 仓库 **Settings → Pages → Source 必须设为 “GitHub Actions”**。
- 组织站点仓库名固定为 `nlpkeg.github.io`，根路径，`astro.config.mjs` 里 `site='https://nlpkeg.github.io'`、`base='/'`。

## 待办 / 占位（接手前请知悉）

- **论文作者列表是占位**（会议链接已核实为真实），正式上线前逐条核对作者与顺序。
- `people/jin-zhuoran`（金卓然）：职称按「助理研究员」暂定、无照片（主页当前 404）、`advisor:false`；待补照片与确认。
- 何世柱、刘康照片为旧站兜底图，分辨率偏低，建议替换高清图。
- 研究方向详情页、论文全量、公众号资讯迁移尚未做（流程见 CONTENT.md）。
- 备选视觉方案 B（学术电路·浅色）/ C（神经流形·渐变）的整套 mockup 在用户的 gstack 数据目录，不在本仓库。

## 设计真实来源

`docs/superpowers/specs/2026-06-02-nlpke-website-design.md` —— 含所有已拍板决策、研究方向归纳依据、团队结构、部署目标。改动方向前先读它。
