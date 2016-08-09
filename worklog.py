from datetime import datetime
from log import Log
from task import Task
import re
import settings
import sys

class WorkLog:

    def find_by_date(self, idx):
        """Returns a list of 1 Task index.

        Keyword arguments:
        idx -- Choice from date list
        """
        return [idx - 1]

    def find_by_pattern(self, pattern=''):
        """Returns a list of tasks that match the pattern.

        Keyword arguments:
        pattern -- String or regex pattern to search for.
        """
        result = []
        if pattern:
            for key, task in enumerate(self.tasks):
                match_name = re.match(pattern, task.task_name())
                match_notes = re.match(pattern, task.task_notes())
                if match_name is not None or match_notes is not None:
                    result.append(key)
        return result

    def find_task(self, key='', value=''):
        """Returns result of indices of tasks.

        Keyword arguments:
        key -- string of how value should be handled.
        value -- search value of what we are looking for.

        """
        result = []
        if key == 'search' or key == 'regex':
            result = self.find_by_pattern(value)
        elif key == 'mins':
            result = [key for key, task in enumerate(self.tasks)
                      if value['min'] <= task.minutes() <= value['max']]
        elif key == 'date':
            result = self.find_by_date(value)

        return result

    def display_task(self, idx=None):
        """Display to the terminal a given task.

        Keyword arguments:
        task -- a Task object
        """
        if idx is not None:
            print('=' * 45)
            print(' Task Name: {}\n Minutes Spent: {}\n Notes: {}\n Date: {}'.format(
                self.tasks[idx].task_name(),
                self.tasks[idx].minutes(),
                self.tasks[idx].task_notes(),
                self.convert_date(self.tasks[idx].task_date())
            ))
            print('=' * 45)

    def display_paginated(self, indices=[]):
        """Displays a task one-by-one,
        using next, previous, quit options to cycle.

        Keyword arguments:
        tasks -- a list of tasks display paginated
        """
        if indices:
            i = 0
            while True:
                page_dir = self.allowable_page_dir(i, len(indices))
                choices = [key for key in page_dir]
                self.display_task_count(i + 1, len(indices))
                self.display_task(indices[i])
                prompt = ' | '.join([page_dir[key] for key in choices])
                choice = self.prompt_menu_choice(choices, '[{}]: '.format(prompt))
                if choice == 'p':
                    i -= 1
                elif choice == 'n':
                    i += 1
                elif choice == 'e':
                    self.edit_task(indices[i])
                    input('Task Updated, Press ENTER to continue.')
                    self.log.rewrite_the_log(self.tasks)
                    break
                elif choice == 'd':
                    options = self.display_verify()
                    option_choice = self.prompt_menu_choice(options)
                    if option_choice == 'y':
                        self.delete_task(indices[i])
                        self.log.rewrite_the_log(self.tasks)
                        input('Task Deleted, Press ENTER to continue.')
                    else:
                        input('Task was NOT deleted, Press ENTER to continue.')
                    break
                elif choice == 'q':
                    break
        else:
            print('There are no tasks to show.')

    def display_by_date(self):
        """Display to the terminal all tasks by date, enumerated

        Keyword arguments:
        tasks -- a list of Task objects
        """
        print(' Tasks by Date')
        print('{}{}'.format(' ', '-' * 45))
        for i, task in enumerate(self.tasks):
            print(' {} {} - {}'.format(
                i + 1,
                task.task_date(),
                task.task_name()
            ))
        return [str(i + 1) for i in range(len(self.tasks))]

    def prompt_find_choice(self, choice=''):
        """Prompt user for input,
        based on choice from Find sub-menu.

        Keyword arguments:
        choice -- a string input choice
        """
        result = None
        while True:
            if choice == 'l':
                choices = self.display_by_date()
                if choices:
                    print('\n Choose a date by entering the number(left) of the date.')
                    choice = self.prompt_menu_choice(choices)
                    if Task.valid_num(choice):
                        result = ['date', int(choice)]
                else:
                    input('Sorry, no items to show. Press ENTER to continue.')
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
                search = input('\n Enter exact search keyword: ')
                result = ['search', search]
                break
            elif choice == 'p':
                pattern = input('\n Enter the RegEx pattern to search for: ')
                result = ['regex', pattern]
                break
            elif choice == 'q':
                break

        return result

    def get_prompt(self, choice):
        """Prompts user for input,
        based-on choice given from Main menu selection.

        Keyword arguments:
        choice -- input choice for main menu
        log -- a Log object
        """
        if choice == 'a':
            item = self.create_task()
            self.log.write_to_log(item)

        elif choice == 'f':
            choices = self.display_find_menu()
            choice = self.prompt_menu_choice(choices)
            search = self.prompt_find_choice(choice)
            if search is not None:
                result = self.find_task(search[0], search[1])
                self.display_paginated(result)

        elif choice == 'q':
            self.clear_screen()
            print('\n Exiting...')
            print("\n Thanks for using {}'s Worklog".format(
                settings.COMPANY_NAME
            ))
            print(' Have a great day!')
            sys.exit(0)

    def main(self):
        """Runs main program loop,
        prompts for main menu input.
        """
        self.clear_screen()
        while True:
            self.tasks = self.log.open_file()
            print("\n {}'s WorkLog\n".format(settings.COMPANY_NAME))
            choices = self.display_main_menu()
            menu_choice = self.prompt_menu_choice(choices)
            self.get_prompt(menu_choice)

            self.clear_screen()
        return False

    def delete_task(self, idx=None):
        if idx is not None:
            del self.tasks[idx]

    def edit_task(self, idx=None):
        """Modify the selected task.

        Keyword arguments:
        task -- a Task object
        """
        if self.tasks[idx] is not None:
            self.tasks[idx].update_all()

    def create_task(self):
        """Creates Task and returns as dict to write to file."""
        task = Task()
        if task:
            item = [{'name': task.name,
                     'mins': task.mins,
                     'notes': task.notes,
                     'date': task.date}]
            return item
        else:
            print('Oops! Task was not created.')

    @staticmethod
    def prompt_menu_choice(choices=[], prompt=' Choice: '):
        """Prompts and validates a choice,
        based-on list of valid choices.

        Keyword arguments:
        choices -- list of valid choices
        prompt -- prompt to be displayed
        """
        # TODO
        while True:
            choice = input(' {} '.format(prompt)).lower()
            if choice:
                if choice[0] in choices:
                    return choice[0]
                else:
                    print('\n Try again, that was not a valid choice.')
            else:
                print('\n Try again, you must enter a choice.')

    @staticmethod
    def display_verify():
        print(' ** ARE YOU SURE? (Y)/(N)')
        return ['y', 'n']

    @staticmethod
    def display_task_count(curr=None, count=None):
        """Displays to terminal
        task number and total number of tasks.

        Keyword arguments:
        curr -- current number
        count -- count of tasks
        """
        if curr is not None and count is not None:
            print('\n Task {} of {}\n'.format(curr, count))

    @staticmethod
    def display_main_menu():
        """Displays to terminal the Main Menu selections."""
        print(' What would you like to do? ')
        print('{}{}'.format(' ', '-' * 45))
        print('{}\n{}\n{}\n'.format(
            ' (A)dd Task',
            ' (F)ind A Task',
            ' (Q)uit Application'
        ))
        return ['a', 'f', 'q']

    @staticmethod
    def display_find_menu():
        """Display to terminal, the Find sub-menu"""
        print('\n Find By...')
        print('{}{}'.format(' ', '-' * 45))
        print('{}\n{}\n{}\n{}\n{}\n{}\n'.format(
            ' (L)ist of Existing Dates',
            ' (R)ange between Dates',
            ' (T)ime spent (range)',
            ' (E)xact Search',
            ' (P)attern RegEx Search',
            ' (Q)uit menu'
        ))
        return ['l', 't', 'e', 'p', 'q']

    @staticmethod
    def convert_date(date, fmt='%m/%d/%Y'):
        """Converts a date to settings DATE_DISPLAY_FORMAT

        Keyword arguments:
        date -- user input date
        fmt -- format of input date
        """
        return datetime.strptime(date, fmt).strftime(
            settings.DATE_DISPLAY_FORMAT)

    @staticmethod
    def clear_screen():
        """Clears the terminal screen"""
        print('\033c', end='')

    @staticmethod
    def allowable_page_dir(num, size):
        """Returns list of allowable pagination directions.

        Keyword arguments:
        num -- Current task number
        size -- Size of the list of tasks
        """
        choices = {
            'e': '(E)dit',
            'd': '(D)elete',
            'p': '(P)revious',
            'n': '(N)ext',
            'q': '(Q)uit'
        }
        if 0 < num < size - 1:
            return choices
        elif num == 0:
            del choices['p']
            if num == size - 1:
                del choices['n']
            return choices
        else:
            del choices['n']
            return choices

    def __init__(self):
        self.log = Log(fields=Task.FIELDS)
        self.tasks = self.log.open_file()


if __name__ == '__main__':
    worklog = WorkLog()
    worklog.main()
