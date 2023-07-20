from classes import Patient, Doctor, Appointment
import sqlite3

CONN = sqlite3.connect('lib/db/login.db')
CURSOR = CONN.cursor()

def log_in(role):
    if role == 0:
        sql = '''
            SELECT * FROM logins WHERE type = 'admin';
        '''
    else:
        sql = '''
            SELECT * FROM logins WHERE type = 'doctor';
        '''

    logins = CURSOR.execute(sql).fetchall()

    print('''\n    ------ Login ------\n''')
    username = input('    Username: ')
    password = input('    Password: ')
    
    flag = False
    for login in logins:
        if login[1] == username and login[2] == password:
            flag = True

    return flag

def admin_page():
    if log_in(0):
        pass
    else:
        print('\n    Either username or password is incorrect, Please try again.')

def doctor_page():
    if log_in(1):
        pass
    else:
        print('\n    Either username or password is incorrect, Please try again.')

def patient_page():
    print('\n    In Progress...')

