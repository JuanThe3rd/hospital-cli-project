
def log_in(role):
    print('''\n    ------ Login ------\n''')
    username = input('    Username: ')
    password = input('    Password: ')
    print(f'\n    {username}, {password}')

def admin_page():
    log_in(0)

def doctor_page():
    log_in(1)

def patient_page():
    print('\n    In Progress...')
