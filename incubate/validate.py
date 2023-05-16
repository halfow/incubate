from string import ascii_letters, digits

from email_validator import validate_email
from inquirer import errors


def project_name(answers, current: str):
    bad_end = "_-"
    bad_start = set(digits)
    bad_start.update(bad_end)
    allowed = set(ascii_letters)
    allowed.update(bad_start)
    checks = [
        (lambda x: len(x) > 0, "must not be empty"),
        (allowed.issuperset, "alphanumeric and '-_' characters are allowed"),
        (lambda x: x[0] not in bad_start, "may not start with a digit, '-' or '_'"),
        (lambda x: x[-1] not in bad_end, "may not end with '-' or '_'"),
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
