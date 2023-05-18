from string import ascii_letters, digits

from email_validator import validate_email
from inquirer import errors

BAD_PROJECT_NAME_END = "_-"
BAD_PROJECT_NAME_START = BAD_PROJECT_NAME_END + digits
PROJECT_NAME_ALLOWED_CHARACTERS = BAD_PROJECT_NAME_START + ascii_letters


def project_name(answers, current: str):
    checks = [
        (lambda x: len(x) > 0, "must not be empty"),
        (set(PROJECT_NAME_ALLOWED_CHARACTERS).issuperset, "alphanumeric and '-_' characters are allowed"),
        (lambda x: x[0] not in BAD_PROJECT_NAME_START, "may not start with a digit, '-' or '_'"),
        (lambda x: x[-1] not in BAD_PROJECT_NAME_END, "may not end with '-' or '_'"),
    ]
    for check, reason in checks:
        if not check(current):
            raise errors.ValidationError("", f"Invalid project name, {reason}.")
    return True


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
