---
marp: true
theme: uncover
paginate: true
style: |
  section {
    background: linear-gradient(135deg, {{ primary_color }} 0%, {{ secondary_color }} 100%);
    color: {{ text_color }};
    font-family: 'Inter', 'Segoe UI', sans-serif;
  }
  h1 { font-size: 2.4em; font-weight: 800; }
  h2 { font-size: 1.6em; font-weight: 600; border-left: 5px solid {{ text_color }}; padding-left: 16px; }
  strong { color: {{ text_color }}; }
  code {
    background: rgba(255,255,255,0.15);
    border-radius: 4px;
    padding: 2px 6px;
  }
---

<!-- _class: lead -->

{% if logo_url %}![w:160]({{ logo_url }}){% endif %}

# Scaling {{ company_name }}
with AI-Native Infrastructure

`{{ domain }}`

---

## Company Snapshot

| Field | Info |
|---|---|
| **Company** | {{ company_name }} |
| **Industry** | {{ industry or '—' }} |
| **Website** | {{ website_url }} |

---

## The Gap We're Closing

{{ company_name }} operates in a fast-moving market.

Your current stack likely handles **volume** but not **intelligence**.

We close the intelligence gap at the communication layer.

---

## Product

- 📞 **AI Voice Agent** — Answers, qualifies, books
- 💬 **SMS Automation** — Follow-ups, reminders, intake
- 📋 **CRM Sync** — Every interaction logged automatically
- 🔔 **Smart Escalation** — Humans only for what matters

---

## Pricing

| Tier | Price | Included |
|---|---|---|
| Starter | $99/mo | 200 min + 500 SMS |
| Pro | $199/mo | 500 min + 2,000 SMS |
| Growth | $399/mo | Unlimited + Priority |

---

<!-- _class: lead -->

# Let's talk.

[{{ website_url }}]({{ website_url }})
{% if linkedin_url %}[LinkedIn]({{ linkedin_url }}){% endif %}
