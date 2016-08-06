import csv
from datetime import datetime
import settings


class Log:
    FIELDNAMES = ['name', 'mins', 'notes', 'date']

    def write_to_log(self, items=[]):
        try:
            with open(self.file_path, 'a') as file:
                writer = csv.DictWriter(file, fieldnames=Log.FIELDNAMES)
                for item in items:
                    writer.writerow(item)
            return True

        except ValueError:
            print('Could add items to file.')
            return False

    def create_file(self):
        try:
            with open(self.file_path, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=Log.FIELDNAMES)
                writer.writeheader()
            return True
        except ValueError:
            print("Error: Could not create file.")
            return False

    def open_file(self):
        try:
            with open(self.file_path, newline='') as file:
                logreader = csv.DictReader(file)
                for row in logreader:
                    print(row)
        except FileNotFoundError:
            print('Could not find existing log file, creating new log.')
            self.create_file()

    @staticmethod
    def get_file_path():
        if hasattr(settings, 'FILE_PATH'):
            return settings.FILE_PATH
        else:
            return False

    def __init__(self):
        self.file_path = self.get_file_path()
