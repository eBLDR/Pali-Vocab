import os


def clear_screen():
    os.system('clear')


def dash_line(length: int = 15):
    print('= ' * length)


def press_enter_(text: str):
    input(f'{text} | Press <enter> ')


def get_user_input(prompt: str, valid_options: list = None, info: str = '', accept_shortcuts=False):
    shortcut_mapper = {}

    if valid_options:
        valid_options = [
            valid_option.lower() for valid_option in valid_options
        ]

        if accept_shortcuts:
            shortcut_mapper = generate_shortcut_mapper(valid_options)
            valid_options.extend(list(shortcut_mapper.keys()))

    if valid_options:
        if info:
            info += ": "

        if shortcut_mapper:
            characters = len(list(shortcut_mapper.values())[0])
            info_valid_options = ", ".join(
                [f"[{option[:characters].upper()}]{option[characters:]}" for option in valid_options]
            )
        else:
            info_valid_options = ", ".join(valid_options)

        info += info_valid_options

    if info:
        print(info)

    while True:
        user_input = input(f'{prompt}: ').strip(' ').lower()

        if valid_options:
            # Check shortcuts
            if option := shortcut_mapper.get(user_input):
                return option

            if user_input not in valid_options:
                continue

        if user_input:
            return user_input


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


def generate_shortened_input_options(options):
    return [
        option[0] for option in options
    ]


def generate_shortcut_mapper(terms):
    shortcut_mapper = {}

    while not shortcut_mapper:
        characters = 1

        for term in terms:
            shortcut = term[:characters]
            shortcut_mapper[shortcut] = term

        if len(shortcut_mapper.keys()) != len(terms):
            characters += 1
            shortcut_mapper.clear()

    return shortcut_mapper
