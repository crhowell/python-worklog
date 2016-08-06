from datetime import datetime
from log import Log
from task import Task
import settings
import sys

CHOICES = ['a', 'f', 'e', 'd', 'q']


def clear_screen():
    print('\033c', end='')


def convert_date(date, fmt='%m/%d/%Y'):
    return datetime.strptime(date, fmt).strftime(
        settings.DATE_DISPLAY_FORMAT)


def display_task(task):
        print('='*45)
        print(' Task Name: {}\n Minutes Spent: {}\n Notes: {}\n Date: {}'.format(
            task['name'],
            task['mins'],
            task['notes'],
            convert_date(task['date'])
        ))
        print('='*45)


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


def prompt_find_menu():
    OPTIONS = ['d', 't', 'e', 'p', 'q']
    print('\n Find By...\n')
    while True:
        print('{}\n{}\n{}\n{}\n{}\n'.format(
            ' (D)ate',
            ' (T)ime spent',
            ' (E)xact Search',
            ' (P)attern',
            ' (Q)uit menu'
        ))
        choice = input(' Choice: ').lower()
        result = None
        if choice:
            if choice[0] in OPTIONS:
                if choice == 'd':
                    date = input('{}'.format(
                        '\n Enter a date to search for: Format mm/dd/yyyy: '))
                    result = ['date', date]

                elif choice == 't':
                    time = input('\n Enter time spent (in minutes): ')

                elif choice == 'e':
                    search = input('\n Enter EXACT search keyword: ')

                elif choice == 'p':
                    pattern = input('\n Enter a regex pattern to look for: ')

                elif choice == 'q':
                    break
            else:
                print('Sorry, that was not an option. Try again.')
        else:
            print('You must enter something. Try again.')

        return result


def get_prompt(choice, log):
    if choice == 'a':
        item = add_task()
        log.write_to_log(item)

    elif choice == 'f':
        choice = prompt_find_menu()
        if choice is not None:
            result = log.find_by(choice[0], choice[1])
            for task in result:
                display_task(task)
            input('Enter to continue')
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
    while True:
        log = Log()
        print("\n {}'s WorkLog\n".format(settings.COMPANY_NAME))
        print_menu()
        menu_choice = prompt_menu_choice()
        if menu_choice:
            if validate_menu_choice(menu_choice[0]):
                get_prompt(menu_choice, log)
            else:
                continue
        else:
            continue

        clear_screen()
    return False

if __name__ == '__main__':
    main()

