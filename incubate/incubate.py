import subprocess
from functools import partial
from pathlib import Path
from typing import TypedDict

from rich import print

from . import static, tree


class Answers(TypedDict):
    project: str
    template: str
    description: str
    confirm: bool | None
    author: str
    email: str
    license: str
    init: bool | None


def create_template(answers: Answers):
    name = answers["template"]
    project = answers["project"]

    templates = static.templates.list_templates(filter_func=lambda x: x.startswith(f"projects/{name}"))

    for template in templates:
        path = Path(static.templates.from_string(template).render(project=project.replace("-", "_")))
        new = Path(project, *path.parts[2:-1], path.stem)
        if new.exists():
            print(f"[red]Overwriting existing file:[/red] {new}")
        new.parent.mkdir(parents=True, exist_ok=True)
        new.write_text(static.templates.get_template(template).render(answers), encoding="utf-8")


def print_info(name: str, project: str):
    print(
        "Created Project",
        f"[bold magenta]{project}[/bold magenta]",
        "from",
        f"[magenta]{name}[/magenta]",
        "template",
        tree.walk(project),
        "\n",
    )


def initial_setup(path: str):
    # This should only run for new projects
    # TODO: Make it so that the user may provide a function to run here instead
    run = partial(subprocess.run, check=True, cwd=path)
    run_quiet = partial(subprocess.run, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=path)

    run(["git", "init"])
    run(["pre-commit", "install"])
    run(["pre-commit", "autoupdate"])
    run_quiet(["git", "add", "--all"])
    run_quiet(["pre-commit", "run", "--all"])
    run_quiet(["git", "add", "--all"])
    run(["git", "commit", "-m", "Initial commit"])
