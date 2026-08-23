"""Central SEO configuration for A3 Corp.

Everything search engines need to identify the business and its founder lives
here so the values stay consistent across meta tags, structured data and the
sitemap. Update the constants below and every page follows.
"""

import json

from django.templatetags.static import static

# ── Canonical identity ────────────────────────────────────────────────
SITE_URL      = 'https://a3-corp.alwaysdata.net'
SITE_NAME     = 'A3 Corp'
LEGAL_NAME    = 'A3 Corporation'
ALT_NAMES     = ['A3 Corporation', 'A3Corp', 'A3 Corp Chennai', 'A3 Corporation Chennai']

TAGLINE       = 'Web Development, Graphic Design & Mobile Apps in Chennai'
DESCRIPTION   = (
    'A3 Corp (A3 Corporation) is a Chennai-based technology company founded by '
    'Aslam Musbar, building premium websites, mobile apps, graphic design and '
    'business software for clients across Tamil Nadu and India.'
)

# ── Founder ───────────────────────────────────────────────────────────
FOUNDER_NAME  = 'Aslam Musbar'
FOUNDER_URL   = 'https://aslam.alwaysdata.net'
FOUNDER_ROLE  = 'Founder & CEO'
FOUNDER_BIO   = (
    'Aslam Musbar is the Founder and CEO of A3 Corporation, a Chennai-based '
    'web development, graphic design and mobile app company. He is a full-stack '
    'developer and entrepreneur working with businesses across Tamil Nadu.'
)

# ── Contact / location ────────────────────────────────────────────────
EMAIL         = 'alaslam381@gmail.com'
PHONE         = '+918220035475'
PHONE_DISPLAY = '+91 82200 35475'
CITY          = 'Chennai'
REGION        = 'Tamil Nadu'
COUNTRY       = 'IN'
LATITUDE      = 13.0827
LONGITUDE     = 80.2707

INSTAGRAM     = 'https://www.instagram.com/a3_corporation/'

# Profiles that prove A3 Corp and Aslam Musbar are the same entity to search
# engines. The founder's personal site is the key link in both directions.
SAME_AS = [FOUNDER_URL, INSTAGRAM]

SERVICES = [
    'Web Development',
    'Mobile App Development',
    'Graphic Design',
    'UI/UX Design',
    'E-Commerce Development',
    'Business Software',
]

DEFAULT_KEYWORDS = [
    'A3 Corp', 'A3 Corporation', 'A3 Corp Chennai', 'Aslam Musbar',
    'web development Chennai', 'website design Tamil Nadu',
    'mobile app development Chennai', 'graphic design Chennai',
    'web development company Chennai',
]


def absolute(path: str) -> str:
    """Build an absolute URL on the canonical domain."""
    return f"{SITE_URL}{path if path.startswith('/') else '/' + path}"


def _org():
    """Organization node — the primary entity for 'A3 Corporation' searches."""
    return {
        '@type': ['Organization', 'ProfessionalService'],
        '@id': f'{SITE_URL}/#organization',
        'name': SITE_NAME,
        'legalName': LEGAL_NAME,
        'alternateName': ALT_NAMES,
        'url': SITE_URL,
        'description': DESCRIPTION,
        'email': EMAIL,
        'telephone': PHONE,
        'priceRange': '₹₹',
        'address': {
            '@type': 'PostalAddress',
            'addressLocality': CITY,
            'addressRegion': REGION,
            'addressCountry': COUNTRY,
        },
        'geo': {'@type': 'GeoCoordinates', 'latitude': LATITUDE, 'longitude': LONGITUDE},
        'areaServed': [
            {'@type': 'City', 'name': CITY},
            {'@type': 'State', 'name': REGION},
            {'@type': 'Country', 'name': 'India'},
        ],
        'founder': {'@id': f'{SITE_URL}/#founder'},
        'sameAs': SAME_AS,
        'openingHoursSpecification': [{
            '@type': 'OpeningHoursSpecification',
            'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'opens': '09:00', 'closes': '19:00',
        }],
        'hasOfferCatalog': {
            '@type': 'OfferCatalog',
            'name': 'A3 Corp Services',
            'itemListElement': [
                {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s}}
                for s in SERVICES
            ],
        },
    }


def _founder(logo_url):
    """Person node — the primary entity for 'Aslam Musbar' searches.

    `url` points at the personal site so Google treats aslam.alwaysdata.net and
    this site as one entity; `sameAs` reinforces it from the other direction.
    """
    return {
        '@type': 'Person',
        '@id': f'{SITE_URL}/#founder',
        'name': FOUNDER_NAME,
        'givenName': 'Aslam',
        'familyName': 'Musbar',
        'alternateName': ['Aslam', 'Al Aslam Musbar'],
        'url': FOUNDER_URL,
        'mainEntityOfPage': FOUNDER_URL,
        'jobTitle': FOUNDER_ROLE,
        'description': FOUNDER_BIO,
        'image': logo_url,
        'email': EMAIL,
        'telephone': PHONE,
        'worksFor': {'@id': f'{SITE_URL}/#organization'},
        'knowsAbout': SERVICES + ['Django', 'Python', 'Full-Stack Development'],
        'homeLocation': {
            '@type': 'Place',
            'address': {
                '@type': 'PostalAddress',
                'addressLocality': CITY,
                'addressRegion': REGION,
                'addressCountry': COUNTRY,
            },
        },
        'sameAs': [FOUNDER_URL, INSTAGRAM, SITE_URL],
    }


def _website():
    return {
        '@type': 'WebSite',
        '@id': f'{SITE_URL}/#website',
        'url': SITE_URL,
        'name': f'{SITE_NAME} — {LEGAL_NAME}',
        'description': DESCRIPTION,
        'inLanguage': 'en-IN',
        'publisher': {'@id': f'{SITE_URL}/#organization'},
    }


def structured_data(request=None):
    """The site-wide JSON-LD graph, rendered once in <head>."""
    try:
        logo_url = absolute(static('Assets/Img/a3_corp.jpg'))
    except Exception:          # static files not collected yet
        logo_url = f'{SITE_URL}/static/Assets/Img/a3_corp.jpg'

    org = _org()
    org['logo'] = {'@type': 'ImageObject', 'url': logo_url}
    org['image'] = logo_url

    graph = [org, _founder(logo_url), _website()]
    return json.dumps({'@context': 'https://schema.org', '@graph': graph},
                      ensure_ascii=False, separators=(',', ':'))


def seo(request):
    """Context processor — SEO values available in every template."""
    path = request.path
    return {
        'SEO': {
            'site_url':       SITE_URL,
            'site_name':      SITE_NAME,
            'legal_name':     LEGAL_NAME,
            'tagline':        TAGLINE,
            'description':    DESCRIPTION,
            'keywords':       ', '.join(DEFAULT_KEYWORDS),
            'canonical':      absolute(path),
            'founder_name':   FOUNDER_NAME,
            'founder_url':    FOUNDER_URL,
            'founder_role':   FOUNDER_ROLE,
            'email':          EMAIL,
            'phone':          PHONE_DISPLAY,
            'city':           CITY,
            'region':         REGION,
            'instagram':      INSTAGRAM,
            'json_ld':        structured_data(request),
        }
    }
