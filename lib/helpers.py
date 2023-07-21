import sqlite3
import sys

CONNL = sqlite3.connect('lib/db/login.db')
CURSORL = CONNL.cursor()

CONND = sqlite3.connect('lib/db/doctors.db')
CURSORD = CONND.cursor()

CONNA = sqlite3.connect('lib/db/appointments.db')
CURSORA = CONNA.cursor()

CONNP = sqlite3.connect('lib/db/patients.db')
CURSORP = CONNP.cursor()

def validate_date(date_text):
    if (len(date_text) != 10) or (date_text[2] != '/') or (date_text[5] != '/'):
        return False
    
    for char in date_text:
        if char == '/':
            pass
        elif char.isdigit() == False:
            return False

    return True

def validate_time(time_text):
    if (len(time_text) != 5) or (time_text[2] != ':'):
        return False
    
    for char in time_text:
        if char == ':':
            pass
        elif char.isdigit() == False:
            return False
        
    return True

def validate_doctor(lastname):
    sql = 'SELECT * FROM doctors WHERE lastname = ?;'
    doctor = CURSORD.execute(sql, (lastname,)).fetchone()

    if doctor == None:
        return False
    else:
        return True

def log_in(role):
    if role == 'admin':
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
    
    flag = False
    user = ''
    for login in logins:
        if login[1] == username and login[2] == password:
            flag = True
            user = login[4]

    return [flag, user]

#        <---------- Admin Page ---------->

def admin_page(user):
    print(f'''
    ------ Admin Page ------

    Welcome {user}!

    1 - Add Doctor
    2 - Remove Doctor
    3 - Quit Program
        ''')
    action = input('    Choose Action: ')
    
    if action == '1':
        admin_action('1', user)
    elif action == '2':
        admin_action('2', user)
    elif action == '3':
        sys.exit('\n    Quitting Program...\n')
    else:
        print('\nInvaid Entry, Sending back to Home Page...')

def admin_action(action, user):
    lastname = input('\n    Enter Doctor\'s last name: ').title()

    if action == '2' and validate_doctor(lastname) == False:
        print(f'\n    Dr. {lastname.title()} was not found in our files, Redirecting back to Home Page...')
        return 0

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
        admin_page(user)

#        <---------- Doctor Page ---------->

def doctor_page(user):
    print(f'''
    ------ Doctor Page ------

    Welcome Dr. {user}!

    1 - View Appointments
    2 - Add Appointment
    3 - Remove Appointment
    4 - Quit Program
        ''')
    action = input('    Choose Action: ')

    if action == '1':
        view_appointments(user)
    elif action == '2':
        add_appointment(user)
    elif action == '3':
        remove_appointment(user)
    elif action == '4':
        sys.exit('\n    Quitting Program...\n')
    else:
        print('\nInvaid Entry, Sending back to Home Page...')

def view_appointments(user):
    doctor = CURSORD.execute('SELECT * FROM doctors WHERE lastname = ?;', (user,)).fetchone()
    sql = 'SELECT * FROM appointments WHERE doctor_id = ?;'
    appointments = CURSORA.execute(sql, (doctor[0],)).fetchall()

    print('\n ----------- Appointments -----------')
    print('| Patient         | Date & Time      |')
    print('|-----------------|------------------|')
    for appointment in appointments:
        sql = 'SELECT * FROM patients WHERE id = ?'
        patient = CURSORP.execute(sql, (appointment[1],)).fetchone()
        patient_name = f'{patient[1]} {patient[2][0]}.'

        print(f'| ', end='')
        print(f'{patient_name}', end='')
        for i in range(16 - len(patient_name)):
            print(f' ', end='')
        print(f'| {appointment[2]} {appointment[3]} |')
    print(' ------------------------------------')

    continuation = input('\nDo you wish to do something else as a doctor? (Enter \'Y\' for yes and anything else for no): ')
    if (continuation == 'Y'):
        doctor_page(user)

def add_appointment(user):
    patient_first_name = input('    Enter patient\'s first name: ').title()
    patient_last_name = input('    Enter patient\'s last name: ').title()
    patient_dob = input('    Enter patient\'s dob (format: mm/dd/yyyy): ')

    while True:
        if validate_date(patient_dob) == False:
            print('\nPatient\'s DOB is formatted incorrectly, Please try again')
            patient_dob = input('\n    Enter patient\'s dob (format: mm/dd/yyyy): ')
        else:
            break

    date = input('    Enter date for appointment (format: mm/dd/yyyy): ')

    while True:
        if validate_date(date) == False:
            print('\nAppointment date is formatted incorrectly, Please try again')
            date = input('\n    Enter date for appointment (format: mm/dd/yyyy): ')
        else: 
            break

    time = input('    Enter time for appointment (format: hh:mm): ')

    while True:
        if validate_time(time) == False:
            print('\nAppointment time is formatted incorrectly, Please try again')
            time = input('\n    Enter time for appointment (format: hh:mm): ')
        else:
            break

    sql = 'SELECT * FROM patients WHERE firstname = ? AND lastname = ? AND dob = ?;'
    patient = CURSORP.execute(sql, (patient_first_name, patient_last_name, patient_dob)).fetchone()

    if patient == None:
        sql = 'INSERT INTO patients (firstname, lastname, dob) VALUES (?, ?, ?);'
        CURSORP.execute(sql, (patient_first_name, patient_last_name, patient_dob))
        CONNP.commit()
        patient = CURSORP.execute('SELECT * FROM patients WHERE firstname = ? AND lastname = ?;', (patient_first_name, patient_last_name)).fetchone()

    doctor = CURSORD.execute('SELECT * FROM doctors WHERE lastname = ?;', (user,)).fetchone()
    
    sql = 'INSERT INTO appointments (doctor_id, patient_id, date, time) VALUES (?, ?, ?, ?);'
    CURSORA.execute(sql, (doctor[0], patient[0], date, time))
    CONNA.commit()
    print('\n    Appointment has been successfully added!')

    continuation = input('\nDo you wish to do something else as a doctor? (Enter \'Y\' for yes and anything else for no): ')
    if (continuation == 'Y'):
        doctor_page(user)

def remove_appointment(user):
    patient_first_name = input('    Enter patient\'s first name: ').title()
    patient_last_name = input('    Enter patient\'s last name: ').title()
    patient_dob = input('    Enter patient\'s dob (format: format: mm/dd/yyyy): ')
    
    while True:
        if validate_date(patient_dob) == False:
            print('\nPatient\'s DOB is formatted incorrectly, Please try again')
            patient_dob = input('\n    Enter patient\'s dob (format: mm/dd/yyyy): ')
        else:
            break

    date = input('    Enter date for appointment (format: mm/dd/yyyy): ')

    while True:
        if validate_date(date) == False:
            print('\nAppointment date is formatted incorrectly, Please try again')
            date = input('\n    Enter date for appointment (format: mm/dd/yyyy): ')
        else: 
            break

    time = input('    Enter time for appointment (format: hh:mm): ')

    while True:
        if validate_time(time) == False:
            print('\nAppointment time is formatted incorrectly, Please try again')
            time = input('\n    Enter time for appointment (format: hh:mm): ')
        else:
            break

    sql = 'SELECT * FROM doctors WHERE lastname = ?'
    doctor = CURSORD.execute(sql, (user,)).fetchone()

    sql = 'SELECT * FROM patients WHERE firstname = ? AND lastname = ? AND dob = ?;'
    patient = CURSORP.execute(sql, (patient_first_name, patient_last_name, patient_dob)).fetchone()

    sql = 'SELECT * FROM appointments WHERE doctor_id = ? AND patient_id = ? AND date = ? AND time = ?'
    appointment = CURSORA.execute(sql, (doctor[0], patient[0], date, time))

    if patient == None:
        print('\nThis patient was not found in our files, Redirecting to Home Page...')
    elif appointment == None:
        print('\nThis appointment was not found in our files, Redirecting to Home Page...')
    else:
        sql = 'DELETE FROM appointments WHERE doctor_id = ? AND patient_id = ? AND date = ? AND time = ?'
        CURSORA.execute(sql, (doctor[0], patient[0], date, time))
        CONNA.commit()
        print('\n    Appointment has been successfully canceled!')

    continuation = input('\nDo you wish to do something else as a doctor? (Enter \'Y\' for yes and anything else for no): ')
    if (continuation == 'Y'):
        doctor_page(user)

#        <---------- Patient Page ---------->

def patient_page():
    print('''
    ------ Patient Page ------

    1 - Check For Upcoming Appointments
    2 - Make an Appointment
    3 - Cancel an Appointment
    4 - Quit Program
    ''')

    action = input('    Choose Action: ')
    if action == '1':
        view_patient_appointments()
    elif action == '2':
        add_patient_appointment()
    elif action == '3':
        remove_patient_appointment()
    elif action == '4':
        sys.exit('\n    Quitting Program...\n')
    else:
        print('\nInvaid Entry, Sending back to Home Page...')

def view_patient_appointments():
    dr_last_name = input('\n    Enter Dr\'s last name: ').title()

    if validate_doctor(dr_last_name.title()) == False:
        print(f'\n    Dr. {dr_last_name.title()} was not found in our files, Redirecting you to Home Page...')
        return 0

    patient_first_name = input('    Enter patient\'s first name: ').title()
    patient_last_name = input('    Enter patient\'s last name: ').title()
    patient_dob = input('    Enter patient\'s dob (format: mm/dd/yyyy): ')

    while True:
        if validate_date(patient_dob) == False:
            print('\nPatient\'s DOB is formatted incorrectly, Please try again')
            patient_dob = input('\n    Enter patient\'s dob (format: mm/dd/yyyy): ')
        else:
            break

    sql = 'SELECT * FROM doctors WHERE lastname = ?'
    doctor = CURSORD.execute(sql, (dr_last_name,)).fetchone()

    sql = 'SELECT * FROM patients WHERE firstname = ? AND lastname = ? AND dob = ?'
    patient = CURSORP.execute(sql, (patient_first_name, patient_last_name, patient_dob)).fetchone()

    if patient == None:
        print(f'\n{patient_first_name} {patient_last_name} was not found in our files, Redirecting back to Home Page...')
        return 0

    sql = 'SELECT * FROM appointments WHERE doctor_id = ? AND patient_id = ?'
    appointments = CURSORA.execute(sql, (doctor[0], patient[0])).fetchall()

    print('\n ---------- Appointments ----------')
    print('| Date            | Time           |')
    print('|-----------------|----------------|')
    for appointment in appointments:
        print(f'| {appointment[2]}      | {appointment[3]}          |')
    print(' ----------------------------------')

    continuation = input('\nDo you wish to do something else as a patient? (Enter \'Y\' for yes and anything else for no): ')
    if (continuation == 'Y'):
        patient_page()

def add_patient_appointment():
    dr_last_name = input('\n    Enter Dr\'s last name: ').title()

    if validate_doctor(dr_last_name.title()) == False:
        print(f'\n    Dr. {dr_last_name.title()} was not found in our files, Redirecting you to Home Page...')
        return 0

    patient_first_name = input('    Enter patient\'s first name: ').title()
    patient_last_name = input('    Enter patient\'s last name: ').title()
    patient_dob = input('    Enter patient\'s dob (format: mm/dd/yyyy): ')
    
    while True:
        if validate_date(patient_dob) == False:
            print('\nPatient\'s DOB is formatted incorrectly, Please try again')
            patient_dob = input('\n    Enter patient\'s dob (format: mm/dd/yyyy): ')
        else:
            break

    date = input('    Enter date for appointment (format: mm/dd/yyyy): ')

    while True:
        if validate_date(date) == False:
            print('\nAppointment date is formatted incorrectly, Please try again')
            date = input('\n    Enter date for appointment (format: mm/dd/yyyy): ')
        else: 
            break

    time = input('    Enter time for appointment (format: hh:mm): ')

    while True:
        if validate_time(time) == False:
            print('\nAppointment time is formatted incorrectly, Please try again')
            time = input('\n    Enter time for appointment (format: hh:mm): ')
        else:
            break

    sql = 'SELECT * FROM doctors WHERE lastname = ?'
    doctor = CURSORD.execute(sql, (dr_last_name,)).fetchone()

    sql = 'SELECT * FROM patients WHERE firstname = ? AND lastname = ? AND dob = ?'
    patient = CURSORP.execute(sql, (patient_first_name, patient_last_name, patient_dob)).fetchone()

    if patient == None:
        sql = 'INSERT INTO patients (firstname, lastname, dob) VALUES (?, ?, ?)'
        CURSORP.execute(sql, (patient_first_name, patient_last_name, patient_dob))
        CONNP.commit()

        sql = 'SELECT * FROM patients WHERE firstname = ? AND lastname = ? AND dob = ?'
        patient = CURSORP.execute(sql, (patient_first_name, patient_last_name, patient_dob)).fetchone()

    sql = 'INSERT INTO appointments (doctor_id, patient_id, date, time) VALUES (?, ?, ?, ?)'
    CURSORA.execute(sql, (doctor[0], patient[0], date, time))
    CONNA.commit()

    print('\n    Appointment has been successfully added!')

    continuation = input('\nDo you wish to do something else as a patient? (Enter \'Y\' for yes and anything else for no): ')
    if (continuation == 'Y'):
        patient_page()

def remove_patient_appointment():
    dr_last_name = input('\n    Enter Dr\'s last name: ').title()

    if validate_doctor(dr_last_name.title()) == False:
        print(f'\n    Dr. {dr_last_name.title()} was not found in our files, Redirecting you to Home Page...')
        return 0

    patient_first_name = input('    Enter patient\'s first name: ').title()
    patient_last_name = input('    Enter patient\'s last name: ').title()
    patient_dob = input('    Enter patient\'s dob (format: mm/dd/yy): ')
    
    while True:
        if validate_date(patient_dob) == False:
            print('\nPatient\'s DOB is formatted incorrectly, Please try again')
            patient_dob = input('\n    Enter patient\'s dob (format: mm/dd/yyyy): ')
        else:
            break

    date = input('    Enter date for appointment (format: mm/dd/yyyy): ')

    while True:
        if validate_date(date) == False:
            print('\nAppointment date is formatted incorrectly, Please try again')
            date = input('\n    Enter date for appointment (format: mm/dd/yyyy): ')
        else: 
            break

    time = input('    Enter time for appointment (format: hh:mm): ')

    while True:
        if validate_time(time) == False:
            print('\nAppointment time is formatted incorrectly, Please try again')
            time = input('\n    Enter time for appointment (format: hh:mm): ')
        else:
            break

    sql = 'SELECT * FROM doctors WHERE lastname = ?'
    doctor = CURSORD.execute(sql, (dr_last_name,)).fetchone()

    sql = 'SELECT * FROM patients WHERE firstname = ? AND lastname = ? AND dob = ?'
    patient = CURSORP.execute(sql, (patient_first_name, patient_last_name, patient_dob)).fetchone()

    if doctor == None:
        print('\nThis doctor was not found in our files, Redirecting to Home Page...')
    elif patient == None:
        print('\nThis patient was not found in our files, Redirecting to Home Page...')
    else:
        sql = 'DELETE FROM appointments WHERE doctor_id = ? AND patient_id = ? AND date = ? AND time = ?'
        CURSORA.execute(sql, (doctor[0], patient[0], date, time))
        CONNA.commit()
        print('\n    This appointment has been successfully canceled !')

    continuation = input('\nDo you wish to do something else as a patient? (Enter \'Y\' for yes and anything else for no): ')
    if (continuation == 'Y'):
        patient_page()
