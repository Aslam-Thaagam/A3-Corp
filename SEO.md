# SEO — A3 Corporation

Target queries: **"A3 Corporation"** / "A3 Corp" and **"Aslam Musbar"**
Canonical domain: `https://a3-corp.alwaysdata.net`
Founder site: `https://aslam.alwaysdata.net`

---

## What's in the code

All values live in one place — **`a3_app/seo.py`**. Change them there and every meta
tag, structured-data block and sitemap entry follows.

| Piece | Location |
|---|---|
| SEO constants + JSON-LD graph | `a3_app/seo.py` |
| Context processor (`{{ SEO.* }}` in every template) | `a3_app/seo.py:seo`, registered in `settings.TEMPLATES` |
| Meta tags, Open Graph, Twitter, canonical | `a3_app/templates/base.html` `<head>` |
| Per-page title / description / keywords | blocks at the top of each page template |
| `sitemap.xml` | `a3_app/sitemaps.py` → `/sitemap.xml` |
| `robots.txt` | `a3_app/views.py:robots_txt` → `/robots.txt` |
| `noindex` on private pages | `dashboard*.html` |

### Structured data (JSON-LD)

A single `@graph` on every page ties three entities together:

- **Organization / ProfessionalService** `#organization` — name `A3 Corp`, legalName
  `A3 Corporation`, alternateName list, Chennai address, services, opening hours.
- **Person** `#founder` — `Aslam Musbar`, `url` → `aslam.alwaysdata.net`,
  `worksFor` → the organization, `sameAs` → personal site + Instagram + this site.
- **WebSite** `#website`.

Plus page-level nodes: `WebPage` on the homepage, `ProfilePage` (with the founder as
`mainEntity`) on `/about/`, and `CreativeWork` on each sample page.

This is what tells Google that "A3 Corp", "A3 Corporation" and "Aslam Musbar" are one
connected entity rather than three unrelated strings.

---

## What you must do outside the code

Meta tags don't rank a site on their own — **the site has to be crawled, and the two
domains have to point at each other.** These steps matter more than anything above:

### 1. Add the reciprocal link (highest impact)
On **aslam.alwaysdata.net**, link to this site with the same relationship:

```html
<a href="https://a3-corp.alwaysdata.net" rel="me">A3 Corporation — my company</a>
```

Also add a `Person` JSON-LD block there with
`"sameAs": ["https://a3-corp.alwaysdata.net", "https://www.instagram.com/a3_corporation/"]`.
One-way links are weak; the pair is what makes the entity connection stick.

### 2. Google Search Console — https://search.google.com/search-console
1. Add property `https://a3-corp.alwaysdata.net`
2. Verify (HTML tag method → paste the tag into `base.html` `<head>`)
3. **Sitemaps** → submit `sitemap.xml`
4. **URL Inspection** → enter the homepage → *Request Indexing*. Repeat for `/about/`.
5. Do the same for `aslam.alwaysdata.net`.

### 3. Bing Webmaster Tools
https://www.bing.com/webmasters — import directly from Search Console.

### 4. Google Business Profile
https://business.google.com — a free listing for **A3 Corporation**, Chennai.
This is the single biggest lever for a local business name query, and it also
feeds the knowledge panel.

### 5. Consistent citations
Use the exact same **name, address, phone** everywhere: `A3 Corporation`,
Chennai, Tamil Nadu, `+91 82200 35475`. Instagram bio, LinkedIn, JustDial,
IndiaMART, Sulekha. Inconsistent details split the entity.

### 6. Fix the placeholder social links
`a3_app/templates/footer.html` has LinkedIn / Twitter / YouTube icons pointing at
`{% url 'index' %}`. Replace with real profile URLs, then add those URLs to
`SAME_AS` in `a3_app/seo.py`.

---

## Before going live

- [ ] `DEBUG = False` in `a3_corp/settings.py`
- [ ] Rotate `SECRET_KEY` (the current one is committed and marked insecure)
- [ ] `ALLOWED_HOSTS` — drop `'*'`, keep `a3-corp.alwaysdata.net`
- [ ] `python manage.py collectstatic`
- [ ] Confirm HTTPS works — canonical URLs all say `https://`
- [ ] Check `/robots.txt` and `/sitemap.xml` load on the live domain

## Timeline — be realistic

Indexing takes **days to a few weeks** after you request it. Ranking #1 for
"A3 Corporation" is realistic since it's your brand name with little competition.
"Aslam Musbar" is a personal name — you should surface for it, but expect both
`aslam.alwaysdata.net` and this site to appear, with the personal site usually first.
Neither happens the day you deploy.
