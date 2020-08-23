import os


def clear_screen():
    os.system('clear')


def dash_line(length: int = 15):
    print('= ' * length)


def press_enter_(text: str):
    input(f'{text} | Press <enter> ')


def get_user_input(prompt: str, valid_options: list = None, info: str = None):
    if valid_options:
        valid_options = [
            valid_option.lower() for valid_option in valid_options
        ]

    if info:
        print(info)

    while True:
        user_input = input(f'{prompt}: ').strip(' ').lower()

        if valid_options and user_input not in valid_options:
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
