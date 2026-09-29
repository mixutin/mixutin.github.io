"""Generate the committed, dependency-free portfolio pages. Python 3.10+."""
from pathlib import Path
from html import escape
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/projects.json').read_text(encoding='utf-8'))
BASE = 'https://mixutin.github.io'
CRYPTO = 'https://cryptohack.org/user/nurminen/'
GITHUB = 'https://github.com/mixutin'
TEAM = 'https://ctftime.org/team/387399'
ICONS = {
    'arrow': '<path d="M7 17 17 7M7 7h10v10"/>',
    'right': '<path d="M4 12h16m-6-6 6 6-6 6"/>',
    'code': '<path d="m8 6-6 6 6 6m8-12 6 6-6 6M14 4l-4 16"/>',
    'shield': '<path d="m12 2 8 3v6c0 5-8 11-8 11S4 16 4 11V5z"/><path d="m8 11 3 3 5-6"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 6.5c4 2 10 2 14 0M5 17.5c4-2 10-2 14 0"/>',
    'flag': '<path d="M5 22V3m0 1c4-5 10 5 15 0v10c-5 5-11-5-15 0"/>',
    'cpu': '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 1v5m6-5v5M9 18v5m6-5v5M1 9h5m-5 6h5m12-6h5m-5 6h5"/><rect x="9" y="9" width="6" height="6" rx="1"/>',
    'spark': '<path d="m12 1 2.5 8.5L23 12l-8.5 2.5L12 23l-2.5-8.5L1 12l8.5-2.5z"/><circle cx="12" cy="12" r="8"/>',
    'layers': '<path d="m12 2 11 6-11 6L1 8zM1 12l11 6 11-6M1 16l11 6 11-6"/>',
    'wave': '<path d="M2 10v4m4-7v10m4-15v20m4-17v14m4-11v8m4-6v4"/>',
    'book': '<path d="M12 5v17M2 3c4-1 7 0 10 2 3-2 6-3 10-2v16c-4-1-7 0-10 2-3-2-6-3-10-2z"/>',
    'github': '<path d="M9 20c-5 1-5-3-7-3m14 5v-4a3 3 0 0 0-1-2.4c3.5-.4 7-1.7 7-7A5.5 5.5 0 0 0 20.5 5a5 5 0 0 0-.1-4S19 1 16 3a13 13 0 0 0-7 0C6 1 4.6 1 4.6 1A5 5 0 0 0 4.5 5 5.5 5.5 0 0 0 3 8.6c0 5.3 3.5 6.6 7 7A3 3 0 0 0 9 18v4"/>',
    'chat': '<path d="M21 11a8 8 0 0 1-8 8H8l-6 3 2-6a8 8 0 0 1-1-5 9 9 0 0 1 18 0Z"/><path d="M7 10h10M7 14h6"/>',
    'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>'
}

def icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

def url(lang, page=''):
    return ('/fi/' if lang == 'fi' else '/') + (page.strip('/') + '/' if page else '')

def tr(lang, en, fi):
    return fi if lang == 'fi' else en

def link(href, label, cls='text-link', arrow='arrow'):
    return f'<a class="{cls}" href="{escape(href, quote=True)}">{label}{icon(arrow)}</a>'

def scene(lang, mode='globe', badge=False):
    name = {'globe': 'NETWORK GLOBE', 'shield': 'SECURITY SHIELD', 'orbit': 'CONNECTED SYSTEMS'}[mode]
    return f'''<div class="scene" data-scene="{mode}">
<div class="scene-grid" aria-hidden="true"></div><div class="scene-glow" aria-hidden="true"></div>
<div class="scene-fallback" aria-hidden="true"></div><canvas aria-hidden="true"></canvas>
<button class="motion" type="button" aria-pressed="false" data-motion-toggle data-pause="{tr(lang,'Pause motion','Pysäytä liike')}" data-resume="{tr(lang,'Resume motion','Jatka liikettä')}">{tr(lang,'Pause motion','Pysäytä liike')}</button>
{f'<div class="scene-badge">{icon("shield")}<div><strong>CRYPTOHACK · #1</strong><small>GLOBALLY &amp; IN FINLAND</small></div></div>' if badge else ''}
</div>'''

def nav(lang, page):
    items = [('', 'Home', 'Etusivu'), ('projects', 'Projects', 'Projektit'), ('ctf', 'CTF & security', 'CTF & tietoturva'), ('about', 'About', 'Minusta'), ('contact', 'Contact', 'Yhteys')]
    links = ''.join(f'<a href="{url(lang,slug)}"'+ (' aria-current="page"' if page == slug else '') + f'>{tr(lang,en,fi)}</a>' for slug,en,fi in items)
    return f'''<a class="skip" href="#main">{tr(lang,'Skip to content','Siirry sisältöön')}</a>
<header class="header"><div class="wrap header-inner">
<a class="brand" href="{url(lang)}" aria-label="{tr(lang,'mixutin, home','mixutin, etusivu')}"><span class="brand-mark">{icon('code')}</span>mixutin<span aria-hidden="true">.</span></a>
<nav class="nav" id="navigation" aria-label="{tr(lang,'Main navigation','Päävalikko')}">{links}</nav>
<div class="header-tools"><nav class="language" aria-label="{tr(lang,'Language','Kieli')}"><a lang="en" hreflang="en" href="{url('en',page)}"{' aria-current="page"' if lang == 'en' else ''}>EN</a><span aria-hidden="true">/</span><a lang="fi" hreflang="fi" href="{url('fi',page)}"{' aria-current="page"' if lang == 'fi' else ''}>FI</a></nav><a class="github-link" href="{GITHUB}">GitHub ↗</a><button class="menu" type="button" aria-label="{tr(lang,'Toggle navigation','Avaa tai sulje valikko')}" aria-expanded="false" aria-controls="navigation">{icon('menu')}</button></div></div></header>'''

def footer(lang):
    return f'''<footer class="footer"><div class="wrap"><div class="footer-top"><div><a class="brand" href="{url(lang)}">mixutin.</a><p>{tr(lang,'Security. Systems. A little curiosity.','Tietoturvaa. Järjestelmiä. Uteliaisuutta.')}</p></div><nav class="footer-links" aria-label="{tr(lang,'Footer','Alatunniste')}"><a href="{GITHUB}">GitHub ↗</a><a href="{CRYPTO}">CryptoHack ↗</a><a href="{url(lang,'writeups')}">Writeups</a><a href="{url(lang,'blog')}">Blog</a></nav></div><div class="footer-bottom"><span>© 2026 Mikael Nurminen · 0x11a / Mixutin</span><span>{tr(lang,'No analytics. No tracking cookies.','Ei analytiikkaa. Ei seurantaevästeitä.')} · <a href="/.well-known/security.txt">security.txt</a> · <a href="/sitemap.xml">Sitemap</a></span></div></div></footer>'''

def shell(lang, page, title, description, body, noindex=False):
    path = url(lang,page)
    csp = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'"
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp}"><meta name="referrer" content="strict-origin-when-cross-origin">
<title>{escape(title)} · Mikael Nurminen / mixutin</title><meta name="description" content="{escape(description,quote=True)}"><meta name="author" content="Mikael Nurminen"><meta name="color-scheme" content="dark"><meta name="theme-color" content="#050b18">
{'<meta name="robots" content="noindex">' if noindex else ''}<link rel="canonical" href="{BASE}{path}"><link rel="alternate" hreflang="en" href="{BASE}{url('en',page)}"><link rel="alternate" hreflang="fi" href="{BASE}{url('fi',page)}"><link rel="alternate" hreflang="x-default" href="{BASE}{url('en',page)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="stylesheet" href="/assets/css/portfolio.css">
<meta property="og:type" content="website"><meta property="og:site_name" content="mixutin · Mikael Nurminen"><meta property="og:title" content="{escape(title,quote=True)} · mixutin"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:locale" content="{'fi_FI' if lang == 'fi' else 'en_GB'}"><meta property="og:image" content="{BASE}/assets/og/og-home{'-fi' if lang == 'fi' else ''}.png"><meta name="twitter:card" content="summary_large_image">
<script src="/assets/js/site.js" defer></script><script src="/assets/js/scene.js" type="module"></script></head><body>{nav(lang,page)}<main id="main">{body}</main>{footer(lang)}</body></html>
'''

def project_card(p,lang,i,compact=False):
    art = f'''<div class="mini-terminal"><div class="terminal-bar"><i></i><i></i><i></i></div><div class="terminal-lines">VIBRIX / x86_64<br>UEFI → kernel<br><b>vibrix&gt; help</b><span class="cursor"></span></div></div>''' if p['slug']=='vibrix' else icon(p['icon'])
    links = link(GITHUB+'/'+p['repo'],'GitHub')
    if p.get('detail'):
        links += link(url(lang,'projects/'+p['slug']),tr(lang,'Case study','Esittely'))
    elif p['website']:
        links += link(p['website'],tr(lang,'Website','Sivusto'))
    tags=''.join(f'<span>{escape(t)}</span>' for t in p['tags'])
    detail='' if compact else f'<details><summary>{tr(lang,"Development status","Kehitysvaihe")}</summary><p>{escape(p["note"][lang])} <a href="{p["source"]}">{tr(lang,"Source ↗","Lähde ↗")}</a></p></details>'
    search=escape(' '.join([p['name'],p['description'][lang],*p['tags']]),quote=True)
    return f'''<article class="project-card" data-project data-category="{p['category']}" data-search="{search}"><div class="project-art {p['slug']}" aria-hidden="true"><span class="art-label">{p['category'].upper()}</span>{art}<span class="art-index">0{i+1} / OPEN SOURCE</span></div><div class="project-body"><span class="status">{escape(p['status'][lang])}</span><h3><a href="{GITHUB}/{p['repo']}">{escape(p['name'])}</a></h3><p>{escape(p['description'][lang])}</p><div class="tags">{tags}</div>{detail}<div class="project-links">{links}</div></div></article>'''

def cta(lang):
    return f'''<section class="wrap section" id="contact"><div class="cta"><div><p class="section-label">{tr(lang,'NEXT CONNECTION','SEURAAVA YHTEYS')}</p><h2>{tr(lang,"Something worth building?","Jotain rakentamisen arvoista?")}</h2><p>{tr(lang,"An interesting security problem, an open-source idea, or a game worth preserving. Let's talk.","Kiinnostava tietoturvaongelma, avoimen lähdekoodin idea tai säilyttämisen arvoinen peli. Jutellaan.")}</p></div>{link(url(lang,'contact'),tr(lang,'Get in touch','Ota yhteyttä'),'button primary','right')}</div></section>'''

def rank_strip(lang):
    return f'''<div class="wrap" id="ctf"><div class="achievement-strip"><a class="achievement" href="{CRYPTO}"><strong>#1</strong><div><span class="rank-label">Globally</span><small>CryptoHack</small></div></a><a class="achievement" href="{CRYPTO}"><strong>#1</strong><div><span class="rank-label">In Finland</span><small>CryptoHack</small></div></a><a class="achievement" href="{TEAM}"><strong class="word">THEM?!</strong><div><span class="rank-label">CTF team</span><small>Crypto &amp; rev</small></div></a><a class="achievement" href="{url(lang,'projects')}"><strong class="word">BUILD</strong><div><span class="rank-label">{tr(lang,'In the open','Avoimesti')}</span><small>{tr(lang,'From research to code','Tutkimuksesta koodiin')}</small></div></a></div><p class="snapshot">{tr(lang,'Portfolio snapshot · September 2026. Rankings can change.','Portfolion tilanne · syyskuu 2026. Sijoitukset voivat muuttua.')} <a href="{CRYPTO}">{tr(lang,'Current CryptoHack profile ↗','Ajantasainen CryptoHack-profiili ↗')}</a></p></div>'''

def home(lang):
    cards=''.join(project_card(p,lang,i,True) for i,p in enumerate(DATA['projects'][:3]))
    body=f'''<section class="wrap hero"><div class="hero-copy"><p class="eyebrow">0x11a / MIXUTIN · {tr(lang,'BASED IN FINLAND','SUOMESTA')}</p><h1>Mikael<br><span class="gradient">Nurminen.</span></h1><p class="hero-role">{tr(lang,'Security researcher. Builder by nature.','Tietoturvan tutkija. Utelias rakentaja.')}</p><p class="lead">{tr(lang,'I take systems apart to understand them — then build something better. Cryptography, reverse engineering and open-source projects, from Finland to the world.','Puran järjestelmiä ymmärtääkseni niitä — ja rakennan tilalle parempaa. Kryptografiaa, takaisinmallinnusta ja avoimen lähdekoodin projekteja Suomesta maailmalle.')}</p><div class="actions">{link(url(lang,'projects'),tr(lang,'Explore my projects','Tutustu projekteihin'),'button primary','right')}{link(url(lang,'ctf'),tr(lang,'CTF & security','CTF & tietoturva'),'button')}</div><div class="hero-foot"><span>CRYPTOGRAPHY</span><span>REVERSE ENGINEERING</span><span>OPEN SOURCE</span></div></div>{scene(lang,'globe',True)}</section>{rank_strip(lang)}
<section class="wrap section" id="projects"><div class="section-head"><div><p class="section-label"><span>01 /</span>{tr(lang,'SELECTED WORK','VALITUT PROJEKTIT')}</p><h2>{tr(lang,'Built with curiosity.','Uteliaisuudesta koodiksi.')}</h2></div>{link(url(lang,'projects'),tr(lang,'All projects','Kaikki projektit'),'text-link','right')}</div><div class="project-grid featured">{cards}</div></section>
<section class="section" id="about"><div class="wrap split"><div class="feature-copy"><p class="section-label"><span>02 /</span>{tr(lang,'BEHIND THE HANDLE','NIMIMERKIN TAKANA')}</p><h2>{tr(lang,'Understand the system.<br><span class="gradient">Challenge the assumptions.</span>','Ymmärrä järjestelmä.<br><span class="gradient">Haasta oletukset.</span>')}</h2><p>{tr(lang,'The interesting part is rarely on the surface. I follow the details: how a cipher fails, what a binary is doing, and how to keep software useful long after its original servers disappear.','Kiinnostavin osa löytyy harvoin pinnalta. Seuraan yksityiskohtia: miksi salaus pettää, mitä ohjelma todella tekee ja miten ohjelmisto pidetään elossa alkuperäisten palvelinten jälkeen.')}</p>{link(url(lang,'about'),tr(lang,'A little more about me','Lisää minusta'),'text-link','right')}</div><div id="skills"><div class="skill-row"><span class="icon-box">{icon('shield')}</span><div><h3>{tr(lang,'Cryptography & CTFs','Kryptografia & CTF')}</h3><p>{tr(lang,'Hands-on problems. Careful reasoning. Competing with THEM?!.','Käytännön ongelmia ja tarkkaa päättelyä. Kilpailen THEM?!-tiimissä.')}</p></div></div><div class="skill-row"><span class="icon-box">{icon('cpu')}</span><div><h3>{tr(lang,'Systems & open source','Järjestelmät & avoin lähdekoodi')}</h3><p>{tr(lang,'Native tools, operating-system experiments and software built in public.','Natiiveja työkaluja, käyttöjärjestelmäkokeiluja ja avoimesti kehitettävää ohjelmistoa.')}</p></div></div><div class="skill-row"><span class="icon-box">{icon('layers')}</span><div><h3>{tr(lang,'Reverse engineering & preservation','Takaisinmallinnus & säilyttäminen')}</h3><p>{tr(lang,'Understanding software so games and overlooked media are not lost.','Ohjelmistojen ymmärtämistä, jotta pelit ja unohdettu media eivät katoa.')}</p></div></div></div></div></section>{cta(lang)}'''
    return shell(lang,'',tr(lang,'Security, systems & open source','Tietoturva, järjestelmät & avoin lähdekoodi'),tr(lang,'Mikael Nurminen / mixutin / 0x11a. Cryptography, CTFs, reverse engineering and public software projects. CryptoHack #1 globally and in Finland.','Mikael Nurminen / mixutin / 0x11a. Kryptografiaa, CTF-kilpailuja, takaisinmallinnusta ja julkisia projekteja. CryptoHack #1 Globally ja #1 In Finland.'),body)

def heading(lang,page,title,desc,mode=None):
    crumb=f'<p class="breadcrumb"><a href="{url(lang)}">{tr(lang,"Home","Etusivu")}</a><span>/</span>{tr(lang,page.capitalize(),{"projects":"Projektit","ctf":"CTF","about":"Minusta","contact":"Yhteys","writeups":"Writeups","blog":"Blogi"}.get(page,page))}</p>'
    text=f'<div>{crumb}<p class="eyebrow">{tr(lang,"MIXUTIN / PORTFOLIO","MIXUTIN / PORTFOLIO")}</p><h1>{title}</h1><p class="lead">{desc}</p></div>'
    return f'<section class="wrap page-hero{" with-scene" if mode else ""}">{text}{scene(lang,mode) if mode else ""}</section>'

def projects(lang):
    categories=[('all','All projects','Kaikki'),('systems','Systems','Järjestelmät'),('desktop','Desktop','Työpöytä'),('preservation','Preservation','Säilyttäminen'),('tools','Tools','Työkalut')]
    buttons=''.join(f'<button class="filter" type="button" data-filter="{s}" aria-pressed="{str(s=="all").lower()}">{tr(lang,en,fi)}</button>' for s,en,fi in categories)
    cards=''.join(project_card(p,lang,i) for i,p in enumerate(DATA['projects']))
    body=heading(lang,'projects',tr(lang,'Ideas into<br><span class="gradient">working code.</span>','Ideoista<br><span class="gradient">toimivaksi koodiksi.</span>'),tr(lang,'A selection of my public GitHub projects. Systems, desktop experiences and game preservation — with the development status kept in view.','Valikoima julkisia GitHub-projektejani. Järjestelmiä, työpöytäsovelluksia ja pelien säilyttämistä — kehitysvaihe avoimesti näkyvillä.'))
    body+=f'''<section class="wrap compact-section" data-project-browser><div class="filter-bar" data-filter-controls hidden><div class="filters" role="group" aria-label="{tr(lang,'Filter projects','Suodata projekteja')}">{buttons}</div><label class="search-label">{tr(lang,'Search projects','Hae projekteja')}<input type="search" data-project-search placeholder="{tr(lang,'Name, language, technology…','Nimi, kieli, teknologia…')}" autocomplete="off"></label></div><p class="results-count" aria-live="polite" data-result-count data-label="{tr(lang,'projects','projektia')}">5 {tr(lang,'projects','projektia')}</p><div class="project-grid">{cards}</div><div class="empty" data-empty hidden><h2>{tr(lang,'No matching projects.','Ei hakutuloksia.')}</h2><p>{tr(lang,'Try another keyword or clear the filters.','Kokeile toista hakusanaa tai tyhjennä suodattimet.')}</p><button class="button" type="button" data-reset>{tr(lang,'Reset filters','Tyhjennä suodattimet')}</button></div><p class="archive-note">{tr(lang,'Public repository selection checked on 29 September 2026. Private repositories and unrelated upstream forks are not listed.','Julkisten projektien valikoima tarkistettu 29.9.2026. Yksityisiä repositorioita tai muiden projektien tavallisia kopioita ei ole listattu.')} <a href="{GITHUB}?tab=repositories">GitHub ↗</a></p></section>{cta(lang)}'''
    return shell(lang,'projects',tr(lang,'Projects','Projektit'),tr(lang,'Public projects by mixutin: Vibrix, Lumina, Mallow, Dauntless Revived and JKI / Jake.','mixutinin julkiset projektit: Vibrix, Lumina, Mallow, Dauntless Revived ja JKI / Jake.'),body)

def ctf(lang):
    body=heading(lang,'ctf',tr(lang,'Break patterns.<br><span class="gradient">Capture flags.</span>','Löydä heikkous.<br><span class="gradient">Ratkaise haaste.</span>'),tr(lang,'Cryptography and reverse engineering are where I go deep. I compete as 0x11a / Mixutin with THEM?! and turn difficult problems into things I can explain.','Kryptografia ja takaisinmallinnus ovat vahvuuksiani. Kilpailen nimillä 0x11a / Mixutin THEM?!-tiimissä ja puran vaikeat ongelmat ymmärrettäviksi ratkaisuiksi.'),'shield')
    rank=''.join(f'<article class="rank-card">{icon(i)}<strong>#1</strong><h2>{t}</h2><p>CRYPTOHACK · SEPTEMBER 2026</p></article>' for i,t in [('globe','Globally'),('flag','In Finland')])
    topics=[('Cryptography','Kryptografia','RSA, elliptic curves, lattices and the details that make or break a cryptosystem.','RSA, elliptiset käyrät, hilat ja yksityiskohdat, jotka ratkaisevat salausjärjestelmän turvallisuuden.'),('Reverse engineering','Takaisinmallinnus','Binaries, program behaviour and reconstructing the reasoning behind an implementation.','Binäärit, ohjelmien käyttäytyminen ja toteutuksen taustalla olevan logiikan selvittäminen.'),('Write it down','Ratkaisu talteen','Clear notes and reproducible explanations after the competition allows publication.','Selkeät muistiinpanot ja toistettavat selitykset kilpailun julkaisusääntöjen sallimissa rajoissa.')]
    topic=''.join(f'<article class="topic"><span class="number">0{i+1} /</span><h3>{tr(lang,en,fi)}</h3><p>{tr(lang,de,df)}</p></article>' for i,(en,fi,de,df) in enumerate(topics))
    body+=f'''<section class="wrap compact-section"><p class="section-label"><span>01 /</span>CRYPTOHACK</p><h2>{tr(lang,'On the scoreboard.','Tulostaululla.')}</h2><div class="rank-grid">{rank}</div><p class="snapshot">{tr(lang,'Ranking snapshot supplied by Mikael for this portfolio, September 2026; not a live ranking feed.','Mikaelin portfolioon ilmoittama sijoitustilanne, syyskuu 2026; ei reaaliaikainen tulostaulu.')} <a href="{CRYPTO}">{tr(lang,'View the current profile ↗','Katso ajantasainen profiili ↗')}</a></p></section>
<section class="section"><div class="wrap split"><div><p class="section-label"><span>02 /</span>THEM?!</p><h2>{tr(lang,'A team sport.<br>A curious mindset.','Joukkuepeliä.<br>Utelias mieli.')}</h2><p class="section-intro">{tr(lang,'I compete with THEM?!. Cryptography and reverse engineering are my main categories, with a focus on understanding the problem rather than just collecting the flag.','Kilpailen THEM?!-tiimissä. Pääkategoriani ovat kryptografia ja takaisinmallinnus. Tavoitteena on ymmärtää ongelma, ei vain kerätä lippua.')}</p><div class="actions">{link(TEAM,'THEM?! / CTFtime','button')}{link(CRYPTO,'CryptoHack','button')}</div></div><div class="profile-panel"><p class="section-label">PLAYER PROFILE</p><dl><div><dt>Handle</dt><dd>0x11a / Mixutin</dd></div><div><dt>{tr(lang,'Team','Tiimi')}</dt><dd>THEM?!</dd></div><div><dt>{tr(lang,'Focus','Painopiste')}</dt><dd>Crypto / Rev</dd></div><div><dt>CryptoHack</dt><dd>nurminen</dd></div></dl></div></div></section><section class="wrap section"><p class="section-label"><span>03 /</span>{tr(lang,'THE CRAFT','OSAAMINEN')}</p><h2>{tr(lang,'Think deeper. Keep learning.','Ajattele syvemmälle. Opi lisää.')}</h2><div class="topic-grid">{topic}</div><div class="actions">{link(url(lang,'writeups'),tr(lang,'Read the writeups index','Avaa writeup-hakemisto'),'button','right')}{link(url(lang,'blog'),'Blog','button')}</div></section>'''
    return shell(lang,'ctf',tr(lang,'CTF & security','CTF & tietoturva'),tr(lang,'0x11a / Mixutin: cryptography, reverse engineering and THEM?!. CryptoHack #1 Globally and #1 In Finland.','0x11a / Mixutin: kryptografia, takaisinmallinnus ja THEM?!. CryptoHack #1 Globally ja #1 In Finland.'),body)

def about(lang):
    body=heading(lang,'about',tr(lang,'Curiosity is<br><span class="gradient">the common thread.</span>','Kaiken taustalla<br><span class="gradient">on uteliaisuus.</span>'),tr(lang,'I am Mikael Nurminen, known online as mixutin and 0x11a. I work at the intersection of security, systems and software preservation.','Olen Mikael Nurminen, verkossa mixutin ja 0x11a. Työskentelen tietoturvan, järjestelmien ja ohjelmistojen säilyttämisen parissa.'))
    body+=f'''<section class="wrap section"><div class="split"><div class="prose"><p class="section-label">BEHIND / 0x11a</p><h2>{tr(lang,'Taking things apart.<br>Making things possible.','Puran osiin.<br>Rakennan mahdollisuuksia.')}</h2><p>{tr(lang,'My favourite part of a problem is finding out how it really works. That might mean studying a cipher, reading machine code or tracing what a game client expects from a server.','Suosikkiosani ongelmassa on selvittää, miten se todella toimii. Se voi tarkoittaa salauksen tutkimista, konekoodin lukemista tai peliasiakkaan palvelinodotusten selvittämistä.')}</p><p>{tr(lang,'Game and media preservation matter to me. Software should not disappear just because a service goes offline. I also build native desktop tools, backends and systems-level experiments.','Pelien ja median säilyttäminen on minulle tärkeää. Ohjelmiston ei pitäisi kadota vain siksi, että palvelu suljetaan. Rakennan myös natiiveja työpöytätyökaluja, palvelimia ja matalan tason järjestelmäkokeiluja.')}</p><p>{tr(lang,'CTF competitions keep me learning. Open-source projects give those ideas somewhere practical to go.','CTF-kilpailut pitävät minut oppimassa. Avoimen lähdekoodin projektit vievät ideat käytäntöön.')}</p></div><aside class="profile-panel"><div class="profile-top"><span class="avatar-monogram" aria-hidden="true">0x11a</span><div><h2>Mikael Nurminen</h2><p>mixutin / 0x11a</p></div></div><dl><div><dt>{tr(lang,'Based in','Sijainti')}</dt><dd>{tr(lang,'Finland','Suomi')}</dd></div><div><dt>CTF</dt><dd>THEM?!</dd></div><div><dt>GitHub</dt><dd><a href="{GITHUB}">@mixutin ↗</a></dd></div><div><dt>{tr(lang,'Focus','Painopiste')}</dt><dd>Crypto · Rev · Systems</dd></div></dl><div class="actions">{link(url(lang,'contact'),tr(lang,'Connect with me','Ota yhteyttä'),'button','right')}</div></aside></div></section>
<section class="section" id="skills"><div class="wrap"><p class="section-label">TOOLKIT /</p><h2>{tr(lang,'Different tools. One mindset.','Eri työkalut. Sama ajattelutapa.')}</h2><div class="topic-grid"><article class="topic"><span class="icon-box">{icon('shield')}</span><h3>{tr(lang,'Security & analysis','Tietoturva & analyysi')}</h3><p>Cryptography · Python · Binary analysis · x86-64 · Windows PE · Reverse engineering</p></article><article class="topic"><span class="icon-box">{icon('cpu')}</span><h3>{tr(lang,'Systems & desktop','Järjestelmät & työpöytä')}</h3><p>Rust · C · C++ · Swift · Linux · macOS · UEFI · QEMU · Tauri</p></article><article class="topic"><span class="icon-box">{icon('code')}</span><h3>{tr(lang,'Backends & creative tools','Palvelimet & luovat työkalut')}</h3><p>TypeScript · Node.js · SQLite · GitHub Actions · Unity · Roblox · Blender · MCP</p></article></div></div></section>
<section class="wrap section" id="workstation"><div class="split"><div id="ai-security"><p class="section-label">WORKFLOW /</p><h2>{tr(lang,'Build. Test. Understand.','Rakenna. Testaa. Ymmärrä.')}</h2><p class="section-intro">{tr(lang,'I use AI-assisted development alongside debugging, testing and direct inspection of the code. A good-looking interface or a green build is a starting point, not proof that every feature works.','Käytän tekoälyavusteista kehitystä virheenjäljityksen, testaamisen ja koodin tarkastelun rinnalla. Hyvännäköinen käyttöliittymä tai vihreä koonti on lähtökohta, ei todiste kaikkien ominaisuuksien toimivuudesta.')}</p></div><div><div class="skill-row"><span class="icon-box">{icon('book')}</span><div><h3>{tr(lang,'Make the state visible','Kehitysvaihe näkyviin')}</h3><p>{tr(lang,'Document what works, what has been tested and what is still planned.','Dokumentoin, mikä toimii, mitä on testattu ja mitä vasta suunnitellaan.')}</p></div></div><div class="skill-row"><span class="icon-box">{icon('layers')}</span><div><h3>{tr(lang,'Preserve the useful parts','Säilytä hyödyllinen')}</h3><p>{tr(lang,'Keep provenance, upstream credit and practical documentation close to the code.','Pidän alkuperän, muiden tekijöiden ansiot ja käytännön dokumentaation lähellä koodia.')}</p></div></div></div></div></section>{cta(lang)}'''
    return shell(lang,'about',tr(lang,'About me','Minusta'),tr(lang,'Meet Mikael Nurminen: mixutin / 0x11a, a Finnish security researcher and open-source builder.','Tutustu Mikael Nurmiseen: mixutin / 0x11a, suomalainen tietoturvan tutkija ja avoimen lähdekoodin tekijä.'),body)

def contact(lang):
    body=heading(lang,'contact',tr(lang,"Let's make<br><span class=\"gradient\">a connection.</span>",'Otetaan<br><span class="gradient">yhteyttä.</span>'),tr(lang,'The best place to reach me is GitHub. For project-specific questions, use the relevant repository so the conversation stays useful to everyone.','Tavoitat minut parhaiten GitHubissa. Projektikohtaiset kysymykset kannattaa jättää kyseiseen repositorioon, jotta keskustelusta on hyötyä muillekin.'),'shield')
    cards=[('github',GITHUB,'GitHub / @mixutin','Public projects, code and collaboration.','Julkiset projektit, koodi ja yhteistyö.'),('chat',GITHUB+'/dauntless-revived/discussions','Dauntless Revived / Discussions','Questions, ideas and play-test reports.','Kysymykset, ideat ja pelitestien havainnot.'),('globe',CRYPTO,'CryptoHack / nurminen','Cryptography profile and current rankings.','Kryptografiaprofiili ja ajantasaiset sijoitukset.')]
    links=''.join(f'<a class="contact-card" href="{u}"><span class="icon-box">{icon(i)}</span><div><h2>{t}</h2><p>{tr(lang,en,fi)}</p></div>{icon("arrow")}</a>' for i,u,t,en,fi in cards)
    body+=f'''<section class="wrap compact-section"><div class="split"><div class="contact-list">{links}</div><div class="feature-copy"><p class="section-label">RESPONSIBLE DISCLOSURE /</p><h2>{tr(lang,'Security issue?<br>Keep it private.','Tietoturvaongelma?<br>Kerro yksityisesti.')}</h2><p>{tr(lang,'Please do not post vulnerability details or secrets in a public issue. For Dauntless Revived, use the private advisory channel. For other projects, follow their security policy.','Älä julkaise haavoittuvuuden yksityiskohtia tai salaisuuksia julkisessa issuessa. Dauntless Revivedille on yksityinen ilmoituskanava. Muiden projektien kohdalla noudata niiden tietoturvaohjetta.')}</p>{link(GITHUB+'/dauntless-revived/security/advisories/new',tr(lang,'Private security report','Yksityinen tietoturvailmoitus'),'button')}
<p class="micro"><a href="/.well-known/security.txt">security.txt ↗</a></p></div></div></section>'''
    return shell(lang,'contact',tr(lang,'Contact','Yhteystiedot'),tr(lang,'Contact Mikael Nurminen / mixutin on GitHub. Project discussions and responsible security disclosure.','Ota yhteyttä Mikael Nurmiseen / mixutiniin GitHubissa. Projektikeskustelut ja vastuullinen tietoturvailmoittaminen.'),body)

def writing(lang,page):
    is_blog=page=='blog'
    title=tr(lang,'Notes from<br><span class="gradient">the workbench.</span>','Muistiinpanoja<br><span class="gradient">työpöydältä.</span>') if is_blog else tr(lang,'Understand it.<br><span class="gradient">Write it down.</span>','Ymmärrä ratkaisu.<br><span class="gradient">Kirjoita se auki.</span>')
    desc=tr(lang,'Project notes, CTF updates and things learned along the way.','Projektimuistiinpanoja, CTF-kuulumisia ja matkan varrella opittua.') if is_blog else tr(lang,'A home for cryptography and reverse-engineering writeups. Publication follows each competition’s rules.','Kryptografian ja takaisinmallinnuksen ratkaisukirjoitukset. Julkaisut noudattavat kunkin kilpailun sääntöjä.')
    body=heading(lang,page,title,desc)
    if is_blog:
        body+=f'''<section class="wrap section"><a class="journal-card" href="{url(lang,'blog/back-in-ctfs')}"><time datetime="2026-09-25">25.09.2026<br>CTF UPDATE</time><div><span class="status">CRYPTO / REV / THEM?!</span><h2>{tr(lang,'Back in CTFs: crypto, rev and THEM?!','Takaisin CTF-kilpailuihin: crypto, rev ja THEM?!')}</h2><p>{tr(lang,'Returning to competition, focusing on cryptography and reverse engineering, and making room for future writeups.','Paluu kilpailuihin, kryptografiaan ja takaisinmallinnukseen keskittyminen sekä tilaa tuleville ratkaisukirjoituksille.')}</p></div>{icon('arrow')}</a></section>'''
    else:
        body+=f'''<section class="wrap section"><div class="cta"><div><p class="section-label">WRITEUPS / 00</p><h2>{tr(lang,'The next chapter is still being written.','Seuraava luku on vielä työn alla.')}</h2><p>{tr(lang,'No challenge writeups have been published on this site yet. Future articles will appear here; the CTF page has my current focus and profile links.','Tällä sivustolla ei ole vielä julkaistu haasteiden ratkaisukirjoituksia. Tulevat artikkelit ilmestyvät tänne. CTF-sivulta löydät painopisteeni ja profiililinkit.')}</p></div>{link(url(lang,'ctf'),tr(lang,'CTF profile','CTF-profiili'),'button','right')}</div></section>'''
    return shell(lang,page,'Blog' if is_blog else 'CTF writeups',desc,body)

def generate():
    out={}
    for lang in ['en','fi']:
        for page,fn in [('',home),('projects',projects),('ctf',ctf),('about',about),('contact',contact),('blog',lambda l:writing(l,'blog')),('writeups',lambda l:writing(l,'writeups'))]:
            out[url(lang,page).lstrip('/')+'index.html']=fn(lang)
    notfound='<section class="wrap center-page"><p class="section-label">CONNECTION NOT FOUND</p><h1>404</h1><h2>Off the map. / Sivua ei löytynyt.</h2><p class="muted">This route does not exist. / Tätä osoitetta ei ole.</p><div class="actions">'+link('/','Back home','button primary')+link('/fi/','Suomenkielinen etusivu','button')+'</div></section>'
    out['404.html']=shell('en','','Page not found','Page not found / Sivua ei löytynyt.',notfound,True)
    paths=[url(l,p) for l in ['en','fi'] for p in ['', 'projects','ctf','about','contact','blog','writeups','projects/dauntless-revived','blog/back-in-ctfs']]
    out['sitemap.xml']='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{BASE}{p}</loc></url>\n' for p in paths)+'</urlset>\n'
    out['llms.txt']='# Mikael Nurminen / mixutin / 0x11a\n\nFinnish security researcher and open-source builder. Cryptography, reverse engineering, game preservation and systems software. CTF team: THEM?!.\n\n## Pages\n'+''.join(f'- [{p.strip("/") or "Home"}]({BASE}{p})\n' for p in paths)+'\n## Public projects\n'+''.join(f'- [{p["name"]}]({GITHUB}/{p["repo"]}): {p["description"]["en"]} {p["note"]["en"]}\n' for p in DATA['projects'])+'\nCryptoHack: #1 globally and #1 in Finland, owner-supplied September 2026 portfolio snapshot, not a live or independently verified ranking. Current profile: '+CRYPTO+'\n'
    return out

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true',help='fail if committed generated pages differ')
    args=parser.parse_args()
    changed=[]
    for path,content in generate().items():
        target=ROOT/path
        if args.check:
            if not target.exists() or target.read_text(encoding='utf-8')!=content:
                changed.append(path)
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(content, encoding='utf-8')
    if changed:
        raise SystemExit('Regenerate with python3 tools/build.py: '+', '.join(changed))
    print('Generated pages are current.' if args.check else 'Generated 15 HTML pages, sitemap.xml and llms.txt.')
