import os
import sys
import tomllib

work_dir = os.path.abspath("..")
lib_data = None
readme_copyright_years = None

sys.path.insert(0, os.path.abspath("../src"))

with open(f"{work_dir}/pyproject.toml", "rb") as FileReader:
	lib_data = tomllib.load(FileReader)

with open(f"{work_dir}/README.md", "r", encoding = "utf-8") as FileReader: 
	readme_copyright_years = FileReader.readlines()[-1].strip().split()[-1].rstrip("_.")

project = "dublib"
copyright = f"{readme_copyright_years}, DUB1401"  # noqa: A001
author = "DUB1401"
release = lib_data["project"]["version"]

extensions = [
	"myst_parser",
	"sphinx.ext.autodoc",
	"sphinx.ext.viewcode"
]

source_suffix = {
	".rst": "restructuredtext",
	".md": "markdown"
}

templates_path = ['_templates']
exclude_patterns = [
	"README.md"
]

language = "ru"
html_theme = "sphinx_rtd_theme"
