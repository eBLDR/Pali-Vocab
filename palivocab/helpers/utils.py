import os

from palivocab import config


def clear_screen():
    os.system('clear')


def dash_line(length: int = 15):
    print('= ' * length)


def press_enter_(text: str):
    input(f'{text} | Press <enter> ')


def get_user_input(
        prompt: str, info: str = '', valid_options: list = None,
        accept_option_all=False, accept_shortcuts=False,
):
    def generate_info_string(
            info_='', shortcut_mapper_=None,
    ):
        if not valid_options:
            return info_

        if info_:
            info_ += ": "

        exclude_items = []

        if accept_option_all:
            exclude_items.append(config.ALL_STRING)

        if shortcut_mapper_:
            exclude_items.extend(list(shortcut_mapper_.keys()))

        valid_options_to_display = [
            option for option in valid_options if option not in exclude_items
        ]

        if shortcut_mapper_:
            shortcut_characters = len(exclude_items[-1])
            valid_options_to_display = [
                f"[{option_[:shortcut_characters].upper()}]{option_[shortcut_characters:]}"
                for option_ in valid_options_to_display
            ]

        if accept_option_all:
            info_ += f'[{config.ALL_STRING}] '

        info_ += ", ".join(sorted(valid_options_to_display))

        return info_

    shortcut_mapper = {}

    if valid_options:
        valid_options = [
            valid_option.lower() for valid_option in valid_options
        ]

        if accept_shortcuts:
            shortcut_mapper = generate_shortcut_mapper(valid_options)
            valid_options.extend(list(shortcut_mapper.keys()))

        if accept_option_all:
            valid_options.append(config.ALL_STRING)

    if info := generate_info_string(
            info,
            shortcut_mapper_=shortcut_mapper,
    ):
        print(info)

    while True:
        user_input = input(f'{prompt}: ').strip(' ').lower()

        if valid_options and user_input not in valid_options:
            continue

        if user_input:
            # Check shortcuts
            return shortcut_mapper.get(user_input) or user_input


def get_user_input_integer(prompt: str, max_value: int = None):
    while True:
        user_input = input(f'{prompt} (max. {max_value}): ')

        # Blank for max
        if not user_input:
            return max_value

        if not user_input.isdigit():
            continue

        user_input = int(user_input)

        if max_value and not (0 < user_input <= max_value):
            continue

        return user_input


def generate_shortcut_mapper(terms):
    shortcut_mapper = {}
    characters = 1

    while not shortcut_mapper:

        for term in terms:
            shortcut = term[:characters]
            shortcut_mapper[shortcut] = term

        if len(shortcut_mapper.keys()) != len(terms):
            characters += 1
            shortcut_mapper.clear()

    return shortcut_mapper
