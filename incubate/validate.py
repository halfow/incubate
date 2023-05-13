from string import ascii_letters, digits

from email_validator import EmailNotValidError, validate_email
from inquirer import errors


def project_name(answers, current):
    bad_start = set(digits)
    bad_start.update("_")
    allowed = set(ascii_letters)
    allowed.update(bad_start)
    checks = [
        allowed.issuperset(current),
        current[0] not in bad_start,
        current[-1] != "_",
    ]
    if all(checks):
        return True

    raise errors.ValidationError(
        "",
        reason="Invalid project name, only [a-zA-Z0-9_] are allowed.]",
    )


def email(answers, current):
    if validate_email(current):
        return True

    raise errors.ValidationError(
        "",
        reason="Invalid email address.",
    )


def quit(answers, current):
    if current:
        return True
    raise SystemExit(1)
