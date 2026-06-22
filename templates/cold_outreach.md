---
marp: true
theme: default
paginate: false
style: |
  section {
    background-color: #FFFFFF;
    color: #111111;
    font-family: '{{ font_name }}', 'Helvetica Neue', Arial, sans-serif;
    padding: 40px 60px;
  }
  h1 { color: {{ primary_color }}; font-size: 2.6em; font-weight: 900; margin-bottom: 0.1em; }
  h2 { color: {{ primary_color }}; font-size: 1.3em; border-left: 5px solid {{ primary_color }}; padding-left: 14px; margin-top: 1.4em; }
  strong { color: {{ primary_color }}; }
  em { color: #555; }
  li { margin-bottom: 6px; }
---

{% if logo_url %}![w:100]({{ logo_url }}){% endif %}

# {{ company_name }},
# Here's the problem.

*A 5-slide brief from the team at [Your Company]*

---

## What We Know About {{ company_name }}

{{ description }}

{% if industry %}- **Industry:** {{ industry }}{% endif %}
- **Website:** [{{ website_url }}]({{ website_url }})
{% if city %}- **Location:** {{ city }}{% if state %}, {{ state }}{% endif %}{% endif %}

---

## The Problem You're Facing

{% if top_pain_points %}
{{ top_pain_points }}
{% else %}
- Every inbound call or inquiry that goes unanswered is a lost client
- Your team spends hours on intake tasks that should be automated
- Competitors using AI are responding 10x faster than manual teams
{% endif %}

---

## What We Do

**One AI layer. Handles everything.**

- \U0001f4de Answers inbound calls automatically
- \U0001f4ac Qualifies and follows up via SMS
- \U0001f4c5 Books your calendar without a human in the loop
- \U0001f4cb Updates your CRM with every interaction

> *Works 24/7. Costs less than one hour of staff time per month.*

---

<!-- _class: lead -->

## One action.

**Book a 15-minute call.**

We'll show you exactly how it works for **{{ company_name }}**.

*No generic demos. Built for {{ industry or 'your industry' }}.*

**[{{ website_url }}]({{ website_url }})**
