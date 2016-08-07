from datetime import datetime
import settings


class Task:
    FIELDS = ['name', 'mins', 'notes', 'date']

    def prompt_date(self):
        while True:
            print(' Date format is: mm/dd/yyyy')
            date = input(' Task Date: ')
            if self.valid_date(date):
                return date

    def prompt_mins(self):
        while True:
            mins = input(' Time spent on task, in minutes: ')
            if self.valid_mins(mins):
                return mins

    def prompt_name(self):
        while True:
            name = input('Task Name: ')
            if self.valid_name(name):
                return name
            else:
                print(' ** Task Name cannot be empty. ** ')

    @staticmethod
    def valid_date(date):
        try:
            datetime.strptime(date, '%m/%d/%Y')
        except ValueError:
            print(' ** Incorrect date format, should be MM/DD/YYYY **')
            return False
        return True

    @staticmethod
    def valid_mins(mins):
        try:
            val = int(mins)
        except ValueError:
            print('Sorry, it needs to be a number.')
            return False
        return True

    @staticmethod
    def valid_name(name):
        return True if name else False

    @staticmethod
    def prompt_notes():
        return input('Additional Notes: ')

    def __init__(self, **kwargs):
        self.name = self.prompt_name()
        self.mins = self.prompt_mins()
        self.notes = self.prompt_notes()
        self.date = self.prompt_date()
