---
marp: true
theme: default
paginate: true
style: |
  section {
    background-color: {{ primary_color }};
    color: {{ text_color }};
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  }
  h1, h2 {
    color: {{ text_color }};
    border-bottom: 3px solid {{ secondary_color }};
    padding-bottom: 8px;
  }
  a {
    color: {{ secondary_color }};
  }
  .lead h1 {
    font-size: 2.2em;
  }
---

<!-- _class: lead -->

{% if logo_url %}![Logo w:180]({{ logo_url }}){% endif %}

# A Proposal for
# **{{ company_name }}**

*Powered by auto-sales-deck-cli*

---

## About {{ company_name }}

{{ description }}

{% if industry %}- **Industry:** {{ industry }}{% endif %}
- **Website:** [{{ website_url }}]({{ website_url }})
{% if linkedin_url %}- **LinkedIn:** [View Profile]({{ linkedin_url }}){% endif %}

---

## The Challenge

Every {{ industry or 'business' }} faces the same core problem:

- Manual, time-consuming workflows
- Disconnected tools that don't talk to each other
- Missed leads and delayed responses

---

## Our Solution for {{ company_name }}

We provide an AI-native communication layer that:

- **Answers calls and qualifies leads automatically**
- **Sends intake forms during the conversation**
- **Books calendars and updates your CRM**
- **Escalates only high-value situations to your team**

---

## Why Now?

> Clients who respond within **5 minutes** are **9x more likely** to convert.

Your team cannot be available 24/7. Your AI agent can.

---

## Next Steps

1. 30-minute discovery call with your team
2. Configure your AI agent for {{ company_name }}'s workflows
3. Go live in under 2 weeks

**Let's build the future together.**

---

<!-- _class: lead -->

{% if logo_url %}![Logo w:120]({{ logo_url }}){% endif %}

## Ready to get started?

[{{ website_url }}]({{ website_url }})
