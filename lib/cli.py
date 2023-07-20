#!/usr/bin/env python3

import helpers
from db import classes

if __name__ == '__main__':
    
    while True:
        print('\n    ------- Home -------')
        role = input(f'''    
    1 - Admin
    2 - Doctor
    3 - Patient
    4 - Quit Program

    Choose User: ''')

        if role == '1':
            helpers.admin_page()
        elif role == '2':
            helpers.doctor_page()
        elif role == '3':
            helpers.patient_page()
        elif role == '4':
            break
        else:
            print('\n    ENTRY INVALID! Must be a number 1 - 4')