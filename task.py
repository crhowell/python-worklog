from datetime import datetime
import settings


class Task:

    def prompt_date(self):
        print('Date format is: mm/dd/yyyy')
        return input('Task Date: ')

    def prompt_notes(self):
        return input('Additional Notes: ')

    def prompt_mins(self):
        while True:
            try:
                prompt = int(input('Time spent on task, in minutes: '))
            except ValueError:
                print('Sorry, it needs to be a number.')
                continue
            else:
                return prompt

    def prompt_name(self):
        return input('Task Name: ')

    def __init__(self, **kwargs):
        self.name = self.prompt_name()
        self.mins = self.prompt_mins()
        self.notes = self.prompt_notes()
        self.date = self.prompt_date()
