"""Build the self-contained academic homepage using only Python's standard library."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'docs'
OUT.mkdir(exist_ok=True)
SITE_URL = json.loads((ROOT / 'site-config.json').read_text(encoding='utf-8')).get('url', '').rstrip('/') + '/'
papers = json.loads((ROOT / 'publications.json').read_text(encoding='utf-8'))
base_css = (ROOT / 'template-base.css').read_text(encoding='utf-8')
e = html.escape

def bibtex(p):
    authors = ' and '.join(', '.join(reversed(a.rsplit(' ', 1))) for a in p['authors'])
    fields = [('title', '{' + p['title'] + '}'), ('author', authors), ('journal', p['journal']),
              ('year', str(p['year'])), ('volume', p['volume'])]
    if p.get('issue'):
        fields.append(('number', p['issue']))
    fields.extend([('pages', p['article']), ('doi', p['doi']), ('url', 'https://doi.org/' + p['doi'])])
    return '@article{' + p['id'] + ',\n' + ',\n'.join('  ' + k + ' = {' + v + '}' for k, v in fields) + '\n}\n'

citation_dir = OUT / 'assets' / 'citations'
citation_dir.mkdir(parents=True, exist_ok=True)
(citation_dir / 'jianglong-chen-publications.bib').write_text('\n'.join(bibtex(p) for p in papers), encoding='utf-8')

rows = []
for i, p in enumerate(papers, 1):
    (citation_dir / (p['id'] + '.bib')).write_text(bibtex(p), encoding='utf-8')
    authors = []
    for j, author in enumerate(p['authors']):
        author_text = '<strong class="me">' + e(author) + '</strong>' if author == 'Jianglong Chen' else e(author)
        if j in p['equal']:
            author_text += '<sup title="共同贡献">†</sup>'
        authors.append(author_text)
    volume = p['volume'] + ('(' + p['issue'] + ')' if p.get('issue') else '')
    pdf_link = f'<a class="mini-link" href="{p["pdf"]}" target="_blank" rel="noopener">PDF 全文 ↗</a>' if p.get('pdf') else ''
    search = ' '.join([p['title'], p['journal'], p['summary'], p['role'], p['doi'], *p['tags']]).lower()
    rows.append(f'''
      <article class="publication-card" id="paper-{p['id']}" data-lead="{str(p['lead']).lower()}" data-category="{p['category']}" data-search="{e(search, quote=True)}">
        <div class="pub-side" aria-hidden="true"><span class="pub-number">{i:02}</span><span class="pub-year">{p['year']}</span><span class="pub-rule"></span></div>
        <div class="pub-main">
          <div class="pub-heading"><span class="journal">{e(p['journal'])}</span><span class="role {'lead-role' if p['lead'] else ''}">{p['role']}</span></div>
          <h3 class="item-title" lang="en"><a href="{p['url']}" target="_blank" rel="noopener noreferrer">{e(p['title'])}<span class="external-arrow" aria-hidden="true"> ↗</span></a></h3>
          <p class="authors" lang="en">{', '.join(authors)}</p>
          <p class="pub-meta">{p['year']} · {volume} · {p['article']}<span class="meta-divider">/</span><span class="doi">doi: {p['doi']}</span></p>
          <p class="highlight">{p['summary']}</p>
          <div class="pub-bottom"><div class="pub-tags">{''.join('<span class="tag">' + e(t) + '</span>' for t in p['tags'])}</div>
          <div class="mini-links"><a class="mini-link" href="https://doi.org/{p['doi']}" target="_blank" rel="noopener noreferrer">DOI ↗</a>{pdf_link}<a class="mini-link" href="assets/citations/{p['id']}.bib" download>引用 ↓</a></div></div>
          <details class="paper-detail"><summary>研究说明</summary><p>{p['note']}</p></details>
        </div>
      </article>''')

css = r'''
    :root { --bg: #f5f6f8; --link: #285ba0; --text: #1f293b; --muted: #687487; --line: #e6eaf0; --shadow: 0 10px 38px rgba(29,48,77,.035); }
    body { background: var(--bg); font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif; }
    .container { max-width: 1120px; padding: 26px 28px 20px; }
    .top-nav { margin: 0 5px 27px; font-size: 13px; }
    .nav-brand { display: flex; gap: 11px; align-items: center; color: var(--text); }
    .brand-mark { display: grid; place-items:center; width:29px; height:29px; border-radius:9px; color:#fff; background:var(--link); font-family:Georgia,serif; font-size:14px; }
    .nav-name { letter-spacing:.08em; font-size:12px; }
    .nav-links { gap:25px; }
    .nav-links a { color:#4e5c70; }
    a:focus-visible, button:focus-visible, input:focus-visible, summary:focus-visible { outline:3px solid #83a9de; outline-offset:5px; }
    .skip-link { position:fixed;left:20px;top:-80px;z-index:100;background:white;padding:12px; }
    .skip-link:focus { top:10px; }
    .card { border:1px solid #e8ebf0; box-shadow:var(--shadow); border-radius:22px; padding:34px 38px; margin-bottom:22px; background:#fff; }
    .hero { grid-template-columns:minmax(0,1fr) 205px; padding:46px 42px 0; overflow:hidden; gap:18px 50px; }
    .eyebrow { display:block; color:var(--link); font-size:11px; font-weight:700; letter-spacing:.17em; margin-bottom:18px; }
    h1 { font-size:46px; letter-spacing:.08em; line-height:1.22; font-weight:700; margin:0 0 7px; }
    .english-name { font-family:Georgia,"Times New Roman",serif; font-size:26px; letter-spacing:.01em; color:#58677c; margin:0 0 19px; }
    .identity { font-size:14px; color:#526176; display:flex; align-items:center;gap:12px; }
    .degree { color:#2d5c98; background:#eef4fb; border:1px solid #e0eaf6; border-radius:6px;padding:3px 9px; font-weight:600; }
    .about-line { font-size:15px; color:#5c6879; line-height:1.95; max-width:645px; margin:16px 0 0; }
    .links { margin-top:23px;gap:10px; }
    .pill-link { padding:8px 15px;font-size:13px;border-radius:8px;border:1px solid #dfe5ed;background:#fff; }
    .pill-link.primary { background:var(--link);color:#fff;border-color:var(--link); }
    .pill-link.primary:hover { background:#214d87; }
    .portrait { width:164px;margin:0;justify-self:end;border:1px solid #dbe5f0;border-radius:16px;overflow:hidden;box-shadow:0 7px 24px rgba(29,48,77,.08);background:#f3f7fc; }
    .portrait img { display:block;width:100%;height:auto; }
    .hero-foot { grid-column:1/-1;border-top:1px solid var(--line);display:flex;gap:32px;margin-top:16px;padding:18px 0 21px;align-items:center; }
    .hero-foot p { font-size:12px;color:var(--muted);margin:0; }
    .hero-foot strong { font-size:19px;font-weight:600;color:#304a6b;margin-right:7px; }
    .hero-foot .focus-note { margin-left:auto;font-size:10px;letter-spacing:.12em;color:#8290a2; }
    .section-header { display:flex;align-items:center;justify-content:space-between;gap:20px;margin-bottom:22px; }
    .section-title { display:flex;align-items:baseline;gap:13px;flex-wrap:wrap; }
    h2 { border:0;padding:0;margin:0;font-size:22px;font-weight:650;letter-spacing:.02em; }
    .section-english { font-family:Georgia,serif;font-size:16px;color:#8a95a4; }
    .section-number { font-size:10px;letter-spacing:.1em;color:#9ca7b5; }
    .research-grid { display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:25px; }
    .research-item + .research-item { border-left:1px solid var(--line);padding-left:25px; }
    .research-icon { width:32px;height:32px;margin-bottom:14px;color:#557da9; }
    .research-item h3 { font-size:16px;line-height:1.5;font-weight:600;margin-bottom:9px; }
    .research-item p { font-size:13px;color:#728094;line-height:1.85; }
    .research-keywords { font-size:11px !important;color:#4f7199 !important;margin-top:11px !important; }
    .papers-header { margin-bottom:8px; }
    .paper-note { font-size:12px;color:#7e8999;margin:0 0 22px; }
    .download-link { font-size:12px;white-space:nowrap; }
    .publication-toolbar { display:flex;flex-wrap:wrap;align-items:center;gap:12px;justify-content:space-between;padding-bottom:21px;border-bottom:1px solid var(--line); }
    .filters { display:flex;flex-wrap:wrap;gap:6px; }
    button { font:inherit;cursor:pointer; }
    .filter { border:1px solid transparent;border-radius:7px;background:#f3f5f8;color:#67768a;padding:7px 11px;font-size:12px;line-height:1.5; }
    .filter[aria-pressed="true"] { background:#eaf1fb;border-color:#d9e6f7;color:#285b9d;font-weight:600; }
    .filter:hover { border-color:#c6d5e9; }
    .search-wrap { position:relative;flex:0 1 236px; }
    .search-wrap svg { position:absolute;left:11px;top:11px;width:15px;height:15px;pointer-events:none;color:#8994a4; }
    #paper-search { width:100%;border:1px solid #e1e6ed;border-radius:7px;background:#fff;padding:9px 10px 9px 34px;font:inherit;font-size:12px;color:var(--text); }
    #paper-search::placeholder { color:#8a95a5; }
    .results-count { font-size:11px;color:#8894a3;margin:15px 0 0; }
    .publication-card { grid-template-columns:47px minmax(0,1fr);gap:20px;padding:28px 0;border-bottom:1px solid var(--line);align-items:start; }
    .publication-card:last-child { padding-bottom:8px; }
    .publication-card[hidden] { display:none; }
    .pub-side { display:flex;flex-direction:column;padding-top:2px; }
    .pub-number { font-family:Georgia,serif;font-size:29px;line-height:1.2;color:#a8b5c6; }
    .pub-year { font-size:10px;color:#8c99a9;margin-top:5px; }
    .pub-rule { width:18px;height:2px;background:#d7e2f0;margin-top:14px; }
    .pub-heading { display:flex;flex-wrap:wrap;gap:9px 14px;align-items:center;margin-bottom:10px; }
    .journal { font-size:12px;letter-spacing:.015em;color:var(--link);font-weight:600; }
    .role { background:#f4f5f7;border-radius:4px;color:#7e8997;font-size:10px;padding:2px 7px;white-space:nowrap; }
    .lead-role { color:#3b659a;background:#edf3fb; }
    .item-title { font-size:17px;line-height:1.55;font-weight:600;letter-spacing:0; }
    .item-title a { color:#243246; }
    .item-title a:hover { color:var(--link);text-decoration:none; }
    .external-arrow { font-size:13px;color:#9aadc6;white-space:nowrap; }
    .authors { font-size:12px;line-height:1.8;margin-top:10px;color:#7b8798; }
    .me { color:#354a66;font-weight:650; }
    sup { font-size:9px;margin-left:2px; }
    .pub-meta { font-size:10px;color:#8b96a5;margin-top:5px;overflow-wrap:anywhere; }
    .meta-divider { margin:0 9px;color:#c1cad6; }
    .highlight { font-size:13px;line-height:1.85;color:#637185;margin:12px 0; }
    .pub-bottom { display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px 14px; }
    .pub-tags { display:flex;flex-wrap:wrap;gap:5px; }
    .tag { padding:3px 7px;margin:0;border-radius:4px;font-size:10px;color:#738093;background:#f5f6f8; }
    .mini-links { margin:0;gap:7px; }
    .mini-link { border-radius:5px;font-size:11px;padding:3px 9px;background:#fff; }
    .paper-detail { margin-top:10px; }
    .paper-detail summary { font-size:11px;color:#8a96a6; }
    .paper-detail p { font-size:12px;color:#6d7b8e;line-height:1.8; }
    #no-results { padding:38px 0;text-align:center;color:#6e7d90;font-size:14px; }
    #reset-search { margin:14px auto 0;display:block; }
    .contact-card { display:flex;justify-content:space-between;align-items:center;gap:24px;background:#f9fbfe; }
    .contact-card h2 { font-size:20px; }
    .contact-card p { font-size:13px;color:#7c899a;margin-top:10px; }
    .email-link { display:flex;align-items:center;gap:12px;background:#fff;border:1px solid #dce5f0;border-radius:9px;padding:13px 17px;font-size:14px;overflow-wrap:anywhere; }
    .email-link svg { width:17px;height:17px;flex-shrink:0; }
    .footer { max-width:1064px;margin:0 auto;padding:7px 20px 25px;display:flex;gap:12px;justify-content:space-between;font-size:10px;color:#8d99a8; }
    .footer a { color:#8d99a8; }
    .sr-only { position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0; }
    section { scroll-margin-top:24px; }
    @media (max-width:820px) {
      .container { padding:20px 20px 12px; }.top-nav { display:flex;margin-bottom:20px; }.nav-name { font-size:10px; }.nav-links { gap:16px; }
      .card { padding:28px; }.hero { padding:34px 28px 0;grid-template-columns:minmax(0,1fr) 120px;gap:18px 24px; }
      .portrait { width:112px;border-radius:12px; }
      h1 { font-size:37px; }.english-name { font-size:23px; }.identity { flex-wrap:wrap;gap:7px;font-size:12px; }.about-line { font-size:14px; }
      .hero-foot { gap:22px; }.hero-foot .focus-note { display:none; }.research-grid { gap:17px; }.research-item + .research-item { padding-left:17px; }
      .publication-card { grid-template-columns:35px minmax(0,1fr);gap:14px; }.pub-number { font-size:25px; }.item-title { font-size:16px; }
      .contact-card { flex-wrap:wrap; }.contact-card .email-link { font-size:13px; }
    }
    @media (max-width:560px) {
      .container { padding:17px 14px 10px; }.top-nav { margin:0 4px 18px; }.nav-name { display:none; }.nav-links { gap:21px;font-size:12px; }
      .card { padding:25px 21px;border-radius:17px;margin-bottom:16px; }.hero { grid-template-columns:1fr;position:relative;padding:29px 23px 0; }
      .eyebrow { font-size:9px;letter-spacing:.13em;margin-bottom:16px; }.hero h1 { font-size:35px; }.english-name { font-size:21px;margin-bottom:18px; }
      .portrait { position:absolute;right:25px;top:58px;width:68px;border-radius:9px; }
      .identity { font-size:12px;gap:8px; }.about-line { font-size:13px;line-height:1.9; }.pill-link { padding:8px 12px;font-size:12px; }
      .hero-foot { gap:19px;margin-top:6px;padding:16px 0 18px; }.hero-foot p { font-size:10px; }.hero-foot strong { font-size:17px;margin-right:5px; }
      .section-header { margin-bottom:20px;gap:12px; }.section-title { gap:10px; }h2 { font-size:19px; }.section-english { font-size:14px; }.section-number { display:none; }
      .research-grid { grid-template-columns:1fr;gap:18px; }.research-item { display:grid;grid-template-columns:28px 1fr;gap:0 13px; }.research-item + .research-item { padding:18px 0 0;border-left:0;border-top:1px solid var(--line); }
      .research-icon { grid-row:1/4;width:26px;height:26px;margin:2px 0; }.research-item h3 { margin-bottom:6px;font-size:15px; }.research-item p { font-size:12px; }.research-keywords { margin-top:7px !important; }
      .papers-header { align-items:flex-start;flex-direction:column;margin-bottom:10px; }.download-link { font-size:11px; }.paper-note { font-size:10px;line-height:1.8;margin-bottom:16px; }
      .publication-toolbar { gap:13px;padding-bottom:16px; }.filters { width:100%;gap:5px; }.filter { padding:7px 8px;font-size:10px; }.search-wrap { flex-basis:100%; }
      .publication-card { grid-template-columns:1fr;gap:10px;padding:24px 0; }.pub-side { flex-direction:row;align-items:center;gap:7px;padding:0; }.pub-number { font-size:19px; }.pub-year { margin:0;font-size:9px; }.pub-rule { margin:0 0 0 3px;width:30px;height:1px; }
      .pub-heading { gap:6px 8px;margin-bottom:9px; }.journal { font-size:11px; }.role { font-size:9px; }.item-title { font-size:15px;line-height:1.55; }.authors { font-size:11px;line-height:1.8; }
      .pub-meta { font-size:9px; }.highlight { font-size:12px; }.pub-bottom { gap:10px; }.tag { font-size:9px; }.mini-link { font-size:10px; }.paper-detail summary { font-size:10px; }
      .contact-card { gap:18px; }.contact-card h2 { font-size:19px; }.contact-card p { font-size:12px; }.email-link { padding:12px;width:100%;font-size:12px !important;gap:9px; }
      .footer { flex-direction:column;align-items:center;font-size:9px;gap:5px;padding:8px 16px 22px; }
    }
    @media (prefers-reduced-motion:reduce) { html { scroll-behavior:auto; }* { transition:none !important; } }
    @media print { body { background:white; }.container { max-width:100%;padding:0; }.top-nav,.publication-toolbar,.results-count,.paper-detail,.portrait,.footer { display:none; }.card { box-shadow:none;border:0;padding:20px 0; }.hero { display:block; }.hero-foot { display:none; }.publication-card { break-inside:avoid; }.publication-card[hidden] { display:grid; }.contact-card { break-inside:avoid; } }
'''

page = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="陈江龙（Jianglong Chen），博士研究生。研究关注天然产物、肾损伤与肾纤维化，结合药理实验与多组学分析探索相关机制。">
  <meta name="theme-color" content="#285ba0">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="陈江龙 | Jianglong Chen · 学术主页">
  <meta property="og:description" content="天然产物 · 肾脏疾病 · 多组学研究">
  <meta property="og:url" content="__SITE_URL__">
  <link rel="canonical" href="__SITE_URL__">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <title>陈江龙 | Jianglong Chen · 学术主页</title>
  <!-- Based on Xin-Jiaqi/minimal-academic-homepage; personalized content and layout. -->
  <style>''' + base_css + css + '''</style>
</head>
<body>
  <a class="skip-link" href="#about">跳至主要内容</a>
  <main class="container">
    <nav class="top-nav" aria-label="主导航">
      <a class="nav-brand" href="#about" aria-label="陈江龙，首页"><span class="brand-mark" aria-hidden="true">JC</span><span class="nav-name">JIANGLONG CHEN</span></a>
      <div class="nav-links"><a href="#research">研究方向</a><a href="#publications">学术论文</a><a href="#contact">联系</a></div>
    </nav>

    <section class="card hero" id="about" aria-labelledby="name">
      <div>
        <span class="eyebrow">ACADEMIC HOMEPAGE / 学术主页</span>
        <h1 id="name">陈江龙</h1>
        <p class="english-name" lang="en">Jianglong Chen</p>
        <div class="identity"><span class="degree">博士研究生</span><span>天然产物药理 · 肾脏疾病研究</span></div>
        <p class="about-line">我的研究围绕<strong>天然产物对肾损伤与肾纤维化的作用机制</strong>展开，结合药理实验、网络药理学与多组学分析，探索肾脏保护相关的活性物质与分子通路。</p>
        <div class="links"><a class="pill-link primary" href="#publications">浏览研究论文 <span aria-hidden="true">&nbsp;↓</span></a><a class="pill-link" href="mailto:cjl2913183067@163.com">邮件联系 <span aria-hidden="true">&nbsp;↗</span></a></div>
      </div>
      <figure class="portrait"><img src="assets/jianglong-chen.jpg" alt="陈江龙的个人照片" width="307" height="378" fetchpriority="high"></figure>
      <div class="hero-foot"><p><strong>06</strong>本页收录论文</p><p><strong>04</strong>第一 / 共同第一作者</p><span class="focus-note">NATURAL PRODUCTS & RENAL RESEARCH</span></div>
    </section>

    <section class="card" id="research" aria-labelledby="research-title">
      <div class="section-header"><div class="section-title"><h2 id="research-title">研究方向</h2><span class="section-english" lang="en">Research interests</span></div><span class="section-number">01 / RESEARCH</span></div>
      <div class="research-grid">
        <div class="research-item">
          <svg class="research-icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><path d="M6 25C4 12 13 5 26 5c0 14-7 22-20 20Z"/><path d="M6 26 22 10M11 21l-1-7M16 16h7"/></svg>
          <h3>天然产物与肾脏保护</h3><p>关注白羊解、七叶内酯等天然产物，探索活性成分、体内分布与潜在药理作用。</p><p class="research-keywords">Arundina graminifolia · Esculetin</p>
        </div>
        <div class="research-item">
          <svg class="research-icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><circle cx="7" cy="7" r="3"/><circle cx="25" cy="8" r="3"/><circle cx="16" cy="17" r="3"/><circle cx="8" cy="26" r="3"/><circle cx="25" cy="26" r="3"/><path d="m9 10 5 5m4-1 5-4m-9 9-4 5m8-5 5 5"/></svg>
          <h3>肾损伤与纤维化机制</h3><p>围绕 AKI-to-CKD 进程，研究炎症、氧化应激与纤维化相关信号通路。</p><p class="research-keywords">TGF-β · PI3K-AKT/mTOR · NF-κB</p>
        </div>
        <div class="research-item">
          <svg class="research-icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><path d="M5 5v22h23M10 21l6-8 5 4 6-10"/><circle cx="10" cy="21" r="1.5" fill="currentColor"/><circle cx="16" cy="13" r="1.5" fill="currentColor"/><circle cx="21" cy="17" r="1.5" fill="currentColor"/><circle cx="27" cy="7" r="1.5" fill="currentColor"/></svg>
          <h3>多组学与计算分析</h3><p>整合转录组、代谢组与单细胞数据，结合网络药理学和机器学习探索疾病相关机制。</p><p class="research-keywords">Transcriptomics · Metabolomics · scRNA-seq</p>
        </div>
      </div>
    </section>

    <section class="card" id="publications" aria-labelledby="publications-title">
      <div class="section-header papers-header"><div class="section-title"><h2 id="publications-title">学术论文</h2><span class="section-english" lang="en">Publications</span></div><a class="download-link" href="assets/citations/jianglong-chen-publications.bib" download>下载全部引用 · BibTeX ↓</a></div>
      <p class="paper-note"><strong>加粗</strong>表示本人署名；† 表示共同贡献。作者顺序及贡献标注依据论文原文。</p>
      <div class="publication-toolbar">
        <div class="filters" role="group" aria-label="按研究主题或作者身份筛选"><button class="filter" type="button" data-filter="all" aria-pressed="true">全部 6</button><button class="filter" type="button" data-filter="lead" aria-pressed="false">第一 / 共一 4</button><button class="filter" type="button" data-filter="natural" aria-pressed="false">天然产物</button><button class="filter" type="button" data-filter="omics" aria-pressed="false">多组学分析</button></div>
        <div class="search-wrap"><label class="sr-only" for="paper-search">搜索论文标题、期刊或关键词</label><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10" cy="10" r="6.5"/><path d="m15 15 5 5"/></svg><input type="search" id="paper-search" placeholder="搜索标题、期刊、关键词…" autocomplete="off"></div>
      </div>
      <p class="results-count" id="results-count" role="status" aria-live="polite">显示全部 6 篇论文 · 2026</p>
      <div id="paper-list">''' + '\n'.join(rows) + '''</div>
      <div id="no-results" hidden>没有找到匹配的论文。<button class="filter" type="button" id="reset-search">清除搜索与筛选</button></div>
    </section>

    <section class="card contact-card" id="contact" aria-labelledby="contact-title"><div><div class="section-title"><h2 id="contact-title">学术交流</h2><span class="section-english" lang="en">Get in touch</span></div><p>欢迎围绕天然产物、肾脏疾病与多组学研究交流。</p></div><a class="email-link" href="mailto:cjl2913183067@163.com"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/></svg>cjl2913183067@163.com <span aria-hidden="true">↗</span></a></section>
  </main>
  <footer class="footer"><span>© 2026 陈江龙 · Jianglong Chen</span><span>更新于 2026.10 · <a href="https://github.com/Xin-Jiaqi/minimal-academic-homepage" target="_blank" rel="noopener noreferrer">Minimal Academic Homepage</a></span></footer>
  <script>
    (() => {
      const search = document.getElementById('paper-search');
      const buttons = [...document.querySelectorAll('[data-filter]')];
      const papers = [...document.querySelectorAll('.publication-card')];
      let selected = 'all';
      function update() {
        const terms = search.value.trim().toLocaleLowerCase().split(/\\s+/).filter(Boolean);
        let count = 0;
        for (const paper of papers) {
          const matchesFilter = selected === 'all' || (selected === 'lead' ? paper.dataset.lead === 'true' : paper.dataset.category === selected);
          const matchesSearch = terms.every(term => paper.dataset.search.includes(term));
          paper.hidden = !(matchesFilter && matchesSearch);
          if (!paper.hidden) count++;
        }
        for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.filter === selected));
        document.getElementById('results-count').textContent = `显示 ${count} / ${papers.length} 篇论文 · 2026`;
        document.getElementById('no-results').hidden = count !== 0;
      }
      buttons.forEach(button => button.addEventListener('click', () => { selected = button.dataset.filter; update(); }));
      search.addEventListener('input', update);
      document.getElementById('reset-search').addEventListener('click', () => { selected = 'all'; search.value = ''; update(); search.focus(); });
    })();
  </script>
</body>
</html>
'''
if SITE_URL == '/':
    page = page.replace('  <meta property="og:url" content="__SITE_URL__">\n', '').replace('  <link rel="canonical" href="__SITE_URL__">\n', '')
else:
    page = page.replace('__SITE_URL__', e(SITE_URL, quote=True))
(OUT / 'index.html').write_text(page, encoding='utf-8')
(OUT / '.nojekyll').write_text('', encoding='utf-8')
(OUT / 'assets' / 'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="17" fill="#285ba0"/><text x="32" y="44" text-anchor="middle" fill="white" font-family="Georgia,serif" font-size="35">JC</text></svg>', encoding='utf-8')
print(f'Built {OUT / "index.html"}: {len(papers)} publications, {sum(p["lead"] for p in papers)} first/co-first author papers.')
