from datetime import datetime
from log import Log
from task import Task
import settings
import sys


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


def add_task():
    task = Task()
    if task:
        print(task)
        item = [{'name': task.name, 'mins': task.mins, 'notes': task.notes, 'date': task.date}]
        return item
    else:
        print('Oops!')


def display_find_menu():
    print('\n Find By...\n')
    print('{}\n{}\n{}\n{}\n{}\n'.format(
        ' (D)ate',
        ' (T)ime spent (range)',
        ' (E)xact Search',
        ' (P)attern',
        ' (Q)uit menu'
    ))
    return ['d', 't', 'e', 'p', 'q']


def prompt_find_choice(choice=''):
    result = None
    while True:
        if choice == 'd':
            date = input('{}'.format(
                '\n Enter a date to search for: Format mm/dd/yyyy: '))
            result = ['date', date]
            break
        elif choice == 't':
            min_time = input('\n Enter MINimum time (in minutes): ')
            max_time = input(' \n Enter MAXimum time (in minutes): ')
            result = ['mins', {'min': min_time, 'max': max_time}]
            break
        elif choice == 'e':
            search = input('\n Enter EXACT search keyword: ')
            result = ['search', search]
        elif choice == 'q':
            break

    return result


def prompt_menu_choice(choices=[]):
    while True:
        choice = input(' Choice: ').lower()
        if choice:
            if choice[0] in choices:
                return choice[0]
            else:
                print(' Sorry, that is not a valid choice.')
        else:
            print(' You must enter a choice.')


def get_prompt(choice, log):
    if choice == 'a':
        item = add_task()
        log.write_to_log(item)

    elif choice == 'f':
        choices = display_find_menu()
        choice = prompt_menu_choice(choices)
        search = prompt_find_choice(choice)
        if search is not None:
            result = log.find_by(search[0], search[1])
            for task in result:
                display_task(task)
        input('Enter to continue')
    elif choice == 'e':
        pass
    elif choice == 'd':
        pass
    elif choice == 'q':
        print('Exiting...')
        sys.exit(0)


def display_main_menu():
    print(' What would you like to do? ')
    print('{}{}'.format(' ', '-'*45))
    print('{}\n{}\n{}\n{}\n{}\n'.format(
        ' (A)dd Task',
        ' (F)ind By',
        ' (E)dit Task',
        ' (D)elete Task',
        ' (Q)uit Application'
    ))
    return ['a', 'f', 'e', 'd', 'q']


def main():
    clear_screen()
    while True:
        log = Log()
        print("\n {}'s WorkLog\n".format(settings.COMPANY_NAME))
        choices = display_main_menu()
        menu_choice = prompt_menu_choice(choices)
        get_prompt(menu_choice, log)

        clear_screen()
    return False

if __name__ == '__main__':
    main()

