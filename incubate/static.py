"""
Gathered data that will not change during runtime.
"""
import datetime
import subprocess
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

template_path = Path(__file__).with_name("templates")

templates = Environment(loader=FileSystemLoader(template_path))
templates.globals["year"] = datetime.datetime.utcnow().year

licenses = {license.stem: license for license in template_path.joinpath("licenses").glob("*") if license.is_file()}

projects = {project.stem: project for project in template_path.joinpath("projects").glob("*") if project.is_dir()}

with subprocess.Popen(["git", "config", "user.name"], stdout=subprocess.PIPE, encoding="utf-8") as process:
    author = process.stdout.read().strip()
    # TODO: Add a fallback to the system username if git config is not set

with subprocess.Popen(["git", "config", "user.email"], stdout=subprocess.PIPE, encoding="utf-8") as process:
    email = process.stdout.read().strip()
    # TODO: Add a fallback to the system email if git config is not set
