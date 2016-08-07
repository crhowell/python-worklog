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
            name = input(' Task Name: ')
            if self.valid_name(name):
                return name
            else:
                print(' ** Task Name cannot be empty. ** ')

    def task_date(self):
        return self.date

    def task_notes(self):
        return self.notes

    def task_name(self):
        return self.name

    def minutes(self):
        return self.mins

    def set_notes(self):
        self.notes = self.prompt_notes()

    def set_date(self):
        new_date = input(' Task Date[{}]: '.format(self.date)) or self.date
        self.date = new_date

    def set_mins(self):
        new_mins = input(' Time spent[{}]: '.format(self.mins)) or self.mins
        self.mins = new_mins

    def set_name(self):
        new_name = input(' Task Name[{}]: '.format(self.name)) or self.name
        self.name = new_name

    def update_all(self):
        self.set_name()
        self.set_mins()
        self.set_notes()
        self.set_date()

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
            print(' Sorry, it needs to be a number.')
            return False
        return True

    @staticmethod
    def valid_name(name):
        return True if name else False

    @staticmethod
    def prompt_notes():
        return input(' Additional Notes: ')

    def __init__(self, **kwargs):
        self.name = (self.prompt_name()
                     if 'name' not in kwargs else kwargs['name'])
        self.mins = (self.prompt_mins()
                     if 'mins' not in kwargs else int(kwargs['mins']))
        self.notes = (self.prompt_notes()
                      if 'notes' not in kwargs else kwargs['notes'])
        self.date = (self.prompt_date()
                     if 'date' not in kwargs else kwargs['date'])
