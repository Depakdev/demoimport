# Orlando IV Care — website

A premium, fully responsive marketing site for a mobile IV therapy business.
**Pure HTML, CSS and vanilla JavaScript.** No React, no Bootstrap, no Tailwind,
no build step required, no dependencies to install.

---

## Quick start

Double-click `index.html` to open it in your browser. Everything works.

For a closer match to how it behaves on a real server (clean URLs, correct
canonical paths), run a local server from this folder:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

---

## Folder structure

```
orlando-iv-care/
├── index.html              Home
├── services.html           Services — all 17 therapies, filterable cards
├── locations.html          Locations hub
├── about.html              About Us
├── contact.html            Contact + booking form
├── locations/
│   ├── dr-phillips.html    → /locations/dr-phillips
│   ├── lake-nona.html      → /locations/lake-nona
│   ├── winter-park.html    → /locations/winter-park
│   ├── windermere.html     → /locations/windermere
│   └── celebration.html    → /locations/celebration
├── css/style.css           One stylesheet, fully tokenised
├── js/main.js              One script, commented by feature
├── images/                 All imagery + SOURCES.md (how to replace)
├── sitemap.xml
├── robots.txt
└── _tools/                 Optional generators (see below)
```

---

## The five things you'll most likely want to change

### 1. Phone number, email, hours

They appear in the header, footer, contact page, mobile bar and every CTA.
Fastest way to change them everywhere:

**Find and replace across all `.html` files:**

| Find | Replace with |
|---|---|
| `(407) 000-0000` | your display phone number |
| `+14070000000` | your dialable number (`tel:` links) |
| `hello@orlandoivcare.com` | your email |

Each page also carries an `EDIT ME` comment right after `<body>` pointing at
these values.

### 2. Colours, fonts, spacing

Open `css/style.css` and edit **section 01 (Design tokens)** only — the first
~90 lines. Every colour, font, radius, shadow and spacing step on the site
derives from those variables. Change `--teal-700` and the whole site rebrands.

```css
--teal-700: #0A7C75;   /* primary button colour */
--ink-800:  #0E1416;   /* body text + dark surfaces */
--font-heading: 'Outfit', …;
--font-body:    'Inter', …;
```

### 3. Images

The site ships with **real free stock photos from Unsplash**, loaded from their
CDN (Unsplash Licence — commercial use, no attribution required).

To use your own: save it in `/images` with the filename from the table in
`images/SOURCES.md`, then run

```bash
python3 _tools/use-local-images.py
```

Photos you haven't supplied keep their Unsplash image, so nothing breaks
mid-swap. `--revert` puts the stock photos back.

### 4. Connecting the booking form

The form validates fully in the browser but doesn't send anywhere yet — it's a
static site, so there's no server to send to.

Open `js/main.js` and find:

```js
/* >>> EDIT ME: hook your booking backend up here <<< */
function submitBooking(data) { … }
```

Replace the body with a `fetch()` to Formspree, Netlify Forms, Basin, or your own
endpoint. A commented Formspree example is already there. Everything else —
validation, error messages, loading spinner, success confirmation — keeps working.

### 5. Services and locations content

Each page is plain readable HTML. Find the section you want, edit the text.
Service cards live in `services.html` inside `<div class="svc-grid">`; each card
carries a `data-category` attribute that drives the filter chips.

---

## What's built in

**Design**

- Premium black / charcoal + teal-cyan + white palette
- Outfit (headings) / Inter (body), loaded from Google Fonts with `display=swap`
- One shadow scale, one radius scale, 4/8px spacing rhythm throughout
- Subtle scroll-reveal animations, hover states and micro-interactions

**Responsive**

- Mobile-first, tested at 375 / 768 / 1024 / 1440px and in landscape
- Slide-in mobile drawer: sticky header with a close button, collapsible
  Locations submenu, phone/email/hours at the foot, focus trapping, Escape to
  close, closes on tap-outside and on any link tap
- Sticky call/book bar on phones, safe-area aware (notch + gesture bar)
- No horizontal scroll at any width

**Accessibility**

- Skip link, visible focus rings, sequential heading order
- 44px+ touch targets and 4.5:1 text contrast in both light and dark sections
- `aria-expanded` / `aria-controls` on nav, accordion and filters
- Form labels, inline errors near the field, `role="alert"` error summary
- Full `prefers-reduced-motion` support

**SEO**

- Unique title + meta description + canonical per page
- Open Graph and Twitter card tags
- JSON-LD: `MedicalBusiness` on the homepage, `FAQPage` on services, about and
  all five location pages
- Semantic landmarks, descriptive alt text, breadcrumbs
- `sitemap.xml` and `robots.txt` included

**Performance**

- Zero JS dependencies; one CSS file, one JS file (deferred)
- Photos served from Unsplash's CDN with `auto=format` (WebP/AVIF where supported)
- `width`/`height` on every image (no layout shift), lazy loading below the fold
- Hero image marked `fetchpriority="high"`
- Animations limited to `transform` and `opacity`

---

## Before you go live

1. Replace `https://www.orlandoivcare.com` in the canonical / OG / sitemap URLs
   with your real domain (find and replace across `.html` and `sitemap.xml`).
2. Swap the stock photos for your own — see `images/SOURCES.md`. Photos of your
   real nurses and premises will always outperform stock.
3. Update the phone number, email and hours.
4. Connect the booking form to a real backend.
5. Have a licensed clinician review the medical copy and the disclaimer in the
   footer. The testimonials and statistics are **illustrative placeholders** —
   replace them with real ones before publishing, since fabricated reviews and
   health claims carry legal risk.
6. Add your analytics snippet before `</body>` if you want tracking.

### Clean URLs

Files are named so that hosts which strip `.html` (Netlify, Vercel, Cloudflare
Pages, GitHub Pages with a rewrite) serve them at:

```
/services          /locations         /about        /contact
/locations/dr-phillips  /locations/lake-nona  …
```

Canonical tags already point at those clean URLs. On plain Apache/Nginx, add a
rewrite rule or keep the `.html` extension — both work.

---

## `_tools/` (optional)

Three Python scripts that are **not needed to run or edit the site**:

- `build.py` — regenerates every HTML page from shared header/footer templates.
  Useful if you want to change the nav on all 10 pages at once.
  **It overwrites the `.html` files**, so don't run it after hand-editing them
  unless you've made your changes in the script too.
- `use-local-images.py` — switches every `<img>` from the Unsplash CDN to your
  own files in `/images` (and back again with `--revert`).
- `verify.py` — runs the build checks: broken links, missing images, duplicate
  IDs, heading order, SEO tags, and the rule that location pages contain no
  address, map or directions.

Delete the `_tools/` folder if you'd rather not have it. The site doesn't use it.

---

## Browser support

Chrome, Edge, Firefox and Safari — current and one previous major version,
desktop and mobile. Uses `IntersectionObserver`, CSS custom properties,
`aspect-ratio` and CSS grid, all of which have been broadly supported since 2021.
