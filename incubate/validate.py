import re

from inquirer import errors


def cname(answers, current):
    pattern = re.compile(r"^[a-zA-Z0-9_]+$")
    if pattern.match(current):
        return True

    raise errors.ValidationError(
        "",
        reason="Invalid project name, only [a-zA-Z0-9_] are allowed.]",
    )


def email(answers, current):
    pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if pattern.match(current):
        return True

    raise errors.ValidationError(
        "",
        reason="Invalid email address.",
    )


def quit(answers, current):
    if current:
        return True
    raise SystemExit(1)
