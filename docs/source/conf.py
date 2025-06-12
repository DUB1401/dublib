import tomllib
import sys
import os



work_dir = os.path.abspath("../..")
lib_data = None
readme_copyright_years = None

sys.path.insert(0, os.path.abspath("../../src"))

with open(f"{work_dir}/pyproject.toml", "rb") as FileReader:
	lib_data = tomllib.load(FileReader)

with open(f"{work_dir}/README.md", "r", encoding = "utf-8") as FileReader: 
	readme_copyright_years = FileReader.readlines()[-1].strip().split()[-1].rstrip("_.")

project = "dublib"
copyright = f"{readme_copyright_years}, DUB1401"
author = "DUB1401"
release = lib_data["project"]["version"]

extensions = [
    "sphinx.ext.autodoc",
	"sphinx.ext.viewcode"
]

templates_path = ['_templates']
exclude_patterns = []

language = "ru"


html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
