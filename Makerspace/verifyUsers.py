########################################################################
# verifyUsers
#
# these functions are used to SHA256 hash strings and lines in a CSV file
########################################################################
import hashlib
import csv


# takes csv filename formatted (hashed student id, hashed student email)
# returns list of hashed student emails
def readCSV(filename):
    with open(filename, mode='r') as file:
        csvFile = csv.reader(file)
        student_info = [line for line in csvFile]

    # student_ids = [student[0] for student in student_info]
    student_emails = [student[1] for student in student_info]
    return student_emails


# takes an email
# sha256 hashes the email
# returns true if the hashed email is in the list of student emails
def isStudent(email):
    hashed_email = hashlib.sha256(email.encode()).hexdigest()
    emails = readCSV("CS-majors-minors.csv")
    if hashed_email in emails:
        return True
    return False


# takes a string
# returns sha256 hash of string - MB
def hash256(string):
    h = hashlib.new('sha256')
    h.update(bytes(string, 'utf-8'))
    return h.hexdigest()


if __name__ == '__main__':
    # EXAMPLES
    user_email = "rebecca.wilson@spartans.ut.edu"
    print(f"{user_email} is a student: {isStudent(user_email)}")
    user_email = "rebecca.wilson2@spartans.ut.edu"
    print(f"{user_email} is a student: {isStudent(user_email)}")

