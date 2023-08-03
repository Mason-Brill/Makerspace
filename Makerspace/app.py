########################################################################
# NOTES
# [1] Add your database password: database.py line 22
# [2] Edit the url of the discord webhook that you'd like to send your emergency text: app.py approximately line 33
#
# TIPS
# [1] the name of each worker calendar needs to be exactly the same as the work's 'first_name last_name' from the database
#
# REFERENCES
# [1] https://www.w3schools.com/python/python_mysql_getstarted.asp
# [2] https://www.udemy.com/course/the-ultimate-mysql-bootcamp-go-from-sql-beginner-to-expert/
# [3] https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/
# [4] https://stackoverflow.com/questions/48344632/passing-a-long-list-of-variables-to-render-template-flask
# [5] http://www.mindrot.org/projects/py-bcrypt/
########################################################################
from flask import Flask, render_template, session, request, make_response, redirect, url_for
from datetime import datetime
from google.auth.exceptions import RefreshError
import bcrypt
import database
import getSchedules
import getWeek
import verifyUsers
import discord_text
import equipment
import employee_login

# discord channel webhook url
emergencyTextURL = 'https://discord.com/api/webhooks/1102005034067173487/upAZ8En1k0z2KVQOYt_fD1IX05gz2H9vCACnxXNIwuRxLY-NccI2l9_EQ1tXSrmRzJfX'

app = Flask(__name__)
app.secret_key = '\x93E\xa9\x12\xc4\xa98\xf2\xbdcj\x12\xc7\xfc\xc1\xf8\x9c\xe7\x01\x85\xee\xd8Ug'

# connect to database
mydb, my_cursor = database.connect_to_database()


# determine if user is logged in
def is_logged_in():
    if 'logged_in' in session:
        return True
    return False


# homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    ############ get equipment from database and create html ###########
    equipment_parameters = equipment.create_parameters()

    ################### worker sign in/out makerspace ###################
    if request.method == 'POST':
        if ((session['privilege_level'] == 'worker' or session['privilege_level'] == 'administrator')
                and 'submit_worker' in request.form):

            # TODO: make the user log back in if they've been inactive for a while?
            ######## log worker into or out of makerspace shift #######
            is_working = employee_login.toggle_shift_status(session['user_id'])

            # this redirect prevents the form from submitting the worker checkin button when the page refreshes
            return redirect(url_for('index', is_logged_in=is_logged_in(), is_checked_in=is_working,
                                    worker_count=employee_login.worker_count(), worker_availability=employee_login.worker_availability()))

    #### determine whether user is currently working in makerspace ####
    if 'user_id' in session:
        user_id = session['user_id']
    else:
        user_id = None
    is_working = employee_login.is_working(user_id)

    return render_template('index.html', is_checked_in=is_working, worker_count=employee_login.worker_count(),
                           worker_availability=employee_login.worker_availability(), is_logged_in=is_logged_in(),
                           **equipment_parameters)


# scheduling page
@app.route('/schedule')
def schedule():
    #################### get makerspace schedule ######################
    try:
        # search database for workers
        my_cursor.execute("SELECT first_name, last_name FROM accounts WHERE privilege_level= %s", ('worker',))
        worker_names = my_cursor.fetchall()
        workers = []
        for worker in worker_names:
            workers.append(worker[0] + ' ' + worker[1])
        this_week = getWeek.getCurrentWeek()
        formatted_week = getWeek.formatDates(this_week, "%d %B %Y")
        weekly_schedule = getSchedules.createSchedule(workers, time_frame="this_week")
        worker_schedule = getSchedules.html_format(weekly_schedule)
        return render_template('schedule.html', this_week=formatted_week[0], hours_of_operation=worker_schedule,
                               is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                               worker_availability=employee_login.worker_availability())
    # the token currently needs to be refreshed weekly
    except RefreshError:
        return render_template('schedule.html', error_message='new token required', is_logged_in=is_logged_in(),
                               worker_count=employee_login.worker_count(), worker_availability=employee_login.worker_availability())


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    ###################### login to makerspace #########################
    if 'logged_in' in session:
        return render_template('logout.html')
    else:
        if request.method == 'POST':
            # get user login information
            email = request.form['email']
            password = request.form['password'].encode('utf-8')

            # search database for user's password
            my_cursor.execute("SELECT passwords.password FROM passwords JOIN accounts ON "
                              "passwords.user_id = accounts.user_id WHERE accounts.email = %s", (email,))
            hashed_password = my_cursor.fetchone()

            # verify email and password match
            if hashed_password and bcrypt.hashpw(password, hashed_password[0].encode('utf-8')) == hashed_password[0].encode('utf-8'):
                # get all user information
                my_cursor.execute("SELECT * FROM accounts WHERE email = %s", (email,))
                user_info = my_cursor.fetchone()
                # create user session
                session['logged_in'] = True
                session['user_id'] = user_info[0]
                session['email'] = user_info[1]
                session['first_name'] = user_info[2]
                session['last_name'] = user_info[3]
                session['privilege_level'] = user_info[4]

                # update accounts to reflect last login time
                my_cursor.execute('UPDATE accounts set last_login=%s WHERE user_id=%s', (datetime.now(), user_info[0]))
                mydb.commit()

                # create equipment database and get html as parameters
                equipment_parameters = equipment.create_parameters()

                ####################### determine shift status #####################
                if 'user_id' in session:
                    user_id = session['user_id']
                else:
                    user_id = None
                is_working = employee_login.is_working(user_id)

                # create response needed to create cookie
                response = make_response(render_template('index.html', is_logged_in=is_logged_in(), is_checked_in=is_working,
                                                         worker_count=employee_login.worker_count(),
                                                         worker_availability=employee_login.worker_availability(),
                                                         **equipment_parameters))

                # create a cookie that javascript can see
                response.set_cookie('level', session['privilege_level'])
                return response

            # displays login page with message for failed login attempt
            else:
                return render_template('login.html', msg="invalid email or password", is_logged_in=is_logged_in(),
                                       worker_count=employee_login.worker_count(), worker_availability=employee_login.worker_availability())
        # displays login page
        return render_template('login.html', is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                               worker_availability=employee_login.worker_availability())


# logout of makerspace website
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    ######################### logout of website #######################
    if 'logged_in' in session:
        if request.method == 'POST':
            # clear session
            session.pop('logged_in', False)
            session.pop('user_id', None)
            session.pop('email', None)
            session.pop('first_name', None)
            session.pop('last_name', None)
            session.pop('privilege_level', None)

            # delete cookie that can be seen by javascript
            response = make_response(render_template('login.html', is_logged_in=is_logged_in(),
                                                     worker_count=employee_login.worker_count(),
                                                     worker_availability=employee_login.worker_availability()))
            response.set_cookie('level', value='public')
            return response
        else:
            return render_template('login.html', is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                   worker_availability=employee_login.worker_availability())

    else:
        return render_template('login.html', is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                               worker_availability=employee_login.worker_availability())


# TODO: add a way to update user information - right now if your account exists you will be forced to login
# TODO: add second password line and verify they match
# Register for a makerspace account
@app.route('/register', methods=['GET', 'POST'])
def register():
    ################ register for a makerspace account #################
    if request.method == 'POST':
        # get user information
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # set privilege level to student - MB
        privilege_level = 'student'

        # make sure characters entered in first or last name are english language characters only - MB
        if first_name.isalpha() == False or last_name.isalpha() == False:
            return render_template('register.html', msg="Name fields must contain a-z characters only!",
                                   is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                   worker_availability=employee_login.worker_availability())
        
        # making sure length of first is no more than 20 characters - MB
        if len(first_name) > 20:
            return render_template('register.html', msg="The first name field must be less than 20 characters",
                                   is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                   worker_availability=employee_login.worker_availability())

        # making sure length of last name is no more than 30 characters - MB
        if len(last_name) > 30:
            return render_template('register.html', msg="The last name must be less than 30 characters",
                                   is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                   worker_availability=employee_login.worker_availability())

        # making sure characters entered in password field are English language characters only - MB
        if not password.isalpha():
            return render_template('register.html', msg="Password field must contain a-z characters only!",
                                   is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                   worker_availability=employee_login.worker_availability())
        
        # checking if password is at least 12 characters, but not longer than 60 characters in length - MB
        if len(password) < 12 or len(password) > 60:
            return render_template('register.html', msg="Password must be between 12 and 60 characters in length!",
                                   is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                   worker_availability=employee_login.worker_availability())
        else:
            # encrypt password
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))

        # search database for user email
        my_cursor.execute("SELECT * FROM accounts WHERE email= %s", (email,))
        user_data = my_cursor.fetchone()

        if user_data:
            return render_template('register.html', msg="Account already exists!", is_logged_in=is_logged_in(),
                                   worker_count=employee_login.worker_count(),
                                   worker_availability=employee_login.worker_availability())

        elif all([email, password, first_name, last_name, privilege_level]) and verifyUsers.isStudent(email):
            # add user to accounts table
            my_cursor.execute('INSERT INTO accounts (email, first_name, last_name, privilege_level, created) '
                              'VALUES (%s, %s, %s, %s, %s)', (email, first_name, last_name, privilege_level, datetime.now()))
            mydb.commit()

            # get newly created user id
            my_cursor.execute("SELECT * FROM accounts WHERE email= %s", (email,))
            user_data = my_cursor.fetchone()

            # add password to passwords table
            my_cursor.execute('INSERT INTO passwords (user_id, password, created) '
                              'VALUES (%s, %s, %s)', (user_data[0], password, datetime.now()))
            mydb.commit()
            # return user to login page
            return render_template('login.html', msg="You successfully registered. Please login.", is_logged_in=is_logged_in(),
                                   worker_count=employee_login.worker_count(), worker_availability=employee_login.worker_availability())

        # unsupported email
        elif not verifyUsers.isStudent(email):
            return render_template('register.html', msg="you aren't eligible to register with that email address",
                                   is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                   worker_availability=employee_login.worker_availability())
        # incomplete form
        else:
            return render_template('register.html', msg="please fill out the form", is_logged_in=is_logged_in(),
                                   worker_count=employee_login.worker_count(), worker_availability=employee_login.worker_availability())

    # show registration form
    return render_template('register.html', is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                           worker_availability=employee_login.worker_availability())


# send emergency text message to discord server
@app.route('/emergencyText', methods=['GET', 'POST'])
def emergencyText():
    ######################### send emergency text######################
    if 'logged_in' in session:
        if request.method == 'POST':
            # append users first and last name to message
            message = request.form['message']
            message = message + ' -' + session['first_name'] + ' ' + session['last_name']
            # send message to discord webhook
            discord_text.PagingDiscordServer(emergencyTextURL, message)
            return render_template('emergencyText.html', verification="Your emergency text was sent.",
                                   is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                   worker_availability=employee_login.worker_availability())
        return render_template('emergencyText.html', is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                               worker_availability=employee_login.worker_availability())
    else:
        return render_template('403.html')


# add new equipment to database
@app.route('/addEquipment', methods=['GET', 'POST'])
def addEquipment():
    ##################### add equipment to database ###################
    if 'logged_in' in session and session['privilege_level'] == "administrator":
        if request.method == 'POST':
            # get equipment information
            category = request.form['category']
            subcategory = request.form['subcategory']
            equipment_name = request.form['equipment_name']
            quantity = request.form['quantity']
            description = request.files['txt_file']
            image = request.files['png_file']

            # verify equipment name is less than or equal to 45 characters - MB
            if len(equipment_name) > 45:
                return render_template('addEquipment.html', msg="Equipment name must be no more than 45 characters",
                                       is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                       worker_availability=employee_login.worker_availability())

            # verify characters entered in fields are english language characters or spaces - MB
            if not equipment_name.replace(' ', '').isalpha() and not subcategory.replace(' ', '').isalpha():
                return render_template('addEquipment.html', msg="equipment name must contain a-z characters or spaces only!",
                                       is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                       worker_availability=employee_login.worker_availability())

            # verify quantity is a number - MB
            if not quantity.isnumeric():
                return render_template('addEquipment.html', msg="value entered in quantity field must be numeric",
                                       is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                       worker_availability=employee_login.worker_availability())

            # search database for user equipment name
            my_cursor.execute("SELECT * FROM equipment WHERE equipment_name= %s", (equipment_name,))
            equipment_table = my_cursor.fetchone()

            if equipment_table:
                # return message if the equipment (based on its name is already in the database)
                return render_template('addEquipment.html', msg=f"{equipment_name} already exists",
                                       is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                       worker_availability=employee_login.worker_availability())

            # create database entry of equipment
            elif all([category, subcategory, quantity]) and category != '':
                # save equipment to database

                my_cursor.execute('INSERT INTO equipment (category, subcategory, quantity, created) '
                                  'VALUES (%s, %s, %s, %s)', (category, subcategory, quantity, datetime.now()))
                mydb.commit()

                # get id of this equipment from database
                equipment_id = my_cursor.lastrowid

                # add equipment name to database
                if equipment_name:
                    my_cursor.execute('UPDATE equipment SET equipment_name = %s WHERE equipment_id=%s', (equipment_name, equipment_id))
                    mydb.commit()

                # add description file name to database and save file
                if description:
                    description_filename = "description_" + str(equipment_id)
                    my_cursor.execute('UPDATE equipment SET description_file_name = %s WHERE equipment_id=%s', (description_filename, equipment_id))
                    mydb.commit()
                    description_filename = description_filename + ".txt"
                    description.save('static/equipment_descriptions/' + description_filename)

                # add image file name to database and save file
                if image:
                    image_filename = "image_" + str(equipment_id)
                    my_cursor.execute('UPDATE equipment SET image_file_name = %s WHERE equipment_id=%s', (image_filename, equipment_id))
                    mydb.commit()
                    image_filename = image_filename + ".png"
                    image.save('static/images/' + image_filename)

                return render_template('addEquipment.html', msg=f'You successfully added a new {subcategory}!',
                                       is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                                       worker_availability=employee_login.worker_availability())

            else:
                return render_template('addEquipment.html', msg="please fill out the form", is_logged_in=is_logged_in(),
                                       worker_count=employee_login.worker_count(), worker_availability=employee_login.worker_availability())

        return render_template('addEquipment.html', is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                               worker_availability=employee_login.worker_availability())
    else:
        return render_template('403.html')


# edit equipment in database
@app.route('/editEquipment', methods=['GET', 'POST'])
def editEquipment():
    # TODO: Edit Equipment
    if 'logged_in' in session and session['privilege_level'] == "administrator":
        if request.method == 'POST':
            pass
        return render_template('editEquipment.html', is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                               worker_availability=employee_login.worker_availability())
    else:
        return render_template('403.html')


# make a reservation to use makerspace equipment
@app.route('/reservation')
def reservation():
    ############## show google form all logged in users ################
    if 'logged_in' in session:
        return render_template('reservation.html', is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                               worker_availability=employee_login.worker_availability())
    else:
        return render_template('403.html')


# make a reservation to use makerspace equipment
@app.route('/bugs')
def bug_reporting():
    ############## show bug reporting to all users ################
    return render_template('bugs.html', is_logged_in=is_logged_in(), worker_count=employee_login.worker_count(),
                           worker_availability=employee_login.worker_availability())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
