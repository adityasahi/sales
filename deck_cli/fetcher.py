import requests

CONTEXT_API_BASE = "https://api.context.dev"

def fetch_brand_data(domain: str, api_key: str) -> dict:
    """
    Fetch brand and company data from Context.dev for a given domain.
    Returns a normalized dict with keys safe for Jinja2 template injection.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.get(
            f"{CONTEXT_API_BASE}/v2/brand",
            params={"domain": domain},
            headers=headers,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Context.dev API error ({resp.status_code}): {resp.text}") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error fetching brand data: {e}") from e

    colors = data.get("colors", {})
    socials = data.get("socials", {})

    return {
        "company_name": data.get("name", domain.split(".")[0].capitalize()),
        "domain": domain,
        "description": data.get("description", "A great company."),
        "logo_url": data.get("logo", ""),
        "primary_color": colors.get("primary", "#1a1a2e"),
        "secondary_color": colors.get("secondary", "#16213e"),
        "text_color": colors.get("text", "#FFFFFF"),
        "industry": data.get("category", ""),
        "linkedin_url": socials.get("linkedin", ""),
        "twitter_url": socials.get("twitter", ""),
        "website_url": f"https://{domain}",
    }
