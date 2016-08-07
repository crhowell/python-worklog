import csv
from datetime import datetime
import settings
from task import Task


class Log:
    """A Log is an instance representation of a CSV file.

    The contents of the CSV log file are loaded into an instance
    of a Log. Any changes to the log with actions such as
    add, delete, and edit will cause the Log's state to be
    saved to the file and the instance to be reloaded.
    """

    def find_by_date(self, idx):
        """Returns a list containing 1 task item.

        Keyword arguments:
        idx -- index choice from enumerated date list
        """
        i = idx - 1
        return [self.tasks[i]]

    def search_by_term(self, term=''):
        """Returns a list of tasks matching a term.

        Keyword arguments:
        term -- Search keyword term
        """
        result = []
        if term:
            for task in self.tasks:
                if term in task.task_name():
                    result.append(task)
                if term in task.task_notes():
                    if task not in result:
                        result.append(task)
        return result

    def find_task(self, key='', value=''):
        """Returns result of given key action.

        Keyword arguments:
        key -- string of how value should be handled.
        value -- search value of what we are looking for.

        """
        result = []
        if key == 'search':
            result = self.search_by_term(value)
        elif key == 'regex':
            result = []
        elif key == 'mins':
            result = [task for task in self.tasks
                      if value['min'] <= task.minutes() <= value['max']]
        elif key == 'date':
            result = self.find_by_date(value)

        return result

    def write_to_log(self, items=[]):
        """Appends to file, list of items.

        Keyword arguments:
        items -- a list of task items
        """
        try:
            with open(self.file_path, 'a') as file:
                writer = csv.DictWriter(file, fieldnames=Task.FIELDS)
                for item in items:
                    writer.writerow(item)
            return True

        except ValueError:
            print(' Could add items to file.')
            return False

    def create_file(self):
        """Creates a new CSV file on the local drive."""
        try:
            with open(self.file_path, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=Task.FIELDS)
                writer.writeheader()
                if self.entries:
                    for entry in self.entries:
                        writer.writerow(entry)
            return True
        except ValueError:
            print(' Error: Could not create file.')
            return False

    def open_file(self):
        """Attempts to open an existing CSV file,
        If file does not exist, calls create_file method.
        """
        entries = []
        try:
            with open(self.file_path, newline='') as file:
                logreader = csv.DictReader(file)
                for entry in logreader:
                    task = Task(**entry)
                    entries.append(task)
        except FileNotFoundError:
            print(' Could not find existing log file, creating new log.')
            self.create_file()

        finally:
            return entries

    def all_tasks(self):
        """Returns a list of all tasks"""
        return self.tasks

    @staticmethod
    def get_file_path():
        """Returns settings.py FILE_PATH, if exists."""
        if hasattr(settings, 'FILE_PATH'):
            return settings.FILE_PATH
        else:
            return False

    def __init__(self):
        self.file_path = self.get_file_path()
        self.tasks = self.open_file()
