---
marp: true
theme: default
paginate: true
style: |
  section {
    background-color: {{ primary_color }};
    color: {{ text_color }};
    font-family: '{{ font_name }}', 'Inter', 'Helvetica Neue', sans-serif;
  }
  h1 { font-size: 2.2em; font-weight: 900; border-bottom: 3px solid {{ secondary_color }}; padding-bottom: 8px; }
  h2 { font-size: 1.5em; font-weight: 700; color: {{ text_color }}; }
  strong { color: {{ text_color }}; }
  table { width: 100%; border-collapse: collapse; }
  td, th { padding: 8px 12px; border: 1px solid {{ secondary_color }}; font-size: 0.85em; }
---

<!-- _class: lead -->

{% if logo_url %}![w:160]({{ logo_url }}){% endif %}

# {{ company_name }}

### {{ value_proposition or description }}

`{{ website_url }}` {% if linkedin_url %}| [LinkedIn]({{ linkedin_url }}){% endif %}

---

## The Problem

{% if top_pain_points %}
{{ top_pain_points }}
{% else %}
- **Businesses miss 62% of inbound calls** during business hours
- Manual intake workflows lose qualified leads before contact
- No affordable 24/7 communication layer exists for SMBs
{% endif %}

---

## The Solution

**{{ company_name }}** is {{ description or 'an AI-native communication platform' }}.

{% if top_services %}
**What we offer:**
{{ top_services }}
{% else %}
- AI voice agents that answer, qualify, and route calls
- SMS automation for intake, reminders, and follow-up
- Full CRM sync and calendar booking — zero human intervention
{% endif %}

---

## Market Opportunity

| Market | Size |
|---|---|
| TAM (Global SMB Comm. Software) | $47B+ |
| SAM (US Professional Services) | $8.2B |
| SOM (AI-first vertical comm.) | $620M |

> 33M small businesses in the US. Less than 5% use AI for intake.

---

## Traction

- ✅ Pilot clients live and paying
- ✅ Sub-45 second average AI response time
- ✅ 80%+ first-call resolution rate
- ✅ Integrations: Google Calendar, Stripe, Clio, Outlook

---

## Business Model

| Tier | Price | Margin |
|---|---|---|
| Starter | $99/mo | ~78% |
| Pro | $199/mo | ~80% |
| Growth | $399/mo | ~83% |

> Net Revenue Retention target: 115%+

---

## Why {{ vc_name or 'You' }}?

{% if thesis %}
Your thesis on **{{ sector_focus or 'AI infrastructure' }}** is exactly where {{ company_name }} operates.

> *{{ thesis[:280] }}*
{% else %}
We're building the infrastructure layer that every professional service business will need in the next 5 years.
{% endif %}

{% if portfolio %}
**Relevant portfolio:** {{ portfolio[:200] }}
{% endif %}

---

## The Ask

- **Raising:** [Round Size]
- **Use of funds:** Product, GTM, hiring
- **Lead investor:** [Lead Name or TBD]

**One ask:** 15 minutes to show you a live demo.

---

<!-- _class: lead -->

{% if logo_url %}![w:100]({{ logo_url }}){% endif %}

## Let's build the future of SMB communication.

**[{{ website_url }}]({{ website_url }})**
{% if vc_linkedin %}[{{ vc_name }} on LinkedIn]({{ vc_linkedin }}){% endif %}
