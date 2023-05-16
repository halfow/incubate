"""Gathered data that will not change after its first collected."""
import datetime
import subprocess
from importlib.metadata import version
from pathlib import Path
from random import choice

from jinja2 import Environment, FileSystemLoader

template_path = Path(__file__).with_name("templates")

templates = Environment(
    loader=FileSystemLoader(template_path),
    block_start_string="{§",
    block_end_string="§}",
    variable_start_string="{¤",
    variable_end_string="¤}",
)
templates.globals["year"] = datetime.datetime.utcnow().year

licenses = {license.stem: license for license in template_path.joinpath("licenses").glob("*") if license.is_file()}

projects = {project.stem: project for project in template_path.joinpath("projects").glob("*") if project.is_dir()}

with subprocess.Popen(["git", "config", "user.name"], stdout=subprocess.PIPE, encoding="utf-8") as process:
    author = process.stdout.read().strip()
    # TODO: Add a fallback to the system username if git config is not set

with subprocess.Popen(["git", "config", "user.email"], stdout=subprocess.PIPE, encoding="utf-8") as process:
    email = process.stdout.read().strip()
    # TODO: Add a fallback to the system email if git config is not set

color = choice(
    [
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
    ]
)
ver = "v" + version("incubate")
logo = f"""
            [grey0 on white]████████[/grey0 on white]
          [grey0 on white]██        ██[/grey0 on white]
        [grey0 on white]██▒▒▒▒        ██[/grey0 on white]
      [grey0 on white]██▒▒▒▒▒▒      ▒▒▒▒██[/grey0 on white]
    [grey0 on white]██  ▒▒▒▒        ▒▒▒▒▒▒██[/grey0 on white]
    [grey0 on white]██                ▒▒▒▒██[/grey0 on white]     ▄█         ▄▄           ▄▄   ▄█      ▄▄▄▄▀ ▄▄▄▄
  [grey0 on white]██▒▒      ▒▒▒▒▒▒          ██[/grey0 on white]   ██     █  █▀ ▀▄     ▄  █  █  █ █  ▀▀▀ █   ▐█   ▀
  [grey0 on white]██      ▒▒▒▒▒▒▒▒▒▒        ██[/grey0 on white]   ██ ██   █ █   ▀  █   █ █ ▀ ▄ █▄▄█     █   ▐█▀▀
  [grey0 on white]██      ▒▒▒▒▒▒▒▒▒▒    ▒▒▒▒██[/grey0 on white]   ▐█ █ █  █ █▄  ▄▀ █   █ █  ▄▀ █  █    █    ▀█▄▄▄▀
  [grey0 on white]██▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒██[/grey0 on white]    ▐ █  █ █ ▀███▀  █▄ ▄█  ▀▀      █   ▀
    [grey0 on white]██▒▒▒▒  ▒▒▒▒▒▒    ▒▒▒▒██[/grey0 on white]        █   ██         ▀▀▀          ▀
      [grey0 on white]██▒▒              ██[/grey0 on white]          ▀              [bold cyan]{ver:>30}[/bold cyan]
        [grey0 on white]████        ████[/grey0 on white]
            [grey0 on white]████████[/grey0 on white]
""".replace(
    "▒", f"[{color}]█[/{color}]"
)

if __name__ == "__main__":
    from rich import print

    print(logo)
