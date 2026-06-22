"""VC Research Agent

An autonomous agent that:
1. Accepts a list of VC firm domains
2. Crawls each firm's website via Context.dev
3. Scores each firm's fit against your company profile
4. Returns a ranked list with thesis summary, fit score, and outreach priority

Usage:
    from deck_cli.agents.vc_research_agent import VCResearchAgent

    agent = VCResearchAgent(context_api_key="...", openai_api_key="...")
    results = agent.rank_vcs(
        your_domain="mychiti.com",
        vc_domains=["sequoiacap.com", "a16z.com", "ycombinator.com"],
    )
    for r in results:
        print(r["vc_name"], r["fit_score"], r["reason"])
"""

import os
from deck_cli.fetcher import fetch_brand_data, fetch_vc_profile

class VCResearchAgent:
    def __init__(self, context_api_key: str, openai_api_key: str | None = None):
        self.context_key = context_api_key
        self.openai_key = openai_api_key

    def rank_vcs(self, your_domain: str, vc_domains: list[str]) -> list[dict]:
        """
        Crawl each VC site and score fit against your company.
        Returns a list of dicts sorted by fit_score descending.
        """
        your_brand = fetch_brand_data(your_domain, self.context_key, ai_copy=True)
        results = []

        for vc_domain in vc_domains:
            print(f"  Researching {vc_domain}...")
            vc = fetch_vc_profile(vc_domain, self.context_key)
            score, reason = self._score_fit(your_brand, vc)
            results.append({
                "vc_name": vc["vc_name"],
                "vc_domain": vc_domain,
                "vc_website": vc["vc_website"],
                "thesis": vc["thesis"],
                "stage_focus": vc["stage_focus"],
                "sector_focus": vc["sector_focus"],
                "what_they_value": vc["what_they_value"],
                "portfolio": vc["portfolio"],
                "fit_score": score,
                "reason": reason,
                "_vc_data": vc,
                "_brand_data": your_brand,
            })

        return sorted(results, key=lambda x: x["fit_score"], reverse=True)

    def _score_fit(self, brand: dict, vc: dict) -> tuple[int, str]:
        """
        Score (0-100) how well this VC fits your company.
        Uses OpenAI if available, otherwise keyword heuristic scoring.
        """
        if self.openai_key:
            return self._gpt_score(brand, vc)
        return self._heuristic_score(brand, vc)

    def _gpt_score(self, brand: dict, vc: dict) -> tuple[int, str]:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            prompt = f"""
You are a startup advisor evaluating VC-founder fit.

Founder Company:
- Name: {brand['company_name']}
- Industry: {brand['industry']}
- Description: {brand['description']}
- Value Proposition: {brand['value_proposition']}

VC Firm:
- Name: {vc['vc_name']}
- Thesis: {vc['thesis']}
- Stage Focus: {vc['stage_focus']}
- Sector Focus: {vc['sector_focus']}
- What They Value: {vc['what_they_value']}

Rate the fit score from 0-100 and give a 1-sentence reason.
Respond in this exact format:
SCORE: <number>
REASON: <one sentence>
"""
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80,
                temperature=0.3,
            )
            text = resp.choices[0].message.content.strip()
            lines = text.split("\n")
            score = int([l for l in lines if l.startswith("SCORE:")][0].split(":")[1].strip())
            reason = [l for l in lines if l.startswith("REASON:")][0].split(":", 1)[1].strip()
            return score, reason
        except Exception as e:
            return self._heuristic_score(brand, vc)

    def _heuristic_score(self, brand: dict, vc: dict) -> tuple[int, str]:
        score = 40  # base
        industry = brand.get("industry", "").lower()
        sector = (vc.get("sector_focus") or "").lower()
        thesis = (vc.get("thesis") or "").lower()
        keywords = ["ai", "saas", "automation", "b2b", "sms", "voice", "communication", "fintech", "legal", "vertical"]
        matches = sum(1 for kw in keywords if kw in sector or kw in thesis)
        score += matches * 8
        score = min(score, 95)
        reason = f"Keyword overlap on: {', '.join([kw for kw in keywords if kw in sector or kw in thesis][:3]) or 'general fit'}"
        return score, reason
