from inquirer.themes import load_theme_from_dict

Omelette = load_theme_from_dict(
    {
        "Question": {
            "mark_color": "yellow",
            "brackets_color": "normal",
            "default_color": "normal",
        },
        "Editor": {
            "opening_prompt_color": "bright_black",
        },
        "Checkbox": {
            "selection_color": "cyan",
            "selection_icon": "➤",
            "selected_icon": " ◉",
            "selected_color": "yellow",
            "unselected_color": "normal",
            "unselected_icon": " ◯",
            "locked_option_color": "gray50",
        },
        "List": {
            "selection_color": "cyan",
            "selection_cursor": "➤ ",
            "unselected_color": "normal",
        },
    }
)
