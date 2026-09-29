# mixutin · Mikael Nurminen

A bilingual portfolio for **security, cryptography, reverse engineering and open-source software**, published at **https://mixutin.github.io/**. Finnish: **https://mixutin.github.io/fi/**.

Deep navy, electric blue and cyan. Original animated network globe and extruded security shields. Actual separate HTML pages, not a JavaScript router.

## Pages

| English | Finnish | Content |
| --- | --- | --- |
| `/` | `/fi/` | Introduction, 3D globe, CryptoHack highlights and selected projects |
| `/projects/` | `/fi/projects/` | Five public projects, search, category filters and development status |
| `/ctf/` | `/fi/ctf/` | Cryptography, reverse engineering, THEM?! and ranking snapshot |
| `/about/` | `/fi/about/` | Background, toolkit and workflow |
| `/contact/` | `/fi/contact/` | GitHub, project discussions and private disclosure |
| `/blog/` | `/fi/blog/` | Blog index |
| `/writeups/` | `/fi/writeups/` | Writeup index; no invented challenge articles |

The existing `/projects/dauntless-revived/` case study and `/blog/back-in-ctfs/` article, including their Finnish versions, are preserved. Their original stylesheet is retained as `assets/css/legacy.css`, with a navy theme layered on top. Existing project sites such as `/Vibrix/` and `/Mallow/` remain separate GitHub Pages projects.

## Preview and edit

The deployed pages are committed static files. GitHub Pages needs no build configuration change, npm install, CDN or application server. Keep `.nojekyll` and the existing security contact file.

```sh
python3 -m http.server 4100
# Open http://localhost:4100/ or http://localhost:4100/fi/
```

Content and templates are in `tools/build.py`. The curated public project catalog, source links and bilingual descriptions are in `data/projects.json`. To regenerate the committed pages:

```sh
python3 tools/build.py
python3 tools/build.py --check
python3 -m unittest discover -s tests -v
node --check assets/js/site.js
node --check assets/js/scene.js
```

Python 3.10+ is sufficient; the generator and structural tests use only the standard library. Node is only needed for the optional syntax checks. CI verifies the committed HTML matches the generator and checks links, languages, IDs, content and script syntax.

## Visuals, accessibility and performance

`assets/js/scene.js` projects original 3D coordinates onto a Canvas 2D surface. It draws a dotted globe, simplified continent silhouettes, orbiting connections and a depth-sorted extruded shield. It uses no Three.js, texture download or external code. This is decorative artwork, not real network traffic or an accurate map.

The renderer caps pixel density at 1.75 and animation at approximately 30 frames per second. It stops when its scene is outside the viewport, when the document is hidden or when motion is paused. `prefers-reduced-motion` starts with a still rendering. A keyboard-accessible motion button lets readers override the motion state; an optional tab-session preference uses `sessionStorage` defensively. A CSS illustration remains when JavaScript or Canvas is unavailable.

Navigation, content, source links and all project cards work without JavaScript. Search controls appear only when initialized. The responsive menu exposes its state to assistive technology and closes with Escape. New pages have local-only assets, a restrictive Content Security Policy, visible focus indicators, a skip link, canonical URLs and matching language links. Their code has no analytics or tracking cookies. Preserved historical pages still contain their original Google Fonts request and, on the detailed project page, the public roadmap fetch.

## Content provenance

Public project selection was checked against GitHub on **29 September 2026**: **Vibrix, Lumina, Mallow, Dauntless Revived, JKI / Jake**. Each entry links its source README. Pre-alpha and incomplete features are described as such; notably, Mallow's runtime setup is not a working Windows application launcher. Private repositories and unrelated upstream forks are not promoted as new original projects.

**CryptoHack #1 Globally / #1 In Finland** is the owner's September 2026 portfolio snapshot, not an independently verified real-time feed. The pages link to https://cryptohack.org/user/nurminen/ for the current position. Refresh the snapshot wording when updating it.

Dauntless Revived is a modified fork of **Undaunted by gwog (Gregory Morford) and contributors**, under AGPL-3.0. The original case study and upstream credit remain intact. Game names belong to their owners; these are unofficial projects, not endorsements. No game assets or private account data are added by this redesign.

## Validation of this redesign

The generated pages and JavaScript were checked locally. Chromium in-memory layout fixtures exercised all 14 bilingual routes at a mobile viewport, desktop and mobile screenshots, project category/search/reset behavior, the menu, paused and reduced-motion rendering, and the no-JavaScript project list. No horizontal overflow or JavaScript exceptions were observed in those fixtures. The environment blocked local HTTP browser navigation, so these are layout/interaction tests, not a claim of a complete deployed-browser or CSP audit.

Implementation: GPT-6 Astra Pro, at the repository owner's request.
