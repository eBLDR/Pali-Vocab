import os

from palivocab import config


def clear_screen():
    os.system('clear')


def dash_line(length: int = 15):
    print('= ' * length)


def press_enter_(text: str):
    input(f'{text} | Press <enter> ')


def confirmation():
    valid = ['y', 'n']

    while True:
        action = input('Confirm [y, n]: ')
        if action in valid:
            return action == 'y'


def get_user_input(
        prompt: str, info: str = '', valid_options: list = None,
        accept_shortcuts=False, accept_many=False,
):
    """
    :return: <list> if accept_many else <str>
    """

    def generate_info_string(
            info_='', shortcut_mapper_=None,
    ):
        if not valid_options:
            return info_

        if shortcut_mapper_:
            shortcut_characters = len(list(shortcut_mapper_.keys())[-1])
            valid_options_to_display = [
                f"[{option_[:shortcut_characters].upper()}]{option_[shortcut_characters:]}"
                for option_ in valid_options
            ]

        else:
            valid_options_to_display = valid_options

        if info_:
            info_ += ": "

        if accept_many:
            info_ += f'(comma separated) [{config.ALL_STRING}] '

        info_ += ", ".join(sorted(valid_options_to_display))

        return info_

    shortcut_mapper = {}

    if valid_options:
        valid_options = [
            valid_option.lower() for valid_option in valid_options
        ]

        if accept_shortcuts:
            shortcut_mapper = generate_shortcut_mapper(valid_options)

    if info := generate_info_string(
            info,
            shortcut_mapper_=shortcut_mapper,
    ):
        print(info)

    while True:
        user_input = input(f'{prompt}: ').replace(' ', '').lower()

        if not valid_options:
            if user_input:
                return user_input

            continue

        if not accept_many:
            if user_input in valid_options or user_input in shortcut_mapper:
                return shortcut_mapper.get(user_input) or user_input

            continue

        if user_input == config.ALL_STRING:
            return valid_options

        user_inputs = user_input.split(',')

        for user_input in user_inputs:
            if user_input not in valid_options and user_input not in shortcut_mapper:
                print(f'Wrong option: {user_input}')
                break

        else:
            return [
                shortcut_mapper.get(user_input) or user_input for user_input in user_inputs
            ]


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
