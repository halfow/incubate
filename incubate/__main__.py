import subprocess
from functools import partial
from pathlib import Path

import inquirer
from rich import print

from . import static, theme, tree, validate


def main():
    print(static.logo)

    answers = inquirer.prompt(
        [
            inquirer.Text(
                "project",
                message="Project name",
                validate=validate.project_name,
            ),
            # Check if the project name exists already
            inquirer.Confirm(
                name="confirm",
                message="The project name already exists, do you want to continue?",
                ignore=lambda x: not Path(x["project"]).exists(),
                default=False,
                validate=validate.quit,
            ),
            inquirer.List(
                "type",
                message="Project type",
                choices=static.projects,
            ),
            inquirer.Text(
                "description",
                message="Description",
            ),
            inquirer.Text(
                "author",
                message="Author",
                default=static.author,
            ),
            inquirer.Text(
                "email",
                message="Email",
                validate=validate.email,
                default=static.email,
            ),
            inquirer.List(
                "license",
                message="License",
                choices=static.licenses,
                default="MIT",
            ),
        ],
        theme=theme.Omelette,
    )
    if answers is None:
        raise SystemExit(1)

    project_name = answers["project"]
    project_type = answers["type"]
    templates = static.templates.list_templates(filter_func=lambda x: x.startswith(f"projects/{project_type}"))

    for template in templates:
        path = Path(static.templates.from_string(template).render(project=answers["project"].replace("-", "_")))
        new = Path(project_name, *path.parts[2:-1], path.stem)
        if new.exists():
            print(f"[bold yellow]Overwriting[/bold yellow] '{new!s}'")

        new.parent.mkdir(parents=True, exist_ok=True)
        new.write_text(static.templates.get_template(template).render(**answers))

    print(
        "Created Project",
        f"[bold magenta]{project_name}[/bold magenta]",
        "from",
        f"[magenta]{project_type}[/magenta]",
        "template",
        tree.walk(project_name),
        "\n",
    )

    # NOTE: Exit befor initial setup if the project already exists
    if answers["confirm"]:
        return 0

    # This should only run for new projects
    # TODO: Make it so that the user may provide a function to run here instead
    run = partial(subprocess.run, check=True, cwd=project_name)
    run_quiet = partial(subprocess.run, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=project_name)

    run(["git", "init"])
    run(["pre-commit", "install"])
    run(["pre-commit", "autoupdate"])
    run_quiet(["git", "add", "--all"])
    run_quiet(["pre-commit", "run", "--all"])
    run_quiet(["git", "add", "--all"])
    run(["git", "commit", "-m", "Initial commit"])


if __name__ == "__main__":
    raise SystemExit(main())
