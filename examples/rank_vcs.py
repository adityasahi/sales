"""
Example: Use the VCResearchAgent to rank a list of VC firms by fit,
then auto-generate a pitch deck and outreach email for the top pick.

Run:
    python examples/rank_vcs.py
"""

import os
from deck_cli.agents.vc_research_agent import VCResearchAgent
from deck_cli.fetcher import fetch_brand_data
from deck_cli.renderer import render_template
from deck_cli.compiler import compile_deck
from deck_cli.outreach import generate_outreach

YOUR_DOMAIN = "mychiti.com"  # Replace with your company domain
VC_LIST = [
    "ycombinator.com",
    "a16z.com",
    "sequoiacap.com",
    "firstround.com",
    "betaworks.com",
]

CONTEXT_KEY = os.getenv("CONTEXT_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    print("\U0001f916 VCResearchAgent: Ranking VCs by fit...\n")
    agent = VCResearchAgent(context_api_key=CONTEXT_KEY, openai_api_key=OPENAI_KEY)
    rankings = agent.rank_vcs(YOUR_DOMAIN, VC_LIST)

    print("\n\U0001f3c6 VC Fit Rankings:")
    for i, r in enumerate(rankings, 1):
        print(f"  {i}. {r['vc_name']} — Score: {r['fit_score']}/100")
        print(f"     Reason: {r['reason']}")
        print(f"     Thesis: {r['thesis'][:120] if r['thesis'] else 'N/A'}...\n")

    # Auto-generate pitch deck + outreach for the top-ranked VC
    top = rankings[0]
    print(f"\n\U0001f4ca Auto-generating pitch deck for top pick: {top['vc_name']}")

    brand = top["_brand_data"]
    vc = top["_vc_data"]
    context = {**brand, **vc}

    os.makedirs("output", exist_ok=True)

    rendered = render_template("templates/investor_pitch.md", context)
    temp_md = f"output/{top['vc_domain']}_temp.md"
    with open(temp_md, "w") as f:
        f.write(rendered)
    deck_out = f"output/{top['vc_domain'].replace('.', '_')}_pitch.pdf"
    compile_deck(temp_md, deck_out, "pdf")
    os.remove(temp_md)
    print(f"\u2705 Pitch deck: {deck_out}")

    email = generate_outreach(brand, vc, OPENAI_KEY)
    email_out = f"output/{top['vc_domain'].replace('.', '_')}_outreach.txt"
    with open(email_out, "w") as f:
        f.write(email)
    print(f"\u2705 Outreach email: {email_out}")
