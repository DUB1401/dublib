import os
import sys
import tomllib
from typing import Any

work_dir: str = os.path.abspath("..")
lib_data: dict[str, Any] | None = None
readme_copyright_years: str | None = None

sys.path.insert(0, os.path.abspath("../src"))

with open(f"{work_dir}/pyproject.toml", "rb") as reader:
	lib_data = tomllib.load(reader)

with open(f"{work_dir}/README.md", encoding = "utf-8") as reader: 
	readme_copyright_years = reader.readlines()[-1].strip().split()[-1].rstrip("_.")

project = "dublib"
copyright = f"{readme_copyright_years}, DUB1401"  # noqa: A001
author = "DUB1401"
release = lib_data["project"]["version"]

extensions = [
	"myst_parser",
	"sphinx.ext.autodoc",
	"sphinx.ext.viewcode",
]

source_suffix = {
	".rst": "restructuredtext",
	".md": "markdown",
}

templates_path = ['_templates']
exclude_patterns = [
	"README.md",
]

html_theme = "sphinx_rtd_theme"
