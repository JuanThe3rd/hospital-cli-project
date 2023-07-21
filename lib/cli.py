#!/usr/bin/env python3

from helpers import admin_page, doctor_page, patient_page, log_in
import sys

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
            log_in_data = log_in('admin')
            if log_in_data[0]:
                admin_page(log_in_data[1])
            else:
                print('\n    Either username or password is incorrect, Please try again.')
        elif role == '2':
            log_in_data = log_in('doctor')
            if log_in_data[0]:
                doctor_page(log_in_data[1])
            else:
                print('\n    Either username or password is incorrect, Please try again.')
        elif role == '3':
            patient_page()
        elif role == '4':
            sys.exit('\n    Quitting Program...\n')
        else:
            print('\n    ENTRY INVALID! Must be a number 1 - 4')