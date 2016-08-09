from datetime import datetime
from log import Log
import re
import settings
import sys
from task import Task


class WorkLog:
    """A WorkLog interacts between a Task and a Log.

    It contains all the methods for a user to interact
    with a Log. This includes menus, user input for prompts,
    displaying single or navigating a list of paginated tasks.
    """

    def find_by_date(self, date=''):
        """Returns a list of 1 Task index.

        Keyword arguments:
        idx -- Choice from date list
        """
        result = []
        if date:
            for i, task in enumerate(self.tasks):
                if date == task.task_date():
                    result.append(i)
        return result

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
        elif key == 'range':
            result = self.find_date_range(value[0], value[1])

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
                self.convert_display_date(self.tasks[idx].task_date())
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
                self.clear_screen()
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
                    self.prompt_action_status('Task updated')
                    self.log.rewrite_the_log(self.tasks)
                    break
                elif choice == 'd':
                    options = self.display_verify()
                    option_choice = self.prompt_menu_choice(options)
                    if option_choice == 'y':
                        self.delete_task(indices[i])
                        self.log.rewrite_the_log(self.tasks)
                        self.prompt_action_status('Task Deleted')
                    else:
                        self.prompt_action_status('Task was NOT deleted')
                    break
                elif choice == 'q':
                    break
        else:
            print('There are no tasks to show.')

    def find_date_range(self, date1, date2):
        d1 = self.convert_to_date(date1)
        d2 = self.convert_to_date(date2)

        result = []
        for i, task in enumerate(self.tasks):
            curr_date = self.convert_to_date(task.task_date())
            if d2 > d1:
                if d1 <= curr_date <= d2:
                    result.append(i)
            else:
                if d2 <= curr_date <= d1:
                    result.append(i)
        return result

    def display_by_date(self):
        """Display to the terminal all tasks by date, enumerated

        Keyword arguments:
        tasks -- a list of Task objects
        """
        self.clear_screen()
        group = self.group_dates()
        print('\n Tasks by Date')
        print('{}{}'.format(' ', '-' * 45))
        for i in range(len(group[0])):
            print(' {} {}'.format(
                group[0][i],
                group[1][i]
            ))

        return group

    def group_dates(self):
        """Groups tasks into a dict by numbered dates."""
        group = [[], []]
        for i, task in enumerate(self.tasks):
            if task.task_date() not in group[1]:
                group[0].append(str(i+1))
                group[1].append(task.task_date())
        return group

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
                    choice = self.prompt_menu_choice(choices[0])
                    if Task.valid_num(choice):
                        index = int(choice) - 1
                        result = ['date', choices[1][index]]
                else:
                    self.prompt_action_status('Sorry, no items to show')
                break
            elif choice == 'r':
                print(' Date format is: mm/dd/yyyy')
                date1 = self.prompt_for_date('First Date')
                date2 = self.prompt_for_date('Second Date')
                result = ['range', [date1, date2]]
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
            self.prompt_action_status('Task Added')
            self.clear_screen()

        elif choice == 'f':
            choices = self.display_find_menu()
            choice = self.prompt_menu_choice(choices)
            search = self.prompt_find_choice(choice)
            if search is not None:
                result = self.find_task(search[0], search[1])
                if result:
                    self.display_paginated(result)
                else:
                    self.prompt_action_status('No results found')

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
            print('\n * Leave it blank to continue without changing value. *')
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
    def convert_to_date(date=''):
        if Task.valid_date(date):
            return datetime.strptime(date, '%m/%d/%Y')

    @staticmethod
    def prompt_for_date(prmpt='Date'):
        while True:
            date = input(' {}: '.format(prmpt))
            if Task.valid_date(date):
                return date

    @staticmethod
    def prompt_action_status(prompt='\n'):
        input('\n {}. Press ENTER to continue.'.format(prompt))

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

    def display_find_menu(self):
        """Display to terminal, the Find sub-menu"""
        self.clear_screen()
        print('\n Find By...')
        print('{}{}'.format(' ', '-' * 45))
        print('{}\n{}\n{}\n{}\n{}\n{}\n'.format(
            ' (L)ist of Existing Dates',
            ' (R)ange of Dates',
            ' (T)ime spent (range)',
            ' (E)xact Search',
            ' (P)attern RegEx Search',
            ' (Q)uit menu'
        ))
        return ['l', 'r', 't', 'e', 'p', 'q']

    @staticmethod
    def convert_display_date(date, fmt='%m/%d/%Y'):
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
