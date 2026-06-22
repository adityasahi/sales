import requests

CONTEXT_API_BASE = "https://api.context.dev"


def _get(endpoint: str, params: dict, headers: dict) -> dict:
    """Generic GET helper with error handling."""
    try:
        resp = requests.get(
            f"{CONTEXT_API_BASE}{endpoint}",
            params=params,
            headers=headers,
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError:
        return {}
    except requests.exceptions.RequestException:
        return {}


def fetch_brand_data(domain: str, api_key: str, ai_copy: bool = False) -> dict:
    """
    Full enrichment fetch from Context.dev.
    Pulls brand, socials, fonts, screenshot, address, NAICS, and optionally AI-generated copy.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Core brand + styleguide
    brand = _get("/v2/brand", {"domain": domain}, headers)
    colors = brand.get("colors", {})
    socials = brand.get("socials", {})

    # Fonts
    font_data = _get("/v1/font", {"domain": domain}, headers)
    font_name = font_data.get("font", "Helvetica Neue")

    # Address
    addr = _get("/v1/address", {"domain": domain}, headers)

    # NAICS industry classification
    naics = _get("/v1/naics", {"domain": domain}, headers)

    # Screenshot
    screenshot_data = _get("/v1/screenshot", {"url": f"https://{domain}"}, headers)
    screenshot_url = screenshot_data.get("screenshot_url", "")

    payload = {
        # Brand
        "company_name": brand.get("name", domain.split(".")[0].capitalize()),
        "domain": domain,
        "description": brand.get("description", ""),
        "logo_url": brand.get("logo", ""),
        "favicon_url": brand.get("favicon", ""),
        "backdrop_url": brand.get("backdrop", ""),
        # Colors
        "primary_color": colors.get("primary", "#1a1a2e"),
        "secondary_color": colors.get("secondary", "#16213e"),
        "text_color": colors.get("text", "#FFFFFF"),
        # Font
        "font_name": font_name,
        # Socials
        "linkedin_url": socials.get("linkedin", ""),
        "twitter_url": socials.get("twitter", ""),
        "youtube_url": socials.get("youtube", ""),
        "facebook_url": socials.get("facebook", ""),
        # Address
        "city": addr.get("city", ""),
        "state": addr.get("state", ""),
        "country": addr.get("country", ""),
        # Industry
        "industry": brand.get("category", naics.get("title", "")),
        "naics_label": naics.get("title", ""),
        "naics_code": naics.get("code", ""),
        # Screenshot
        "screenshot_url": screenshot_url,
        # Website
        "website_url": f"https://{domain}",
        # AI copy placeholders (populated below if --ai-copy)
        "top_pain_points": "",
        "top_services": "",
        "value_proposition": "",
        "why_now": "",
    }

    if ai_copy:
        payload["top_pain_points"] = _ai_query(
            domain, "List the top 3 operational pain points this company likely faces. Be concise, one sentence each.", headers
        )
        payload["top_services"] = _ai_query(
            domain, "What are the main products or services this company sells? List them briefly.", headers
        )
        payload["value_proposition"] = _ai_query(
            domain, "In one sentence, what is this company's core value proposition?", headers
        )
        payload["why_now"] = _ai_query(
            domain, "Why is now the right time for this company to adopt new AI-powered tools?", headers
        )

    return payload


def fetch_vc_profile(vc_domain: str, api_key: str) -> dict:
    """
    Deep-crawl a VC firm's website using Context.dev to extract:
    - Investment thesis
    - Portfolio companies
    - Stage and sector focus
    - Partner names and bios
    - Contact/application info
    Returns a dict for injection into pitch deck templates and outreach messages.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Brand basics
    brand = _get("/v2/brand", {"domain": vc_domain}, headers)
    colors = brand.get("colors", {})

    # Crawl the full VC website
    crawl = _get("/v1/crawl", {"domain": vc_domain, "limit": 20}, headers)
    pages = crawl.get("pages", [])
    full_site_text = "\n\n".join(
        [p.get("markdown", "") for p in pages if p.get("markdown")]
    )[:12000]  # cap to avoid token overflow

    # AI queries against the VC site
    thesis = _ai_query(vc_domain, "What is this VC firm's investment thesis? What problems or sectors do they focus on?", headers)
    stage_focus = _ai_query(vc_domain, "What funding stages does this VC invest in (pre-seed, seed, Series A, etc.)?", headers)
    sector_focus = _ai_query(vc_domain, "What sectors or industries does this VC firm primarily invest in?", headers)
    portfolio = _ai_query(vc_domain, "Name up to 10 portfolio companies this VC has invested in.", headers)
    check_size = _ai_query(vc_domain, "What is the typical check size or fund size of this VC firm?", headers)
    what_they_value = _ai_query(vc_domain, "What qualities, metrics, or founder traits does this VC firm say they look for in investments?", headers)
    partners = _ai_query(vc_domain, "Who are the key partners or team members at this VC firm?", headers)
    how_to_apply = _ai_query(vc_domain, "How does this VC firm prefer to receive pitches or applications? What is their process?", headers)

    return {
        "vc_name": brand.get("name", vc_domain.split(".")[0].capitalize()),
        "vc_domain": vc_domain,
        "vc_website": f"https://{vc_domain}",
        "vc_logo_url": brand.get("logo", ""),
        "vc_primary_color": colors.get("primary", "#0F172A"),
        "vc_text_color": colors.get("text", "#FFFFFF"),
        "vc_linkedin": brand.get("socials", {}).get("linkedin", ""),
        "vc_twitter": brand.get("socials", {}).get("twitter", ""),
        "thesis": thesis,
        "stage_focus": stage_focus,
        "sector_focus": sector_focus,
        "portfolio": portfolio,
        "check_size": check_size,
        "what_they_value": what_they_value,
        "partners": partners,
        "how_to_apply": how_to_apply,
        "full_site_text": full_site_text,
    }


def _ai_query(domain: str, question: str, headers: dict) -> str:
    """Run a natural language query against a domain via Context.dev AI Query API."""
    try:
        resp = requests.post(
            f"{CONTEXT_API_BASE}/v1/ai-query",
            json={"domain": domain, "query": question},
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("answer", "")
    except Exception:
        return ""


def scrape_page(url: str, api_key: str) -> str:
    """Scrape a single URL and return clean markdown text via Context.dev."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = _get("/v1/scrape/markdown", {"url": url}, headers)
    return data.get("markdown", "")
