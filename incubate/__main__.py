from pathlib import Path

import inquirer
from rich import print

from . import static, theme, validate
from .incubate import create_template, initial_setup, print_info


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
                "template",
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
            inquirer.Confirm(
                name="init",
                message="Initialize project?",
                default=True,
            ),
        ],
        theme=theme.Omelette,
    )

    if answers is None:
        raise SystemExit(1)

    create_template(answers)
    print_info(answers["template"], answers["project"])

    if answers["init"]:
        initial_setup(answers["project"])


if __name__ == "__main__":
    raise SystemExit(main())
