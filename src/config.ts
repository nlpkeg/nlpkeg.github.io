// Central site configuration.
// Switching the homepage look is meant to be a one-line change here plus a CSS theme block.
// Available themes: 'constellation' (A 知识星图 · dark), 'circuit' (B 学术电路 · light), 'flow' (C 神经流形 · gradient).
export const ACTIVE_THEME = 'constellation' as const;

export type ThemeName = 'constellation' | 'circuit' | 'flow';

export const SITE = {
  nameZh: '自然语言处理与知识工程研究组',
  nameEn: 'NLP & Knowledge Engineering Research Group',
  shortName: 'NLPKE',
  org: 'CASIA',
  instituteZh: '中国科学院自动化研究所',
  instituteEn: 'Institute of Automation, Chinese Academy of Sciences',
  github: 'https://github.com/nlpkeg',
  huggingface: 'https://huggingface.co/NLPKE',
  location: '北京 · 海淀',
};

// Graduate students are shown as a count only (no names). Dedup of the roster gave 54 unique.
export const GRAD_STUDENTS = '50+';

export const STATS = [
  { n: '190+', zh: '近三年论文', en: 'Papers (3 yrs)' },
  { n: '8', zh: '开源工具', en: 'Open-Source Tools' },
  { n: '4', zh: '在职 Faculty', en: 'Faculty' },
  { n: '6', zh: '研究方向', en: 'Directions' },
];
