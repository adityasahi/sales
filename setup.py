from setuptools import setup, find_packages

setup(
    name="auto-sales-deck",
    version="0.1.0",
    author="Aditya Sahi",
    description="Generate personalized, branded sales decks from any domain using Context.dev + Marp",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/adityasahi/sales",
    packages=find_packages(),
    package_data={"deck_cli": ["../templates/*.md"]},
    include_package_data=True,
    install_requires=[
        "click>=8.1.0",
        "jinja2>=3.1.0",
        "requests>=2.31.0",
        "brand-dev>=0.1.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "deck-cli=deck_cli.cli:main",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
