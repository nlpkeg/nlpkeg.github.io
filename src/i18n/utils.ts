import { ui, DEFAULT_LANG, type Lang, type UIKey } from './ui';

export function useTranslations(lang: Lang) {
  return function t(key: UIKey): string {
    return ui[lang][key] ?? ui[DEFAULT_LANG][key];
  };
}

// Build an href honoring the locale prefix (zh = no prefix, en = /en/...).
export function localizedPath(path: string, lang: Lang): string {
  const clean = path.startsWith('/') ? path : `/${path}`;
  if (lang === 'en') return clean === '/' ? '/en/' : `/en${clean}`;
  return clean;
}

// The "other" language and the path to switch to it for a given current path.
export function altLang(lang: Lang): Lang {
  return lang === 'zh' ? 'en' : 'zh';
}
