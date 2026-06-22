---
marp: true
theme: default
paginate: false
style: |
  section {
    background-color: #FFFFFF;
    color: #111111;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    padding: 48px 64px;
  }
  h1 {
    font-size: 2.8em;
    font-weight: 900;
    color: {{ primary_color }};
    margin-bottom: 0.2em;
  }
  h2 {
    font-size: 1.3em;
    font-weight: 600;
    color: #444;
    margin-top: 1.6em;
    border-bottom: 2px solid {{ primary_color }};
    padding-bottom: 6px;
  }
  p, li { font-size: 1em; color: #333; line-height: 1.7; }
  strong { color: {{ primary_color }}; }
---

{% if logo_url %}![w:120]({{ logo_url }}){% endif %}

# {{ company_name }}

{{ description }}

---

## What We Do

- AI voice + SMS agents for your business
- Handles intake, qualification, booking, and follow-up
- Works 24/7 without adding headcount

---

## Why {{ company_name }}?

> *"{{ company_name }} operates in {{ industry or 'a high-touch industry' }} where response time directly drives revenue."*

We specialize in exactly this use case.

---

## One Simple Step

Book a **15-minute call**.

We'll show you exactly how it works for **{{ company_name }}** — no generic demos.

**[{{ website_url }}]({{ website_url }})**
