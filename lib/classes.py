import sqlite3
'''
from db import appointments
'''

CONN = sqlite3.connect('appointments.db')
CURSOR = CONN.cursor()

class Patient():
    def __init__(self, firstname, lastname, dob, doctor):
        self.firstname = firstname
        self.lastname = lastname
        self.dob = dob
        self.doctor = doctor

class Doctor():
    all = []

    def __init__(self, lastname, patients):
        self.lastname = lastname
        self.patients = patients


class Appointment():
    all = []

    def __init__(self, doctor, patient, time):
        self.doctor = doctor
        self.patient = patient
        self.time = time

def start():
    pass