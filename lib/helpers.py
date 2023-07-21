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
    print('''
    ------ Admin Page ------

    1 - Add Doctor
    2 - Remove Doctor
    3 - Quit Program
        ''')
    action = input('    Choose Action: ')
    
    if action == '1':
        admin_action('1')
    elif action == '2':
        admin_action('2')
    elif action == '3':
        sys.exit('\n    Quitting Program...\n')
    else:
        print('\nInvaid Entry, Sending back to Home Page...')

def admin_action(action):
    lastname = input('\n    Enter Doctor\'s last name: ')

    if action == '1':
        sql = f'INSERT INTO doctors (lastname) VALUES (?);'
    else:
        sql = f'DELETE FROM doctors WHERE lastname = ?;'

    CURSORD.execute(sql, (lastname,))
    CONND.commit()

    if action == '1':
        print(f'\n    Dr. {lastname} has been added to the database!')
    else:
        print(f'\n    Dr. {lastname} has been deleted from the database!')

    continuation = input('\nDo you wish to do something else as an admin? (Enter \'Y\' for yes and anything else for no): ')
    if (continuation == 'Y'):
        admin_page()

def admin_action_2():
    lastname = input('\n    Enter Doctor\'s last name: ')

    sql = f'DELETE FROM doctors WHERE lastname = ?;'
    CURSORD.execute(sql, (lastname,))

def doctor_page():
    if log_in(1):
        pass
    else: 
        print('\n    Either username or password is incorrect, Please try again.')

def patient_page():
    print('\n    In Progress...')

