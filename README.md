# auto-sales-deck-cli

> Generate personalized, branded sales decks from any company domain in seconds — powered by [Context.dev](https://context.dev) and [Marp CLI](https://marp.app).

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Open Source](https://img.shields.io/badge/open--source-yes-brightgreen.svg)

---

## The Problem

Sales teams and founders spend hours manually copying logos, hex codes, and company descriptions from a prospect's website just to build a personalized pitch deck. It's tedious, error-prone, and doesn't scale.

## The Solution

`auto-sales-deck` automates this entirely. Run one command with a prospect's domain, and the tool will:

1. **Fetch brand data** — logo, primary colors, fonts, description, industry, social links via Context.dev
2. **Inject into a Marp template** — Jinja2 renders the brand data into a fully styled Markdown slide deck
3. **Compile to PDF/HTML/PPTX** — Marp CLI renders the final presentation

---

## Requirements

- Python 3.9+
- Node.js + Marp CLI (`npm install -g @marp-team/marp-cli`)
- A [Context.dev](https://context.dev) API Key

---

## Installation

### Option 1 — pip (Recommended)

```bash
pip install auto-sales-deck
```

### Option 2 — Install from Source

```bash
git clone https://github.com/adityasahi/sales.git
cd sales
pip install -e .
```

### Option 3 — Windows Subsystem for Linux (WSL)

> Most developers on Windows use WSL (Ubuntu) for Python CLI tools. Here's how to get fully set up.

**Step 1 — Install WSL (if you haven't already)**

Open PowerShell as Administrator and run:

```powershell
wsl --install
```

This installs WSL 2 with Ubuntu by default. Restart your machine when prompted.

**Step 2 — Open your WSL terminal and update packages**

```bash
sudo apt update && sudo apt upgrade -y
```

**Step 3 — Install Python 3.9+**

```bash
sudo apt install python3 python3-pip python3-venv -y
python3 --version  # confirm 3.9+
```

**Step 4 — Install Node.js and Marp CLI**

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
npm install -g @marp-team/marp-cli
marp --version  # confirm marp is available
```

**Step 5 — Clone and install auto-sales-deck**

```bash
git clone https://github.com/adityasahi/sales.git
cd sales
pip3 install -e .
```

**Step 6 — Set your API key**

```bash
export CONTEXT_API_KEY="your_api_key_here"

# To persist across sessions, add to your shell profile:
echo 'export CONTEXT_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Step 7 — Generate your first deck**

```bash
deck-cli generate --domain stripe.com --output pdf
```

> **Tip for WSL users:** Your generated PDFs land in `./output/` inside WSL. To access them from Windows Explorer, navigate to `\\wsl$\Ubuntu\home\<your-username>\sales\output\`.

---

## Quick Start

**1. Set your Context.dev API key:**

```bash
export CONTEXT_API_KEY="your_api_key_here"
```

**2. Generate a deck:**

```bash
deck-cli generate --domain stripe.com
```

**3. Choose a template and output format:**

```bash
deck-cli generate --domain stripe.com --template templates/agency.md --output pdf
deck-cli generate --domain stripe.com --template templates/saas_pitch.md --output pptx
deck-cli generate --domain stripe.com --template templates/minimal.md --output html
```

Output: `stripe_sales_deck.pdf` saved to `./output/`

---

## CLI Reference

| Flag | Description | Default |
|---|---|---|
| `--domain` | Target company domain (required) | — |
| `--template` | Path to a Marp Markdown template | `templates/default.md` |
| `--output` | Output format: `pdf`, `html`, `pptx` | `pdf` |
| `--out-dir` | Output directory | `./output` |
| `--api-key` | Context.dev API key (overrides env var) | `CONTEXT_API_KEY` env |

---

## Templates

The repo ships with 4 ready-to-use Marp templates:

| Template | Best For |
|---|---|
| `templates/default.md` | General sales / intro deck |
| `templates/saas_pitch.md` | SaaS product pitch |
| `templates/agency.md` | Agency or service business pitch |
| `templates/minimal.md` | Clean minimal one-pager |

All templates use [Jinja2](https://jinja.palletsprojects.com/) syntax so you can customize them freely.

### Create Your Own Template

Create any `.md` file and use these variables:

```markdown
{{ company_name }}       — Company name
{{ domain }}             — Domain
{{ description }}        — Company description
{{ logo_url }}           — Logo image URL
{{ primary_color }}      — Primary brand hex color
{{ secondary_color }}    — Secondary brand hex color
{{ text_color }}         — Text contrast color
{{ industry }}           — Industry label
{{ linkedin_url }}       — LinkedIn profile URL
{{ twitter_url }}        — Twitter/X profile URL
{{ website_url }}        — Website URL
```

---

## Project Structure

```
sales/
├── deck_cli/
│   ├── __init__.py
│   ├── cli.py           # Click CLI entrypoint
│   ├── fetcher.py       # Context.dev brand data fetcher
│   ├── renderer.py      # Jinja2 template renderer
│   └── compiler.py      # Marp CLI subprocess compiler
├── templates/
│   ├── default.md
│   ├── saas_pitch.md
│   ├── agency.md
│   └── minimal.md
├── output/              # Generated decks saved here
├── tests/
│   └── test_fetcher.py
├── setup.py
├── requirements.txt
└── README.md
```

---

## Contributing

Pull requests are welcome! The easiest way to contribute is to **add a new Marp CSS template** to `/templates`.

1. Fork the repo
2. Add your template to `/templates/your_template.md`
3. Open a PR describing what type of deck it's designed for

---

## License

MIT — free to use, fork, and extend.

---

## Built With

- [Context.dev](https://context.dev) — Brand data & web enrichment API
- [Marp](https://marp.app) — Markdown presentation framework
- [Click](https://click.palletsprojects.com/) — Python CLI framework
- [Jinja2](https://jinja.palletsprojects.com/) — Template engine
