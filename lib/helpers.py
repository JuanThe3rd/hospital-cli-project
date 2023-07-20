from classes import Patient, Doctor, Appointment
import sqlite3
import sys

CONNL = sqlite3.connect('lib/db/login.db')
CURSORL = CONNL.cursor()

CONND = sqlite3.connect('lib/db/doctors.db')
CURSORD = CONND.cursor()

def log_in(role):
    if role == 0:
        sql = '''
            SELECT * FROM logins WHERE type = 'admin';
        '''
    else:
        sql = '''
            SELECT * FROM logins WHERE type = 'doctor';
        '''

    logins = CURSORL.execute(sql).fetchall()

    print('''\n    ------ Login ------\n''')
    username = input('    Username: ')
    password = input('    Password: ')
    
    flag = True
    for login in logins:
        if login[1] == username and login[2] == password:
            flag = True

    return flag

def admin_page():
    if log_in(0):
        print('''
    ------ Admin Page ------

    1 - Add Doctor
    2 - Remove Doctor
    3 - Quit Program
        ''')
        action = input('    Choose Action: ')
        
        if action == '1':
            admin_action_1()
        elif action == '2':
            admin_action_2()
        elif action == '3':
            sys.exit('\n    Quitting Program...\n')
        else:
            print('\nInvaid Entry, Sending back to Home Page...')
    else:
        print('\n    Either username or password is incorrect, Please try again.')

def admin_action_1():
    lastname = input('\n    Enter Doctor\'s last name: ')

    sql = f'INSERT INTO doctors (lastname) VALUES (\'{lastname}\');'
    CURSORD.execute(sql)

    print(f'\n    Dr. {lastname} has been added to the database!')

    continuation = input('\nDo you wish to do something else as an admin? (Y/N): ')
    flag = True
    while flag:
        if (continuation != 'Y' or continuation != 'N'):
            print('\n    Invalid input, please enter \'Y\' or \'N\'')
            continuation = input('\nDo you wish to do something else as an admin? (Y/N): ')
        else:
            flag = False
            if continuation == 'Y':
                admin_page()


def admin_action_2():
    pass

def doctor_page():
    if log_in(1):
        pass
    else: 
        print('\n    Either username or password is incorrect, Please try again.')

def patient_page():
    print('\n    In Progress...')

