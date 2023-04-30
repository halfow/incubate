from pathlib import Path

import inquirer
from rich import print

from . import static, tree, validate


def main():
    answers = inquirer.prompt(
        [
            inquirer.Text(
                "project",
                message="Project name",
                validate=validate.cname,
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
            inquirer.Text(
                "description",
                message="Description",
            ),
            inquirer.List(
                "license",
                message="License",
                choices=static.licenses,
                default="MIT",
            ),
        ]
    )
    if answers is None:
        raise SystemExit(1)

    project_name = answers["project"]
    project_type = answers["type"]
    templates = static.templates.list_templates(filter_func=lambda x: x.startswith(f"projects/{project_type}"))

    print(
        "Created Project",
        f"[bold magenta]{project_name}[/bold magenta]",
        "from",
        f"[dim magenta]{project_type}[/dim magenta]",
        "template",
    )
    for template in templates:
        p = Path(static.templates.from_string(template).render(**answers))
        final = Path(project_name, *p.parts[2:-1], p.stem)
        final.parent.mkdir(parents=True, exist_ok=True)
        if final.exists():
            print(f"[bold yellow]Skipping[/bold yellow] '{final!s}' as it already exists")
        else:
            final.write_text(static.templates.get_template(template).render(**answers))

    print(tree.walk(project_name))


if __name__ == "__main__":
    raise SystemExit(main())
