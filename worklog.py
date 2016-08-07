from datetime import datetime
from log import Log
from task import Task
import settings
import sys


def clear_screen():
    """Clears the terminal screen"""
    print('\033c', end='')


def prompt_menu_choice(choices=[], prompt=' Choice: '):
    """Prompts and validates a choice,
    based-on list of valid choices.

    Keyword arguments:
    choices -- list of valid choices
    prompt -- prompt to be displayed
    """
    while True:
        choice = input(' {} '.format(prompt)).lower()
        if choice:
            if choice[0] in choices:
                return choice[0]
            else:
                print('\n Try again, that was not a valid choice.')
        else:
            print('\n Try again, you must enter a choice.')


def convert_date(date, fmt='%m/%d/%Y'):
    """Converts a date to settings DATE_DISPLAY_FORMAT

    Keyword arguments:
    date -- user input date
    fmt -- format of input date
    """
    return datetime.strptime(date, fmt).strftime(
        settings.DATE_DISPLAY_FORMAT)


def display_by_date(tasks):
    """Display to the terminal all tasks by date, enumerated

    Keyword arguments:
    tasks -- a list of Task objects
    """
    print(' Tasks by Date')
    print('{}{}'.format(' ', '-'*45))
    for i, task in enumerate(tasks):
        print(' {} {} - {}'.format(
            i+1,
            task.task_date(),
            task.task_name()
        ))

    return [str(i+1) for i in range(len(tasks))]


def display_task(task):
    """Display to the terminal a given task.

    Keyword arguments:
    task -- a Task object
    """
    print('=' * 45)
    print(' Task Name: {}\n Minutes Spent: {}\n Notes: {}\n Date: {}'.format(
        task.task_name(),
        task.minutes(),
        task.task_notes(),
        convert_date(task.task_date())
    ))
    print('=' * 45)


def allowable_page_dir(num, size):
    """Returns list of allowable pagination directions.

    Keyword arguments:
    num -- Current task number
    size -- Size of the list of tasks
    """
    choices = {
        'p': '(P)revious',
        'n': '(N)ext',
        'q': '(Q)uit'
    }
    if 0 < num < size - 1:
        return choices
    elif num == 0:
        del choices['p']
        if num == size-1:
            del choices['n']
        return choices
    else:
        del choices['n']
        return choices


def display_task_count(curr, count):
    """Displays to terminal
    task number and total number of tasks.

    Keyword arugments:
    curr -- current number
    count -- count of tasks
    """
    print('\n Task {} of {}\n'.format(curr, count))


def display_paginated(tasks=[]):
    """Displays a task one-by-one,
    using next, previous, quit options to cycle.

    Keyword arguments:
    tasks -- a list of tasks display paginated
    """
    if tasks:
        i = 0
        while True:
            page_dir = allowable_page_dir(i, len(tasks))
            choices = [key for key in page_dir]
            display_task_count(i + 1, len(tasks))
            display_task(tasks[i])
            prompt = ' | '.join([page_dir[key] for key in choices])
            choice = prompt_menu_choice(choices, '[{}]: '.format(prompt))
            if choice == 'p':
                i -= 1
            elif choice == 'n':
                i += 1
                pass
            elif choice == 'q':
                break
    else:
        print('There are no tasks to show.')


def edit_task(task=None):
    """Modify the selected task.

    Keyword arguments:
    task -- a Task object
    """
    if task is not None:
        task.update_all()


def create_task():
    """Creates Task and returns as dict to write to file."""
    task = Task()
    if task:
        item = [{'name': task.name,
                 'mins': task.mins,
                 'notes': task.notes,
                 'date': task.date}]
        return item
    else:
        print('Oops!')


def display_find_menu():
    """Display to terminal, the Find sub-menu"""
    print('\n Find By...')
    print('{}{}'.format(' ', '-'*45))
    print('{}\n{}\n{}\n{}\n{}\n'.format(
        ' (D)ate',
        ' (T)ime spent (range)',
        ' (E)xact Search',
        ' (P)attern',
        ' (Q)uit menu'
    ))
    return ['d', 't', 'e', 'p', 'q']


def prompt_find_choice(choice='', log=None):
    """Prompt user for input,
    based on choice from Find sub-menu.

    Keyword arguments:
    choice -- a string input choice
    """
    result = None
    while True:
        if choice == 'd':
            choices = display_by_date(log.all_tasks())
            print(' Choose a date by entering the number(left) of the date.')
            choice = prompt_menu_choice(choices)
            if Task.valid_num(choice):
                result = ['date', int(choice)]
            break
        elif choice == 't':
            min_time = input('\n Enter MINimum time (in minutes): ')
            if Task.valid_num(min_time):
                max_time = input(' \n Enter MAXimum time (in minutes): ')
                if Task.valid_num(max_time):
                    result = ['mins', {'min': int(min_time),
                                       'max': int(max_time)}]
                    break
                else:
                    print('\n ** Please enter a valid MAX time.')
            else:
                print('\n ** Please enter a valid MIN time.')

        elif choice == 'e':
            search = input('\n Enter EXACT search keyword: ')
            result = ['search', search]
            break
        elif choice == 'q':
            break

    return result


def get_prompt(choice, log):
    """Prompts user for input,
    based-on choice given from Main menu selection.

    Keyword arguments:
    choice -- input choice for main menu
    log -- a Log object
    """
    if choice == 'a':
        item = create_task()
        log.write_to_log(item)

    elif choice == 'f':
        choices = display_find_menu()
        choice = prompt_menu_choice(choices)
        search = prompt_find_choice(choice, log)
        if search is not None:
            result = log.find_task(search[0], search[1])
            display_paginated(result)
    elif choice == 'e':
        print(' Task updated.')
        input(' Enter to continue...')
    elif choice == 'd':
        print(' Task Deleted.')
        input(' Enter to continue...')
    elif choice == 'q':
        clear_screen()
        print('\n Exiting...')
        print("\n Thanks for using {}'s Worklog".format(
            settings.COMPANY_NAME
        ))
        print(' Have a great day!')
        sys.exit(0)


def display_main_menu():
    """Displays to terminal the Main Menu selections."""
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
    """Runs main program loop,
    prompts for main menu input.
    """
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

