"""
Tests for the default template creation.
"""
from itertools import product
from subprocess import Popen, run

import pytest
from hypothesis import given
from hypothesis.strategies import emails, sampled_from, text
from inquirer.errors import ValidationError

from incubate import static
from incubate.incubate import create_template, initial_setup
from incubate.validate import PROJECT_NAME_ALLOWED_CHARACTERS, project_name


def valid_project_name(x):
    try:
        return project_name({}, x)
    except ValidationError:
        return False


templates = list(static.projects.keys())


@given(
    project=text(PROJECT_NAME_ALLOWED_CHARACTERS).filter(valid_project_name),
    description=text(),
    author=text(),
    email=emails(),
    license=sampled_from(list(static.licenses.keys())),
)
@pytest.mark.parametrize("template", templates)
@pytest.mark.usefixtures("tmp_location")
def test_create_template(project, template, description, author, email, license):  # noqa: PLR0913
    """
    Test template creation by fuzzing the allowed inputs and possible permutations.
    """
    answers = {
        "project": project,
        "template": template,
        "description": description,
        "author": author,
        "email": email,
        "license": license,
    }
    create_template(answers)


@pytest.mark.parametrize(
    ("template", "init"),
    (
        pytest.param(template, init, id=template + " with init" * init)
        for template, init in product(templates, (True, False))
    ),
)
@pytest.mark.usefixtures("tmp_location")
def test_build_template(template, init):  # noqa: PLR0913
    """
    Test all the generation functions and test that the template builds without errors.
    """
    name = f"test_{template}"
    answers = {
        "project": name,
        "template": template,
        "description": "",
        "author": "woho",
        "email": "a@b.com",
        "license": "MIT",
    }
    create_template(answers)

    if init:
        initial_setup(name)
    else:
        # scm needs to be initialized for setuptools_scm to work
        run(["git", "init"], cwd=name)

    with Popen(["pip", "install", "."], cwd=name) as proc:
        stdout, strerr = proc.communicate()
        assert proc.returncode == 0, f"stdout: {stdout}\nstderr: {strerr}"
