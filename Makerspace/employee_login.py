########################################################################
# employee_login
#
# These functions are related to whether and how many workers are logged
# into their makerspace shifts.
########################################################################
from datetime import datetime
import database

# connect to database
mydb, my_cursor = database.connect_to_database()


# determine whether worker is currently logged in to work in the makerspace
# return the shift_id if the user is working otherwise return false
# NOTE: pass in session['user_id'] from app.py
def is_working(user_id):
    if user_id:
        my_cursor.execute("SELECT employee_hours.shift_id, accounts.first_name, employee_hours.signed_in FROM accounts JOIN "
                          "employee_hours ON accounts.user_id = employee_hours.user_id WHERE "
                          "accounts.user_id = %s AND employee_hours.signed_out IS NULL", (user_id,))
        shift_status = my_cursor.fetchone()
        if shift_status:
            return shift_status[0]      # database shift_id
    return False


# update the signed_out time in worker's shift from employee_hours database table with the current time
def end_shift(user_id):
    shift_id = is_working(user_id)
    my_cursor.execute('UPDATE employee_hours SET signed_out=%s '
                      'WHERE shift_id=%s', (datetime.now(), shift_id))
    mydb.commit()


# create a new entry in the employee_hours database that includes the current time as the sign_in time
def start_shift(user_id):
    my_cursor.execute('INSERT INTO employee_hours (user_id, signed_in) '
                      'VALUES (%s, %s)', (user_id, datetime.now()))
    mydb.commit()


# determines whether a worker is currently working in the makerspace and signs them in or out as appropriate
# returns False if they just ended their shift and returns True if they just started their shift
def toggle_shift_status(user_id):
    is_currently_working = is_working(user_id)
    if is_currently_working:
        end_shift(user_id)
        return False
    else:
        start_shift(user_id)
        return True


# determine and return number of workers currently working in the makerspace
def worker_count():
    my_cursor.execute("SELECT accounts.first_name, employee_hours.signed_in FROM accounts JOIN employee_hours"
                      " ON accounts.user_id = employee_hours.user_id WHERE employee_hours.signed_out IS NULL")
    current_workers = my_cursor.fetchall()
    return len(current_workers)


def worker_availability():
    workers_available = worker_count()
    if workers_available > 0:
        return 'worker_available'
    return 'worker_unavailable'


if __name__ == '__main__':
    print(worker_count())
