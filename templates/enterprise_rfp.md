---
marp: true
theme: gaia
paginate: true
style: |
  section {
    background-color: #0F172A;
    color: #E2E8F0;
    font-family: '{{ font_name }}', 'Inter', sans-serif;
    border-top: 5px solid {{ primary_color }};
  }
  h1, h2 { color: {{ primary_color }}; }
  strong { color: {{ primary_color }}; }
  table { width: 100%; }
  td, th { padding: 8px; border: 1px solid #334155; font-size: 0.82em; }
  th { background-color: {{ primary_color }}; color: #fff; }
---

<!-- _class: lead -->

{% if logo_url %}![w:140]({{ logo_url }}){% endif %}

# Enterprise Proposal
## for **{{ company_name }}**

*Prepared by [Your Company] — Confidential*

---

## Executive Summary

**{{ company_name }}** operates in **{{ industry or 'enterprise services' }}** and faces communication and intake challenges at scale.

This proposal outlines how our AI-native platform integrates with your existing stack to:
- Reduce operational overhead by 40%+
- Eliminate missed inbound contacts
- Provide full audit trail for compliance

---

## Solution Architecture

| Layer | Technology |
|---|---|
| Voice AI | Vapi + ElevenLabs Flash v2.5 |
| SMS Routing | Twilio |
| Orchestration | FastAPI + custom agent runner |
| CRM Sync | Bidirectional via REST API |
| Uptime SLA | 99.9% guaranteed |

---

## Security & Compliance

- \U0001f512 SOC 2 Type II (in progress)
- \U0001f512 Data encrypted at rest (AES-256) and in transit (TLS 1.3)
- \U0001f512 HIPAA-ready configuration available
- \U0001f512 No call recordings stored without explicit consent
- \U0001f512 Full audit log for every AI interaction

---

## Pricing & SLA

| Tier | Monthly | Included | SLA |
|---|---|---|---|
| Business | $499 | 1,000 min + 5,000 SMS | 99.5% |
| Enterprise | $999 | Unlimited | 99.9% + dedicated CSM |
| Custom | Contact | White-label + API access | Custom |

---

## Implementation Timeline

| Phase | Duration | Deliverable |
|---|---|---|
| Discovery | Week 1 | Workflow audit & config spec |
| Integration | Week 2–3 | CRM, calendar, phone number setup |
| Testing | Week 4 | QA, edge case coverage |
| Go-Live | Week 5 | Full production launch |

---

## Next Steps

1. Sign NDA and pilot agreement
2. Schedule technical discovery call
3. Define success metrics (response rate, booking rate)
4. Begin 30-day paid pilot

**[{{ website_url }}]({{ website_url }})**
