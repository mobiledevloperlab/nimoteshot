const documentRoutes = {
  'README.md': '/docs/guide',
  'README.zh-CN.md': '/docs/guide-zh',
  '.github/CONTRIBUTING.md': '/docs/contributing',
  '.github/SECURITY.md': '/docs/security',
  'LICENSE': '/docs/license',
  'docs/THIRD_PARTY_NOTICES.md': '/docs/notices'
};

const slug = location.pathname.split('/').filter(Boolean).at(-1) || 'guide-zh';
const sourceButton = document.getElementById('doc-source');
const content = document.getElementById('doc-content');
const title = document.getElementById('doc-title');
const themeButton = document.getElementById('theme');

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#110d1b' : '#f8f7fb';
  themeButton.textContent = theme === 'dark' ? '☀' : '◐';
  themeButton.setAttribute('aria-label', theme === 'dark' ? '切换到浅色主题' : '切换到深色主题');
}

let theme = localStorage.getItem('nimoteshot-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
applyTheme(theme);
themeButton.addEventListener('click', () => {
  theme = theme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('nimoteshot-theme', theme);
  applyTheme(theme);
});

const activeLink = document.querySelector(`[data-doc="${slug === 'guide-zh' ? 'guide' : slug}"]`);
activeLink?.classList.add('active');
if (slug === 'guide' && activeLink) activeLink.href = '/docs/guide';

function resolveTarget(target, source) {
  if (/^(?:https?:|mailto:|#)/i.test(target)) return target;
  const base = new URL('/' + source, location.origin);
  const normalized = new URL(target, base).pathname.replace(/^\//, '');
  if (documentRoutes[normalized]) return documentRoutes[normalized];
  if (normalized.startsWith('web/assets/')) return '/assets/' + normalized.split('/').at(-1);
  return `https://github.com/mobiledevloperlab/nimoteshot/blob/master/${normalized}`;
}

function appendInline(parent, text, source) {
  text = text.replace(/<[^>]*>/g, '');
  const pattern = /(`[^`]+`|\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*)/g;
  let cursor = 0;
  for (const match of text.matchAll(pattern)) {
    parent.append(document.createTextNode(text.slice(cursor, match.index)));
    if (match[0].startsWith('`')) {
      const code = document.createElement('code');
      code.textContent = match[0].slice(1, -1);
      parent.append(code);
    } else if (match[2]) {
      const link = document.createElement('a');
      link.textContent = match[2];
      link.href = resolveTarget(match[3], source);
      if (/^https?:/i.test(link.href) && new URL(link.href).origin !== location.origin) {
        link.target = '_blank';
        link.rel = 'noopener';
      }
      parent.append(link);
    } else {
      const strong = document.createElement('strong');
      strong.textContent = match[4];
      parent.append(strong);
    }
    cursor = match.index + match[0].length;
  }
  parent.append(document.createTextNode(text.slice(cursor)));
}

function cells(line) {
  return line.trim().replace(/^\||\|$/g, '').split('|').map(value => value.trim());
}

function renderMarkdown(markdown, source) {
  const fragment = document.createDocumentFragment();
  const lines = markdown.replace(/\r/g, '').split('\n');
  let index = 0;
  let codeLines = null;
  while (index < lines.length) {
    const line = lines[index];
    if (line.startsWith('```')) {
      if (codeLines === null) codeLines = [];
      else {
        const pre = document.createElement('pre');
        const code = document.createElement('code');
        code.textContent = codeLines.join('\n');
        pre.append(code); fragment.append(pre); codeLines = null;
      }
      index += 1; continue;
    }
    if (codeLines !== null) { codeLines.push(line); index += 1; continue; }
    if (!line.trim() || /^<\/?(?:p|div|picture|summary|details|img|a|br)\b/i.test(line.trim())) { index += 1; continue; }
    const heading = /^(#{1,4})\s+(.+)$/.exec(line);
    if (heading) {
      const node = document.createElement(`h${Math.min(heading[1].length + 1, 5)}`);
      appendInline(node, heading[2], source); fragment.append(node); index += 1; continue;
    }
    if (/^\s*[-*_]{3,}\s*$/.test(line)) { fragment.append(document.createElement('hr')); index += 1; continue; }
    if (/^\s*[-*+]\s+/.test(line)) {
      const list = document.createElement('ul');
      while (index < lines.length && /^\s*[-*+]\s+/.test(lines[index])) {
        const item = document.createElement('li');
        appendInline(item, lines[index].replace(/^\s*[-*+]\s+/, ''), source); list.append(item); index += 1;
      }
      fragment.append(list); continue;
    }
    if (/^\s*\d+\.\s+/.test(line)) {
      const list = document.createElement('ol');
      while (index < lines.length && /^\s*\d+\.\s+/.test(lines[index])) {
        const item = document.createElement('li');
        appendInline(item, lines[index].replace(/^\s*\d+\.\s+/, ''), source); list.append(item); index += 1;
      }
      fragment.append(list); continue;
    }
    if (line.includes('|') && index + 1 < lines.length && /^\s*\|?\s*:?-+/.test(lines[index + 1])) {
      const table = document.createElement('table');
      const head = document.createElement('thead'); const headRow = document.createElement('tr');
      cells(line).forEach(value => { const cell = document.createElement('th'); appendInline(cell, value, source); headRow.append(cell); });
      head.append(headRow); table.append(head); index += 2;
      const body = document.createElement('tbody');
      while (index < lines.length && lines[index].includes('|') && lines[index].trim()) {
        const row = document.createElement('tr');
        cells(lines[index]).forEach(value => { const cell = document.createElement('td'); appendInline(cell, value, source); row.append(cell); });
        body.append(row); index += 1;
      }
      table.append(body); fragment.append(table); continue;
    }
    const paragraph = [];
    while (index < lines.length && lines[index].trim() && !/^(#{1,4})\s|^```|^\s*[-*+]\s+|^\s*\d+\.\s+/.test(lines[index])) {
      if (!/^<[^>]+>/.test(lines[index].trim())) paragraph.push(lines[index].trim());
      index += 1;
    }
    if (paragraph.length) {
      const node = document.createElement(line.startsWith('>') ? 'blockquote' : 'p');
      appendInline(node, paragraph.join(' ').replace(/^>\s*/, ''), source); fragment.append(node);
    }
  }
  content.replaceChildren(fragment);
}

fetch(`/api/docs/${encodeURIComponent(slug)}`, {headers: {'Accept': 'application/json'}})
  .then(response => { if (!response.ok) throw new Error('Document not found'); return response.json(); })
  .then(documentData => {
    title.textContent = documentData.title;
    window.document.title = `${documentData.title} — NimoteShot`;
    renderMarkdown(documentData.content, documentData.source);
    sourceButton.href = '#doc-content';
  })
  .catch(() => {
    title.textContent = '文档暂时无法读取';
    content.innerHTML = '<p class="docs-error">请返回工作台后重试。</p>';
  });
