from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

def render_template(template_path: str, brand_data: dict) -> str:
    """
    Render a Marp Markdown template with Jinja2 using the provided brand_data dict.
    template_path can be relative (from cwd) or absolute.
    """
    template_path = os.path.abspath(template_path)
    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape([]),  # no HTML escaping for Markdown
        variable_start_string="{{",
        variable_end_string="}}",
    )

    template = env.get_template(template_file)
    return template.render(**brand_data)
