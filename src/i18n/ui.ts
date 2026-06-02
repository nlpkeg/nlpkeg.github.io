export type Lang = 'zh' | 'en';

export const DEFAULT_LANG: Lang = 'zh';

export const ui = {
  zh: {
    'nav.home': '首页',
    'nav.team': '团队',
    'nav.research': '研究',
    'nav.publications': '论文',
    'nav.tools': '工具',
    'nav.news': '资讯',
    'hero.eyebrow': '中国科学院自动化研究所 · 知识工程',
    'hero.lead':
      '解构大模型内部的知识——从知识神经元、知识编辑到检索增强与神经符号推理，让语言模型的“知道”变得可理解、可编辑、可信赖。',
    'hero.cta1': '探索研究方向',
    'hero.cta2': '开源工具',
    'research.kicker': 'Research Directions',
    'research.title': '六大研究方向',
    'research.subtitle': '围绕“大模型知识工程”的连续光谱，从机制理解走向能力构建',
    'tools.kicker': 'Open Source',
    'tools.title': '旗舰工具',
    'tools.subtitle': 'github.com/nlpkeg · 把研究沉淀为可用的工具',
    'news.kicker': 'News',
    'news.title': '最新资讯',
    'news.subtitle': '组内动态、论文录用与学术活动',
    'footer.nav': '导航',
    'footer.resources': '资源',
    'footer.contact': '联系',
    'footer.join': '加入我们',
    'footer.contactWay': '联系方式',
    'footer.tagline': '自然语言处理与知识工程研究组',
  },
  en: {
    'nav.home': 'Home',
    'nav.team': 'Team',
    'nav.research': 'Research',
    'nav.publications': 'Publications',
    'nav.tools': 'Tools',
    'nav.news': 'News',
    'hero.eyebrow': 'Institute of Automation, CAS · Knowledge Engineering',
    'hero.lead':
      'We decode the knowledge inside large language models — from knowledge neurons and editing to retrieval augmentation and neural-symbolic reasoning — making what models "know" understandable, editable and trustworthy.',
    'hero.cta1': 'Explore Research',
    'hero.cta2': 'Open Source',
    'research.kicker': 'Research Directions',
    'research.title': 'Six Research Directions',
    'research.subtitle': 'A continuous spectrum of LLM knowledge engineering — from understanding mechanisms to building capabilities',
    'tools.kicker': 'Open Source',
    'tools.title': 'Flagship Tools',
    'tools.subtitle': 'github.com/nlpkeg · Research distilled into usable tools',
    'news.kicker': 'News',
    'news.title': 'Latest News',
    'news.subtitle': 'Group updates, paper acceptances and academic activities',
    'footer.nav': 'Navigation',
    'footer.resources': 'Resources',
    'footer.contact': 'Contact',
    'footer.join': 'Join Us',
    'footer.contactWay': 'Contact',
    'footer.tagline': 'NLP & Knowledge Engineering Research Group',
  },
} as const;

export type UIKey = keyof (typeof ui)['zh'];
