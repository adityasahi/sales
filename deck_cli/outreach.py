import os


def generate_outreach(brand_data: dict, vc_data: dict | None, openai_key: str | None) -> str:
    """
    Generate a personalized outreach email.
    - If vc_data is provided: generates a VC-tailored fundraising pitch email.
    - If vc_data is None: generates a B2B cold outreach email.
    Uses OpenAI GPT-4o if an API key is available, otherwise falls back to a template.
    """
    if openai_key:
        return _gpt_outreach(brand_data, vc_data, openai_key)
    return _template_outreach(brand_data, vc_data)


def _gpt_outreach(brand_data: dict, vc_data: dict | None, openai_key: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)

        if vc_data:
            system = (
                "You are an expert startup fundraising advisor. "
                "Write a concise, compelling cold email from a founder to a VC partner. "
                "The email must reference the VC's specific thesis, portfolio, and what they value. "
                "Do NOT use generic language. Sound like a real founder who did their homework."
            )
            user = f"""
## Your Company
- Name: {brand_data.get('company_name')}
- Domain: {brand_data.get('domain')}
- Description: {brand_data.get('description')}
- Industry: {brand_data.get('industry')}
- Value Proposition: {brand_data.get('value_proposition')}
- Top Services: {brand_data.get('top_services')}

## Target VC
- Firm: {vc_data.get('vc_name')}
- Website: {vc_data.get('vc_website')}
- Thesis: {vc_data.get('thesis')}
- Stage Focus: {vc_data.get('stage_focus')}
- Sector Focus: {vc_data.get('sector_focus')}
- What They Value: {vc_data.get('what_they_value')}
- Portfolio Examples: {vc_data.get('portfolio')}
- Partners: {vc_data.get('partners')}
- How to Apply: {vc_data.get('how_to_apply')}

Write a cold email from the founder of {brand_data.get('company_name')} to a partner at {vc_data.get('vc_name')}.
Keep it under 200 words. Reference their thesis and portfolio specifically.
End with a single clear CTA (e.g. 15-min call).
"""
        else:
            system = (
                "You are an expert B2B sales copywriter. "
                "Write a short, personalized cold outreach email. "
                "Reference the prospect's actual company, industry, and likely pain points. "
                "Be direct, human, and end with one clear CTA."
            )
            user = f"""
## Prospect Company
- Name: {brand_data.get('company_name')}
- Domain: {brand_data.get('domain')}
- Description: {brand_data.get('description')}
- Industry: {brand_data.get('industry')}
- Top Pain Points: {brand_data.get('top_pain_points')}
- Value Proposition (theirs): {brand_data.get('value_proposition')}

Write a cold B2B outreach email offering AI-powered communication automation to this company.
Keep it under 150 words. Be specific to their industry and pain points.
End with a single CTA (e.g. 15-min call or demo link).
"""

        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=400,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"[OpenAI error: {e}]\n\n" + _template_outreach(brand_data, vc_data)


def _template_outreach(brand_data: dict, vc_data: dict | None) -> str:
    """Fallback template-based outreach if no OpenAI key is available."""
    company = brand_data.get("company_name", "your company")
    industry = brand_data.get("industry", "your industry")
    pain = brand_data.get("top_pain_points", "operational bottlenecks and missed leads")
    services = brand_data.get("top_services", "your core services")
    website = brand_data.get("website_url", "")

    if vc_data:
        vc_name = vc_data.get("vc_name", "your firm")
        thesis = vc_data.get("thesis", "")
        portfolio = vc_data.get("portfolio", "")
        stage = vc_data.get("stage_focus", "early-stage")
        return f"""Subject: {company} — {industry} AI Infrastructure ({stage})

Hi [Partner Name],

I came across {vc_name}'s focus on {thesis[:120] if thesis else industry} and wanted to reach out.

{company} is building AI-native communication infrastructure for {industry} businesses — replacing manual intake, scheduling, and follow-up with autonomous voice and SMS agents.

We noticed {vc_name} has backed companies like {portfolio[:100] if portfolio else 'leading operators in this space'}, and we think our infrastructure play fits squarely in your thesis.

We're raising [round size] and would love a 15-minute call to show you what we've built.

Would [date/time] work?

Best,
[Your Name]
{website}
"""
    else:
        return f"""Subject: Quick question about {company}'s client intake

Hi [Name],

I noticed {company} offers {services[:120] if services else 'a range of services'} — impressive work.

A common challenge for {industry} businesses is {pain[:150] if pain else 'managing high inbound volume without adding headcount'}.

We've built an AI-native communication layer that answers calls, qualifies leads, books calendars, and updates your CRM automatically — 24/7, without a new hire.

Would a 15-minute call make sense to explore if it fits {company}?

Best,
[Your Name]
"""
