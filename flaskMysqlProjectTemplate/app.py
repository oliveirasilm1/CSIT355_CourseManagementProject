import sqlparse
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from MySQLConfig import MySQLConfig
import re

app = Flask(__name__)

app.secret_key = 'CSIT355MOEGMH'
# Testing GitFile Update
# Configure MySQL using the imported config
app.config['MYSQL_HOST'] = MySQLConfig.HOST
app.config['MYSQL_USER'] = MySQLConfig.USER
app.config['MYSQL_PASSWORD'] = MySQLConfig.PASSWORD
app.config['MYSQL_DB'] = MySQLConfig.DATABASE

# Create a MySQL connection
mysql = MySQL(app)

def execute_initial_sql(mysql):
    try:
        cursor = mysql.connection.cursor()
        # Read and execute the initial.sql file
        with open('static/sql/init.sql') as sql_file:
            statements = sqlparse.split(sql_file.read())
            for query in statements:
                print(query)
                cursor.execute(query)
                mysql.connection.commit()

        cursor.close()
    except Exception as e:
        print(f"Error executing initial SQL script: {str(e)}")

# you can comment out the following two lines if using docker compose
with app.app_context():
    execute_initial_sql(mysql)


# @app.before_first_request
# def before_first_request():
#     # run this line if database initialization is needed
#     execute_initial_sql()
#     pass

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Students WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return the result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0] # Access corresponding member in tuple
            session['username'] = account[1]
            # Redirect to home page
            return redirect(url_for('userpage'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Students WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        # Check for valid email and username
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO Students VALUES (NULL, %s, %s, %s, 0, %s, %s, 5, 4)', (username, password, email, 'Test', 'Test'))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/userpage')
def userpage():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Courses")
        data = cursor.fetchall()
        cursor.close()
        #    return render_template('index.html', data=data)
        return render_template('home.html', username=session['username'], data=data)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for logged in users
@app.route('/profile')
def profile():
    # Check if the user is logged in
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Students WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not logged in redirect to login page
    return redirect(url_for('login'))

@app.route('/userpage/enroll')
def enroll():
    return redirect(url_for('profile'))

@app.route('/userpage/withdraw')
def withdraw():
    return redirect(url_for('profile'))

# ORIGINAL INDEX PAGE!!!!
#@app.route('/')
#def index():

    # Display a list of records from the database
#    cursor = mysql.connection.cursor()
#    cursor.execute("SELECT * FROM student")
#    data = cursor.fetchall()
#    cursor.close()
#    return render_template('index.html', data=data)

# Route for adding students
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        # Option 1
        # cursor.execute("INSERT INTO student (sname, age, email) VALUES (%s, %s, %s)",(name, age, email))
        # Option 2
        cursor.execute("INSERT INTO student (sname, age, email) VALUES ('{}', '{}', '{}')".format(name, age, email))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))



# Route for deleting students
@app.route('/delete/<int:id>')
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM student WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE student SET sname = %s, age=%s, email = %s WHERE id = %s", (name, age, email, id))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))
    else:
        print(id)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM student WHERE id = %s", (id,))
        result = cursor.fetchone()
        print(result)
        for row in result:
            print(row)
            # data = [row['id'], row['sname'], row['email']]
        data = result
        cursor.close()
        return render_template('update.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=9999)

