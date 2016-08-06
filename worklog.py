import settings
import sys
from log import Log
from task import Task

CHOICES = ['a', 'f', 'e', 'd', 'q']


def clear_screen():
    print('\033c', end='')


def validate_menu_choice(choice=''):
    return True if choice[0] in CHOICES else False


def add_task():
    task = Task()
    if task:
        print(task)
        item = [{'name': task.name, 'mins': task.mins, 'notes': task.notes, 'date': task.date}]
        return item
    else:
        print('Oops!')

def get_prompt(choice, log):
    if choice == 'a':
        item = add_task()
        log.write_to_log(item)

    elif choice == 'f':
        pass
    elif choice == 'e':
        pass
    elif choice == 'd':
        pass
    elif choice == 'q':
        print('Exiting...')
        sys.exit(0)


def prompt_menu_choice():
    return input(' Choice: ').lower()


def print_menu():
    print(' What would you like to do? ')
    print('{}{}'.format(' ', '-'*45))
    print('{}\n{}\n{}\n{}\n{}\n'.format(
        ' (A)dd Task',
        ' (F)ind By',
        ' (E)dit Task',
        ' (D)elete Task',
        ' (Q)uit Application'
    ))


def main():
    clear_screen()
    log = Log()
    print("\n Welcome to {}'s WorkLog\n".format(settings.COMPANY_NAME))
    while True:
        print_menu()
        menu_choice = prompt_menu_choice()
        if validate_menu_choice(menu_choice):
            get_prompt(menu_choice, log)
        else:
            continue
    return False

if __name__ == '__main__':
    main()

