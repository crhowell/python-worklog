import csv
from datetime import datetime
import settings
import sys
from task import Task


def clear_screen():
    """Clears the terminal screen."""
    print("\033c", end="")


def write_to_log(items=[]):
    filepath = settings.FILE_PATH
    try:
        with open(filepath, 'a') as file:
            fieldnames = ['name', 'mins', 'notes', 'date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            for item in items:
                writer.writerow(item)
        return True

    except ValueError:
        print('Could add items to file.')
        return False


def create_file(filepath=''):
    try:
        with open(filepath, 'w') as file:
            fieldnames = ['name', 'mins', 'notes', 'date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'name': 'Stuff', 'mins': 59, 'notes': 'more stuff', 'date': '04-01-2016'})
            return True
    except ValueError:
        print("something else happened")
        return False


def open_file():
    filepath = settings.FILE_PATH
    logreader = {}

    try:
        with open(filepath, newline='') as file:
            logreader = csv.DictReader(file)
            for row in logreader:
                print(row)
    except FileNotFoundError:
        print('Could not find existing log, creating new.')
        create_file(filepath)
    return logreader


def print_delete_menu():
    # Display menu options related to Delete
    pass


def print_edit_menu():
    # Display menu options related to Edit
    pass


def print_find_menu():
    # Display menu options related to Find
    pass


def print_add_menu():
    # Display menu options related to Add
    pass


def prompt_for_delete():
    pass


def prompt_for_edit():
    pass


def prompt_for_find():
    pass


def add_a_task():
    task = Task()
    if task:
        print(task)
        write_to_log([{'name': task.name, 'mins': task.mins, 'notes': task.notes, 'date': task.date}])
    else:
        print('Oops!')



def get_prompt(choice):
    if choice == 'a':
        add_a_task()
    elif choice == 'f':
        prompt_for_find()
    elif choice == 'e':
        prompt_for_edit()
    elif choice == 'd':
        prompt_for_delete()
    elif choice == 'q':
        print('Exiting...')
        sys.exit(0)


def validate_menu_choice(choice=''):
    return True if choice[0] in ['a', 'f', 'e', 'd', 'q'] else False


def prompt_menu_choice():
    return input('Choice: ').lower()


def print_menu():
    print(" What would you like to do? ")
    print("-"*45)
    print(
        '{}\n{}\n{}\n{}\n{}'.format(
        '(A)dd Task',
        '(F)ind By',
        '(E)dit Task',
        '(D)elete Task',
        '(Q)uit Application'
    ))


def main():
    clear_screen()
    open_file()
    print(" Welcome to {}'s WorkLog".format(settings.COMPANY_NAME))
    while True:
        print_menu()
        menu_choice = prompt_menu_choice()
        if validate_menu_choice(menu_choice):
            get_prompt(menu_choice)
        else:
            continue

    # Validate Input
    # Do selected option... 
    # Loop until user 'quits'
    return False


if __name__ == '__main__':
    main()
