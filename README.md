# mixutin.github.io

Source of <https://mixutin.github.io/>, the personal site of [mixutin](https://github.com/mixutin): cybersecurity, CTFs, reverse engineering and game preservation.

Every page exists in English and in Finnish (under `/fi/`).

Plain static HTML, CSS and a little vanilla JavaScript. There is no build step, and no cookies or analytics. The only outside requests are the Google Fonts stylesheet and, on the project pages, one public file from GitHub for the roadmap bars.

## Layout

| Path | What it is |
|---|---|
| `index.html`, `fi/index.html` | Home: about, CTFs, skills, projects, workstation, AI security, contact |
| `blog/back-in-ctfs/`, `fi/blog/back-in-ctfs/` | CTF return announcement |
| `writeups/`, `fi/writeups/` | Index for future CTF challenge writeups |
| `projects/dauntless-revived/`, `fi/projects/dauntless-revived/` | Landing page for [Dauntless Revived](https://github.com/mixutin/dauntless-revived) |
| `404.html` | Bilingual "page not found" page (GitHub Pages serves it for any missing path) |
| `assets/css/site.css` | All styles. Dark by default, light when the reader's system asks for it |
| `assets/js/roadmap.js` | Counts the done and open items in the project's `ROADMAP.md` for the roadmap bars. The page works without it |
| `assets/img/` | Transparent team and AI platform artwork used on the home pages |
| `assets/og/*.svg` | Sources of the 1200×630 social preview images (`*.png`) and the touch icon |
| `robots.txt`, `sitemap.xml`, `llms.txt`, `.well-known/security.txt` | Crawler, sitemap, plain-text summary and security contact files |
| `.nojekyll` | Tells GitHub Pages to publish the files as they are, so `/.well-known/` is served |

## Preview locally

Serve the folder from its root, because every link is root-relative:

```sh
python3 -m http.server 4100
```

Then open <http://127.0.0.1:4100/>.

## Rebuild the preview images

After editing an SVG in `assets/og/`, render it again at 1200×630:

```sh
cd assets/og
for f in og-home og-home-fi og-dauntless-revived og-dauntless-revived-fi; do
  rsvg-convert -w 1200 -h 630 -o "$f.png" "$f.svg"
done
rsvg-convert -w 180 -h 180 -o ../../apple-touch-icon.png touch-icon.svg
```

The SVGs use the Inter and JetBrains Mono fonts, so have both installed when rendering.

## Notes

- Dauntless Revived is a fork of [Undaunted](https://github.com/SyST3MDeV/Undaunted) by gwog (Gregory Morford) and contributors, licensed AGPL-3.0.
- Dauntless is a trademark of its owners. This site is not affiliated with Phoenix Labs or Epic Games, and it uses no game art: the images and diagrams are original.
- Security reports: <https://github.com/mixutin/dauntless-revived/security/advisories/new>.
