# Images

The site currently uses **real free stock photos from Unsplash**, loaded straight
from Unsplash's CDN. Nothing needs downloading and the site looks finished as-is.

Unsplash Licence: free for commercial use, no attribution required, no permission
needed. Hot-linking their CDN is what Unsplash recommends. Full licence:
<https://unsplash.com/license>

---

## Switching to your own photos

1. Save your photo into this `/images` folder using the filename from the table
   below (e.g. `hero-iv-therapy.jpg`).
2. From the project folder, run:

   ```bash
   python3 _tools/use-local-images.py
   ```

Every `<img>` whose file you've supplied is rewritten to point at
`images/<filename>`. Anything you haven't supplied keeps its Unsplash photo, so
the site never breaks halfway through a swap. Run it again each time you add
more photos.

To go back to the stock photos: `python3 _tools/use-local-images.py --revert`

Prefer to do it by hand? Each `<img>` carries `data-image-name="…"` telling you
which slot it is — just change that tag's `src` to `images/your-file.jpg`.

---

## Image slots

| Filename | Size | Currently showing | What yours should show |
|---|---|---|---|
| `hero-iv-therapy.jpg` | 1600 × 1000 | IV stand on a teal background | Homepage hero. Keep the **left half visually quiet** — the headline sits there. |
| `services-hero.jpg` | 1600 × 900 | Row of IV bags | Services banner: prepared drips, vitamins, a treatment tray. |
| `locations-hero.jpg` | 1600 × 900 | Orlando skyline over the lake | Locations banner: Orlando skyline or waterfront. |
| `about-hero.jpg` | 1600 × 900 | Two clinicians in scrubs | About banner: your team, warm and human. |
| `contact-hero.jpg` | 1600 × 900 | Bright modern living room | Contact banner: comfortable home interior. |
| `location-dr-phillips.jpg` | 1600 × 900 | Upscale home at sunset | Dr. Phillips: upscale homes, Restaurant Row, golf. |
| `location-lake-nona.jpg` | 1600 × 900 | Modern house with pool | Lake Nona: modern architecture, trails, waterfront. |
| `location-winter-park.jpg` | 1600 × 900 | Tree-lined street with cafés | Winter Park: brick streets, Park Avenue, oak canopy. |
| `location-windermere.jpg` | 1600 × 900 | Waterfront house with dock | Windermere: lakefront estates, docks, sunset. |
| `location-celebration.jpg` | 1600 × 900 | Palm-lined town square | Celebration: town centre, palms, resort feel. |
| `why-choose-iv-care.jpg` | 1200 × 900 | Water splash | Hydration or your mobile kit ready to go. |
| `about-team.jpg` | 1200 × 900 | Two clinicians in scrubs | Your actual team. |
| `about-nurse.jpg` | 1200 × 900 | Nurse with a patient | A nurse portrait, natural light. |
| `iv-drip-detail.jpg` | 1200 × 900 | Close-up of a drip line | Detail shot of a drip or IV bag. |
| `mobile-service.jpg` | 1200 × 900 | Clinician with a patient on a sofa | Nurse treating someone at home. |
| `standards.jpg` | 1200 × 900 | Sterile syringes | Single-use supplies laid out neatly. |
| `testimonial-1.jpg` | 240 × 240 | Smiling woman | Square headshot, face centred. |
| `testimonial-2.jpg` | 240 × 240 | Smiling man | Square headshot. |
| `testimonial-3.jpg` | 240 × 240 | Smiling woman | Square headshot. |
| `favicon.svg` | — | Brand droplet | Browser tab icon — edit the SVG to change colours. |

Export JPEGs at quality 80–85. If you'd rather use `.webp`, save it as
`hero-iv-therapy.webp` and update that one `src` by hand.

---

## Where to find more free stock photos

Commercial use allowed on all of these — check the individual photo's licence
before publishing:

- **Unsplash** — <https://unsplash.com/s/photos/iv-drip> · <https://unsplash.com/s/photos/nurse> · <https://unsplash.com/s/photos/orlando-florida>
- **Pexels** — <https://www.pexels.com/search/iv%20drip/> · <https://www.pexels.com/search/wellness/>
- **Pixabay** — <https://pixabay.com/images/search/hydration/>
- **Burst by Shopify** — <https://www.burst.shopify.com/health>

Search terms that suit this brand: *iv drip*, *iv therapy*, *infusion*,
*nurse home visit*, *wellness clinic*, *hydration*, *orlando florida*,
*lakefront home*.

## A note on photos of people

The current testimonial headshots are stock photos paired with placeholder
reviews. Before you publish, replace both with real clients (with written
permission) — pairing a stock face with an invented review is a real legal risk
in healthcare marketing. Also check that any stock model release covers
**commercial healthcare** use; some exclude it.
