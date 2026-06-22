import subprocess
import shutil

def compile_deck(input_md: str, output_file: str, output_format: str = "pdf") -> None:
    """
    Call marp-cli via subprocess to compile a Markdown file into the desired output format.
    Requires: npm install -g @marp-team/marp-cli
    """
    if not shutil.which("marp"):
        raise EnvironmentError(
            "marp-cli not found. Install it with: npm install -g @marp-team/marp-cli"
        )

    format_flags = {
        "pdf": ["--pdf"],
        "html": [],
        "pptx": ["--pptx"],
    }

    flags = format_flags.get(output_format, [])

    cmd = ["marp", input_md, "-o", output_file] + flags

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(
            f"marp-cli failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )
