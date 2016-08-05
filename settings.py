"""WorkLog Application Settings

Contains the following:
Date Formatting
Company Name
Base Directory (Generated)
WorkLog File Location (Generated)

Filenames:
Worklog filenames are generated based-on company name.
They contain the company name, appended with '_worklog.csv'

File Paths:
All worklogs, by default,
are stored in the root app directory, inside the 'logs' folder
"""

import os

# Date Format
DATE_FORMAT = '%m-%d-%Y'

# Enter your Company's name
COMPANY_NAME = 'Some Company'

# File Location Settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
FILENAME = COMPANY_NAME.lower().replace(' ', '_') + '_worklog.csv'
FILE_PATH = os.path.join(LOG_DIR, FILENAME)
