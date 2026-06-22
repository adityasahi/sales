import click
import os
from dotenv import load_dotenv
from deck_cli.fetcher import fetch_brand_data, fetch_vc_profile, scrape_page
from deck_cli.renderer import render_template
from deck_cli.compiler import compile_deck
from deck_cli.outreach import generate_outreach

load_dotenv()


@click.group()
def main():
    """auto-sales-deck-cli: Generate branded sales decks, VC pitch decks, and personalized outreach."""
    pass


@main.command()
@click.option("--domain", required=True, help="Your company domain (e.g. mychiti.com)")
@click.option("--vc-domain", required=True, help="Target VC firm domain (e.g. sequoiacap.com)")
@click.option("--output", default="pdf", type=click.Choice(["pdf", "html", "pptx"]), help="Output format")
@click.option("--out-dir", default="output", help="Directory to save outputs")
@click.option("--openai-key", default=None, help="OpenAI API key for AI copy generation")
@click.option("--api-key", default=None, help="Context.dev API key")
def pitch_vc(
    domain, vc_domain, output, out_dir, openai_key, api_key
):
    """
    Generate a VC-tailored pitch deck AND personalized cold outreach email.
    Crawls the VC's full website to learn their thesis, portfolio, and preferences.
    """
    api_key = api_key or os.getenv("CONTEXT_API_KEY")
    openai_key = openai_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise click.ClickException("Set CONTEXT_API_KEY env var or pass --api-key.")

    click.echo(f"\U0001f3e6 Fetching your company brand data ({domain})...")
    brand = fetch_brand_data(domain, api_key, ai_copy=True)

    click.echo(f"\U0001f50d Crawling VC site: {vc_domain}...")
    vc = fetch_vc_profile(vc_domain, api_key)

    context = {**brand, **{f"vc_{k}" if not k.startswith("vc_") else k: v for k, v in vc.items()}}
    # re-merge cleanly
    context.update(vc)

    os.makedirs(out_dir, exist_ok=True)

    # --- Generate pitch deck ---
    click.echo("\U0001f4ca Rendering VC pitch deck...")
    template_path = "templates/investor_pitch.md"
    rendered_md = render_template(template_path, context)
    temp_md = os.path.join(out_dir, f"{vc_domain}_pitch_temp.md")
    with open(temp_md, "w") as f:
        f.write(rendered_md)
    deck_file = os.path.join(out_dir, f"{vc_domain.replace('.', '_')}_pitch.{output}")
    compile_deck(temp_md, deck_file, output)
    os.remove(temp_md)
    click.echo(f"\u2705 Pitch deck saved: {deck_file}")

    # --- Generate outreach email ---
    click.echo("\u2709\ufe0f Generating personalized outreach email...")
    outreach_text = generate_outreach(
        brand_data=brand,
        vc_data=vc,
        openai_key=openai_key,
    )
    outreach_file = os.path.join(out_dir, f"{vc_domain.replace('.', '_')}_outreach.txt")
    with open(outreach_file, "w") as f:
        f.write(outreach_text)
    click.echo(f"\u2705 Outreach email saved: {outreach_file}")


@main.command()
@click.option("--domain", required=True, help="Target company domain (e.g. stripe.com)")
@click.option("--template", default="templates/default.md", help="Path to Marp Markdown template")
@click.option("--deck-type", default=None,
              type=click.Choice(["sales", "investor", "cold_outreach", "enterprise", "partnership", "case_study", "onboarding"]),
              help="Auto-select a built-in template by deck type")
@click.option("--output", default="pdf", type=click.Choice(["pdf", "html", "pptx"]), help="Output format")
@click.option("--out-dir", default="output", help="Directory to save the generated deck")
@click.option("--ai-copy", is_flag=True, help="Use Context.dev AI Query to write personalized slide copy")
@click.option("--api-key", default=None, help="Context.dev API key")
def generate(domain, template, deck_type, output, out_dir, ai_copy, api_key):
    """Generate a branded sales or pitch deck for a target domain."""
    api_key = api_key or os.getenv("CONTEXT_API_KEY")
    if not api_key:
        raise click.ClickException("Set CONTEXT_API_KEY env var or pass --api-key.")

    deck_type_map = {
        "sales": "templates/default.md",
        "investor": "templates/investor_pitch.md",
        "cold_outreach": "templates/cold_outreach.md",
        "enterprise": "templates/enterprise_rfp.md",
        "partnership": "templates/agency.md",
        "case_study": "templates/minimal.md",
        "onboarding": "templates/minimal.md",
    }
    if deck_type:
        template = deck_type_map[deck_type]

    click.echo(f"\U0001f50d Fetching brand data for {domain}...")
    brand_data = fetch_brand_data(domain, api_key, ai_copy=ai_copy)

    if ai_copy:
        click.echo("\U0001f916 Running AI copy generation via Context.dev...")

    click.echo(f"\U0001f3a8 Rendering template: {template}")
    rendered_md = render_template(template, brand_data)

    os.makedirs(out_dir, exist_ok=True)
    temp_md = os.path.join(out_dir, f"{domain}_temp.md")
    with open(temp_md, "w") as f:
        f.write(rendered_md)

    output_file = os.path.join(out_dir, f"{domain.replace('.', '_')}_deck.{output}")
    click.echo(f"\U0001f4ca Compiling to {output.upper()}...")
    compile_deck(temp_md, output_file, output)
    os.remove(temp_md)
    click.echo(f"\u2705 Done! Deck saved to: {output_file}")


@main.command()
@click.option("--domain", required=True, help="Target prospect domain")
@click.option("--api-key", default=None, help="Context.dev API key")
@click.option("--openai-key", default=None, help="OpenAI API key")
@click.option("--out-dir", default="output", help="Output directory")
def outreach(domain, api_key, openai_key, out_dir):
    """Generate a personalized cold outreach email for any company domain."""
    api_key = api_key or os.getenv("CONTEXT_API_KEY")
    openai_key = openai_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise click.ClickException("Set CONTEXT_API_KEY env var or pass --api-key.")

    click.echo(f"\U0001f50d Fetching brand data for {domain}...")
    brand_data = fetch_brand_data(domain, api_key, ai_copy=True)

    click.echo("\u2709\ufe0f Generating outreach email...")
    email = generate_outreach(brand_data=brand_data, vc_data=None, openai_key=openai_key)

    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"{domain.replace('.', '_')}_outreach.txt")
    with open(out_file, "w") as f:
        f.write(email)
    click.echo(f"\u2705 Outreach email saved: {out_file}")


@main.command()
def list_templates():
    """List all available built-in templates."""
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    templates = [f for f in os.listdir(templates_dir) if f.endswith(".md")]
    click.echo("Available templates:")
    for t in sorted(templates):
        click.echo(f"  - templates/{t}")
