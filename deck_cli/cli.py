import click
import os
from dotenv import load_dotenv
from deck_cli.fetcher import fetch_brand_data
from deck_cli.renderer import render_template
from deck_cli.compiler import compile_deck

load_dotenv()

@click.group()
def main():
    """auto-sales-deck-cli: Generate branded sales decks from any company domain."""
    pass

@main.command()
@click.option("--domain", required=True, help="Target company domain (e.g. stripe.com)")
@click.option("--template", default="templates/default.md", help="Path to Marp Markdown template")
@click.option("--output", default="pdf", type=click.Choice(["pdf", "html", "pptx"]), help="Output format")
@click.option("--out-dir", default="output", help="Directory to save the generated deck")
@click.option("--api-key", default=None, help="Context.dev API key (overrides CONTEXT_API_KEY env var)")
def generate(domain, template, output, out_dir, api_key):
    """Generate a branded sales deck for a target domain."""
    api_key = api_key or os.getenv("CONTEXT_API_KEY")
    if not api_key:
        raise click.ClickException(
            "No API key found. Set CONTEXT_API_KEY env var or pass --api-key."
        )

    click.echo(f"🔍 Fetching brand data for {domain}...")
    brand_data = fetch_brand_data(domain, api_key)

    click.echo(f"🎨 Rendering template: {template}")
    rendered_md = render_template(template, brand_data)

    os.makedirs(out_dir, exist_ok=True)
    temp_md = os.path.join(out_dir, f"{domain}_temp.md")
    with open(temp_md, "w") as f:
        f.write(rendered_md)

    output_file = os.path.join(out_dir, f"{domain.replace('.', '_')}_sales_deck.{output}")
    click.echo(f"📊 Compiling deck to {output.upper()}...")
    compile_deck(temp_md, output_file, output)

    os.remove(temp_md)
    click.echo(f"✅ Done! Deck saved to: {output_file}")

@main.command()
def list_templates():
    """List all available built-in templates."""
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    templates = [f for f in os.listdir(templates_dir) if f.endswith(".md")]
    click.echo("Available templates:")
    for t in templates:
        click.echo(f"  - templates/{t}")
