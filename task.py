from datetime import datetime


class Task:
    FIELDS = ['name', 'mins', 'notes', 'date']

    def prompt_notes(self):
        """Prompts user for a task's notes."""
        return input(' Additional Notes: ')

    def prompt_date(self):
        """Prompts user for a date in a predefined format."""
        while True:
            print(' Date format is: mm/dd/yyyy')
            date = input(' Task Date: ')
            if self.valid_date(date):
                return date

    def prompt_mins(self):
        """Prompts user then validates input for task time."""
        while True:
            mins = input(' Time spent on task, in minutes: ')
            if self.valid_num(mins):
                return mins

    def prompt_name(self):
        """Prompts user then validates input for task name."""
        while True:
            name = input(' Task Name: ')
            if self.valid_name(name):
                return name
            else:
                print(' ** Task Name cannot be empty. ** ')

    def task_date(self):
        """Returns a task's date."""
        return self.date

    def task_notes(self):
        """Returns a task's notes."""
        return self.notes

    def task_name(self):
        """Returns a task's name."""
        return self.name

    def minutes(self):
        """Returns a task's minutes."""
        return self.mins

    def set_notes(self):
        """Sets a task's notes,
        by re-prompting user.
        """
        new_notes = input(' Task Notes[{}]: '.format(self.notes)) or self.notes
        self.notes = new_notes

    def set_date(self):
        """Sets a task's date,
        by re-prompting user.
        """
        new_date = input(' Task Date[{}]: '.format(self.date)) or self.date
        self.date = new_date

    def set_mins(self):
        """Sets a task's minutes,
        by re-prompting user.
        """
        new_mins = input(' Time spent[{}]: '.format(self.mins)) or self.mins
        self.mins = new_mins

    def set_name(self):
        """Sets a task's name,
        by re-prompting user.
        """
        new_name = input(' Task Name[{}]: '.format(self.name)) or self.name
        self.name = new_name

    def update_all(self):
        """Calls all task set methods,
        to prompt user for task updates.
        """
        self.set_name()
        self.set_mins()
        self.set_notes()
        self.set_date()

    @staticmethod
    def valid_date(date):
        """Returns True if date is actually a date,
        based-on a pre-defined date format.
        """
        try:
            datetime.strptime(date, '%m/%d/%Y')
        except ValueError:
            print(' ** Incorrect date format, should be MM/DD/YYYY **')
            return False
        return True

    @staticmethod
    def valid_num(num):
        """Returns True if the input was in-fact an integer."""
        try:
            val = int(num)
        except ValueError:
            print(' Sorry, it needs to be a number.')
            return False
        return True

    @staticmethod
    def valid_name(name):
        """Returns True if non-empty string was given."""
        return True if name else False

    def __init__(self, **kwargs):
        self.name = (self.prompt_name()
                     if 'name' not in kwargs else kwargs['name'])
        self.mins = (self.prompt_mins()
                     if 'mins' not in kwargs else int(kwargs['mins']))
        self.notes = (self.prompt_notes()
                      if 'notes' not in kwargs else kwargs['notes'])
        self.date = (self.prompt_date()
                     if 'date' not in kwargs else kwargs['date'])
