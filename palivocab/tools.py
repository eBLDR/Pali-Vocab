import os


def clear_screen():
    os.system('clear')


def dash_line(length=15):
    print('= ' * length)


def press_enter_(text):
    input(f'{text} | Press <enter> ')


def get_user_input(prompt, valid_options=None):
    if valid_options:
        valid_options = [
            valid_option.lower() for valid_option in valid_options
        ]

    while True:
        user_input = input(f'{prompt}: ').lower()

        if valid_options and user_input not in valid_options:
            continue

        if user_input:
            return user_input


def get_user_input_integer(prompt, max_value=None):
    while True:
        user_input = input(f'{prompt} (max. {max_value}): ')

        if not user_input.isdigit():
            continue

        user_input = int(user_input)

        if max_value and not (0 < user_input <= max_value):
            continue

        return user_input
