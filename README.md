# Incubate your new ideas with a quick start

Scaffolding like tool for new python projects that assumes you use git.

## Installation

pipx installation is recommended.

```bash
pipx install git+https://github.com/halfow/pyproject.git
pipx install pre-commit # This is a dependency for the hatched project
```

For regular pip installation:

```bash
# Its recommended to use a virtual environment to avoid polluting your system
python3 -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/halfow/pyproject.git
```

## Usage

Simply run `incubate` where you want to create a new project. And follow the instructions.

## TODO

- Add argument parser to set some defaults
- Add user config dir to allow
  - custom templates
  - changes to the default templates
- Add a way to template "jinja templates"
