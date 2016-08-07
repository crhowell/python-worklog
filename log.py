import csv
from datetime import datetime
import settings
from task import Task


class Log:

    def find_by_date(self, idx):
        i = idx - 1
        return [self.tasks[i]]

    def search_by_term(self, term=''):
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
        return self.tasks

    @staticmethod
    def get_file_path():
        if hasattr(settings, 'FILE_PATH'):
            return settings.FILE_PATH
        else:
            return False

    def __init__(self):
        self.file_path = self.get_file_path()
        self.tasks = self.open_file()
