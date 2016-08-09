import csv
import settings
from task import Task


class Log:
    """A Log is the representation of a file.

    An instance of log holds all the methods necessary
    to interact with a CSV file. This means adding new
    items, editing items, and deleting items.
    """
    def rewrite_the_log(self, items=[]):
        try:
            with open(self.file_path, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=self.fields)
                writer.writeheader()
                for item in items:
                    row = {
                        'name': item.name,
                        'mins': item.mins,
                        'notes': item.notes,
                        'date': item.date
                    }
                    writer.writerow(row)
            return True
        except ValueError:
            print(' Could not rewrite the log file.')
            return False

    def write_to_log(self, items=[]):
        """Appends to file, list of items.

        Keyword arguments:
        items -- a list of task items
        """
        try:
            with open(self.file_path, 'a') as file:
                writer = csv.DictWriter(file, fieldnames=self.fields)
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
                writer = csv.DictWriter(file, fieldnames=self.fields)
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

    @staticmethod
    def get_file_path():
        """Returns settings.py FILE_PATH, if exists."""
        if hasattr(settings, 'FILE_PATH'):
            return settings.FILE_PATH
        else:
            return False

    def __init__(self, fields=[]):
        self.fields = fields
        self.file_path = self.get_file_path()
