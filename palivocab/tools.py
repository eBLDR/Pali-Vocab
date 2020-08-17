import os


def clear_screen():
    os.system('clear')


def dash_line(length=15):
    print('= ' * length)


def press_enter_(text='Next...'):
    input(f'{text} | Press <enter> ')
