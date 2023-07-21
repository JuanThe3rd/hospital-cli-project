
class Patient():
    def __init__(self, firstname, lastname, dob):
        self.firstname = firstname
        self.lastname = lastname
        self.dob = dob

class Doctor():
    all = []

    def __init__(self, lastname):
        self.lastname = lastname

class Appointment():
    all = []

    def __init__(self, doctor, patient, date, time):
        self.doctor = doctor
        self.patient = patient
        self.date = date
        self.time = time
