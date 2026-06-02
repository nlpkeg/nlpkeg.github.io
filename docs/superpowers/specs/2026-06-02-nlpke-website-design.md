# NLPKE@CASIA 课题组网站 — 设计与交接文档

> 日期: 2026-06-02  
> 状态: **设计进行中（已基本定稿，待动手实现）**。本文件用于跨会话交接——上一会话在用户重启前写下。  
> 重要: 本目录当前名为 `nlprke_website`，**拼写有误，应为 `nlpke_website`（少一个 r）**。用户计划重命名后重启会话。重命名后，Claude 记忆的项目路径键会变化（见末尾"会话恢复注意事项"）。

## 1. 项目概述
为中科院自动化所 **自然语言处理与知识工程研究组（NLPKE@CASIA）** 开发新官网。
- GitHub org: https://github.com/nlpkeg （显示名 "NLPKE@CASIA"）
- HuggingFace org: https://huggingface.co/NLPKE （全名 "Nature Language Processing and Knowledge Engineering Research Group"，当前无公开模型/数据集）
- 由用户的 GitHub 账号管理 org，已配置 SSH 密钥。
- 旧站在 `static/`（站名 NLPR-CIP，2018–2021，单页 Bootstrap 风；含信息抽取/KBQA/知识图谱等已多半失效的 demo）。
- Logo 资产: `所LoGo/`（所 logo，含透明深/浅色长版 png）、`自然语言处理与知识工程研究组Logo/`（研究组 logo，ai/jpg/png）。

## 2. 已确认的关键决策（用户已拍板）
| 项 | 决策 |
|---|---|
| 框架 | **Astro**（内置 i18n 路由）+ **Tailwind CSS** + **Content Collections**（Zod 校验的 markdown/YAML 内容层） |
| 语言 | **中/英双语**（zh 默认 + en） |
| 部署 | **GitHub Pages 组站**，仓库名必须是 `nlpkeg/nlpkeg.github.io`，根路径 base='/' |
| 风格 | 浅色学术风 + 暗色切换，蓝色点缀 |
| 内容层 | 内容与模板分离，存为结构化 markdown/YAML；另配 `CONTENT.md` 维护指南（即用户 #7 要求的"AI 可读的网站信息更新 markdown"） |
| 记忆 | **站点内容（成员简介、论文、bio 等）不写入 Claude 记忆**，只放仓库 markdown（用户 #7 明确要求） |

## 3. 页面结构
```
首页 Home        — Hero(组名/slogan) · 六大研究方向卡片(见§3.1) · 最新资讯 · 旗舰工具 · 数据统计 · GitHub/HF 入口
团队 People      — 仅在职 4 位（见下）；结构需预留 博士生/硕士生 分组（用户说后面要贴，先只放 faculty）
研究 Research    — 展开§3.1 六大方向；含代表作链接（论文/工具）
论文 Publications— 按年份；含离职成员以自动化所邮箱发表的工作；每条 PDF/Code/BibTeX
工具 Tools       — 映射 GitHub 仓库（见下）
模型与数据 Models— 映射 HuggingFace NLPKE（当前空，先占位）
资讯 News        — 博客式 markdown 文章（公众号迁移），列表+详情，封面/日期/标签
加入我们 Join + 联系 Contact
```

### 3.1 研究方向（据 4 位老师 2024–2026 实际挂名论文归纳，2026-06-02 定稿）
> 旧组站的"信息抽取/知识图谱/知识问答/大模型知识工程"已过时。全组近期重心已转向**大模型内部的知识机制**（呼应"知识工程"组名，也是旗舰工具 Know-MRI / RWKU 的主题）。首页 6 张卡全列，研究页展开。
1. **大模型知识机制与可解释性** / LLM Knowledge Mechanisms & Interpretability — 知识神经元、知识定位、机理分析。代表作: Know-MRI(ACL25 Demo)、Journey to the Center of Knowledge Neurons(AAAI24)、Knowledge Localization(ICLR25 Spotlight)、The Knowledge Microscope(ACL25)。覆盖: 赵·刘·曹(核心)·何。
2. **知识编辑与机器遗忘** / Knowledge Editing & Unlearning — 终身编辑、编辑可靠性、遗忘。代表作: RWKU(NeurIPS24)、WilKE(ACL24 Findings)、Knowledge in Superposition(AAAI25 Oral)、Revealing the Deceptiveness of Knowledge Editing(ACL25)、M2Edit(EMNLP25)。覆盖: 赵·刘·曹。
3. **知识增强生成与检索（含 KG 问答）** / Knowledge-Augmented Generation & Retrieval (incl. KGQA) — RAG、长上下文、LLM-KG 融合、知识库问答。代表作: Generate-on-Graph(EMNLP24)、CogMG(ACL24)、KMatrix/KMatrix-2(EMNLP25 Demo)、RetroLM & SparK(AAAI26)、Landmark Embedding(EMNLP24)、LLaSA(NAACL25)。覆盖: 何·刘·赵。
4. **神经符号推理与知识蒸馏** / Neural-Symbolic Reasoning & Knowledge Distillation — 复杂推理、小模型蒸馏、规则学习。代表作: Neural-Symbolic Collaborative Distillation(AAAI25)、SKIntern(COLING25)、From Chain to Tree(COLING WS25)、Toxic CoT(ACL24)。覆盖: 何·刘·赵。
5. **大模型智能体与工具调用** / LLM Agents & Tool Use — 工具利用、GUI/多智能体、领域(司法)智能体。代表作: CITI(AAAI25)、GUI Agents(ACL26)、AgentsCourt/SimuCourt(EMNLP24)、Agent-RewardBench、WideSeek 多智能体。覆盖: 全员。
6. **复杂推理与数学/表格推理** / Complex & Structured Reasoning — 数学推理、表格/代码驱动推理、推理 RL。代表作: TaREx(AAAI26)、Bias-Restrained PReFT for Math(AAAI26)、MIRAGE 归纳推理(ICLR25)、Search-in-Context(ACL25 Findings)。覆盖: 赵·刘·何·曹。

(离职成员 张元哲/陈玉博/郭少茹 以自动化所邮箱发表的工作进论文页，不进上述方向卡覆盖统计。)

## 4. 内容架构（用户 #7 的 AI 可读内容层）
```
src/content/
  people/        一人一文 (frontmatter: name_zh/en, title, interests, photo, links{homepage,scholar,dblp,github}, active, role)
  publications/  按年 YAML (title, authors, venue, year, links{pdf,code,bibtex,project})
  tools/         一仓一文
  models/        HF 发布后补
  news/zh/*.md   news/en/*.md   长文按语言分目录
  research/      一方向一文
CONTENT.md       内容维护指南（讲清字段含义 + 如何加一个人/论文/资讯），供 AI/人维护
```

## 5. 团队成员（站点内容，放仓库；此处仅交接用）
**在职 faculty（团队页只列这 4 位）:**
- **赵军 Zhao Jun** — 研究员/PI。信息抽取、知识图谱、KBQA、推理、LLM。主页 https://zhaojun-nlpr.github.io/ ; Scholar HljRttwAAAAJ ; DBLP "Jun Zhao 0001" (pid 47/2026-1)。代表作 PCNN(EMNLP15)、COLING14 最佳论文、ICLR25 Spotlight。
- **刘康 Liu Kang** — 研究员。信息抽取、事件抽取、KG、QA、LLM 知识编辑。主页 https://www.nlpr.ia.ac.cn/cip/~liukang/index.html ; Scholar DtZCfl0AAAAJ。代表作 TransD(ACL15)、RCNN(AAAI15)，h-index 65。
- **何世柱 He Shizhu** — 研究员。KBQA、知识推理、LLM+KG、神经符号蒸馏、长上下文。主页 https://heshizhu.github.io/ ; GitHub https://github.com/heshizhu ; Scholar zBPIt3QAAAAJ ; DBLP 136/8650 ; shizhu.he@ia.ac.cn。代表作 Generate-on-Graph、神经符号协同蒸馏(AAAI25)、2025 智源青年学者。
- **曹鹏飞 Cao Pengfei** — 青年 faculty（2023 CASIA 博士，赵军门下）。事件抽取、LLM 知识编辑/定位、知识神经元、可解释性。主页 https://cpf-nlpr.github.io/ ; Scholar lP5_LJIAAAAJ ; pengfei.cao@nlpr.ia.ac.cn。代表作 RWKU 基准(NeurIPS24)、知识定位(ICLR25 Spotlight)、AAAI25 Oral。

**离职成员（不进团队页，但论文/成果页要收录其以 @nlpr.ia.ac.cn / @ia.ac.cn 邮箱发表的工作）:**
- 张元哲、陈玉博、郭少茹。

## 6. 工具/开源（映射 GitHub org nlpkeg）
- **Know-MRI** — ACL 2025 Demo，大模型知识机制揭示/解释工具 (14★, MIT)
- **KMatrix** — 异构知识增强工具包 for LLM (Python, Apache-2.0)；另有 **KMatrix-2**、**KMatrix-CR**
- **Capability-Neuron-Localization** — ICLR 2025 论文代码
- **D4S** — NeurIPS 2024 论文代码（编辑后性能下降的原因与方案）

## 7. 部署
- 用户在 GitHub 建空仓库 `nlpkeg/nlpkeg.github.io`（org 站点固定名），Claude 用 SSH 推送（本机**无 gh CLI**）。
- 加 `.github/workflows/deploy.yml`：push main → 构建 Astro → 发布 GitHub Pages。

## 8. 公众号 / 资讯
- 资讯板块本质是 markdown 博客；**用户后续提供公众号原文**。届时把文本+图片转成 `src/content/news/` 下 markdown；量大则写转换脚本（文章内容→markdown + 下载图片）。公众号无官方 API。

## 9. 待办 / 下一步（重启会话后从这里继续）
1. ~~研究方向据论文归纳~~ ✅ 已完成(2026-06-02)，见 §3.1：6 个方向定稿，首页 6 张卡全列。
2. 团队页结构预留博士生/硕士生分组（先只放 4 位 faculty）。✅ people 集合已有 group=faculty|phd|master；团队页当前只渲染 faculty，加学生后开启分组即可。
3. ~~脚手架 Astro 项目~~ ✅ 已完成(2026-06-02)，见 §12。
4. 让用户建 `nlpkeg/nlpkeg.github.io` 仓库。（待办：建仓 + 加 deploy.yml + SSH 推送）
5. 等用户给公众号原文后做资讯迁移（流程见 CONTENT.md）。

## 12. 实现现状（2026-06-02 脚手架完成）
Astro 5.18 + Tailwind v4 + Content Collections + 内置 i18n（zh 默认 / en）。已搭好并通过 `npm run build`（16 页静态产物）。
- **主题可切换**：`src/config.ts` 的 `ACTIVE_THEME`（当前 `constellation`=A），令牌在 `src/styles/themes.css`（已含 A/B/C 三套）。切主题=改一行 + 对应 CSS 块，内容不动。
- **内容层**：`src/content/{research,tools,people,news}` + `src/content.config.ts`（Zod 校验）。维护指南 `CONTENT.md`。
- **页面**（均 zh + /en/，共 30 路由）：首页、team（含成员详情 `/team/[slug]`）、research、tools、news（含文章详情 `/news/[slug]`，WP 风格带日期/标签/正文）、publications(占位)、join、contact。
- **组件**：BaseLayout / Nav / Footer / Hero / NeuralCanvas / ResearchGrid / Tools / News / Team / MemberProfile / NewsArticle / PageHead / ThemeToggle。
- **暗/亮模式**：`<html data-mode>` 轴（独立于 A/B/C 主题），导航栏日/月按钮切换，localStorage 持久化 + 无闪烁内联脚本；A 主题已配浅色调色板，神经 canvas 颜色随模式自适应。
- **成员照片**：`public/people/`（zhao-jun.jpg、cao-pengfei.png 取自主页；he-shizhu.jpg、liu-kang.jpg 用旧 static 兜底）。
- **团队页结构**（people 集合 group 字段：faculty/engineer/secretary/phd/master）：
  - 顶部**合影横幅** `public/group-photo.jpg`（用户提供的 合照.jpg 缩放而来）。
  - **导师**=4 faculty 大卡（照片+bioZh/bioEn，点进 `/team/[slug]` 详情；仅 faculty 生成详情页）。
  - **工程师与秘书**=小卡（工程师：薛智朋/吴顺/叶锦宇/吴迪/张学友；秘书：李文婷/郝希），只姓名+职称、无照片。
  - **研究生**=只显示人数，不列名字。`src/config.ts` 的 `GRAD_STUDENTS='50+'`（用户名单去重后唯一学生 54 人，排除了混入的 1 老师+4 工程师；用户要求不列名字、给稳妥数）。
- **论文**：`src/content/publications/`（6 篇种子，会议链接已核实真实；⚠️作者列表是占位待核对）。/publications 按年分组，链 ACL Anthology/OpenReview/AAAI/arXiv/code。
- **工具**：6 个直链 nlpkeg 组真实仓库（Know-MRI/KMatrix/KMatrix-2/KMatrix-CR/Capability-Neuron-Localization/D4S）。RWKU 不在该组，已移到论文。首页显 3 旗舰，/tools 显全部。
- **logo**：`public/logos/`。**本地预览**：`npm run dev` → http://localhost:4321（Windows `ssh -L 4321:localhost:4321`）。
- 待做：学生名单、论文页真实数据、研究方向详情页、deploy.yml、刘康/何世柱更高清照片（现用旧图）。

## 10. 会话恢复注意事项（重要）
- 目录将从 `nlprke_website` 重命名为 `nlpke_website`。Claude 记忆按项目路径分目录存放：
  - 旧: `~/.claude/projects/-home-xzp-project-nlprke-website/memory/`
  - 新: `~/.claude/projects/-home-xzp-project-nlpke-website/memory/`
- 本会话已把记忆同时写入这两个路径，尽量保证重启后能自动加载。但**最可靠的是本设计文档**（随文件夹移动）。重启后请先读本文件。

## 11. 视觉设计方向（2026-06-02 通过 /design-shotgun 探索）
手写了 3 个真实 HTML 首页 mockup（非 AI 生图，因本机只有 DeepSeek key，OpenAI 图像 API 不可用）。三者**内容完全一致，差异只在布局/主题**。
- **主选 = A 知识星图 / Knowledge Constellation**：深色科技风，Hero 实时 canvas 神经网络/知识图谱动画，霓虹蓝节点，最贴 logo 电路感。Space Grotesk + Noto Sans SC。
- 备份保留（回头给老板挑）：**B 学术电路**（浅色机构可信 + 电路走线分隔，IBM Plex）、**C 神经流形**（流动渐变网格 Hero + 编辑式大列表，Sora）。
- **品牌色**（取自研究组 logo 蓝渐变）：亮青 #36D6FF · 天蓝 #1E9BE0 · 宝蓝 #2A6BF2 · 深蓝 #15357E；深色底 #070A16。
- **mockup 文件位置**（设计产物，不在仓库里，随 gstack 用户数据持久化）：`~/.gstack/projects/nlpke_website/designs/homepage-20260602/`（variant-A/B/C.html + index.html 对比看板 + assets/ logo + approved.json）。预览：`python3 -m http.server 8848` 后访问 `index.html`。

### 11.1 架构要求：主题可切换（用户明确诉求）
老板可能从 A/B/C 里另挑。因内容与布局已分离，Astro 实现时**必须把主题做成可快速切换的层**，切换 ≠ 重写：
- 内容统一走 Content Collections（§4），页面组件只消费数据。
- 视觉令牌（配色/字体/圆角/阴影/动效）集中在一处（Tailwind theme + CSS 变量 + 一个 `theme` 配置）。
- 首页区块（Hero/方向卡/工具/资讯）做成可换的 layout 变体，A=星图深色、B=电路浅色、C=流形渐变，理想情况下切换是改一个配置 + 一套 CSS。
