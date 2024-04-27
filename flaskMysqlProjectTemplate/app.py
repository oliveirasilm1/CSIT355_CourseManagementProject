import sqlparse, re
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from MySQLConfig import MySQLConfig

app = Flask(__name__)
app.secret_key = 'CSIT355MOEGMH'

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

# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:  # Input submitted
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
            session['id'] = account[0]  # Access corresponding member
            session['username'] = account[1]
            # Redirect to home page
            return redirect(url_for('userpage'))
        else:
            # Account doesn't exist or username/password incorrect
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
            cursor.execute('INSERT INTO Students VALUES (NULL, %s, %s, %s, 0, %s, 5, 4)',
                           (username, password, email, 'Test'))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/profile')
def profile():
    # Check if the user is logged in
    if 'loggedin' in session:
        # We need all the account info for the user so that we can display it on the profile page
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Students WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not logged in redirect to login page
    return redirect(url_for('login'))


@app.route('/userpage')
def userpage():
    # Check if the user is logged in
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        # Show Available Courses
        cursor.execute("SELECT * FROM Students WHERE id = %s", (session['id'],))
        data = cursor.fetchone()
        if data[4] == 0:  # Not Admin
            cursor.execute(
                "SELECT * FROM Courses C where not exists (SELECT * FROM Enrolled E where E.id = %s and C.cid = E.cid)",
                (session['id'],))
            data = cursor.fetchall()
            cursor.close()
            return render_template('available.html', username=session['username'], data=data)
        else:
            cursor.execute("SELECT * FROM Students")
            data = cursor.fetchall()
            cursor.close()
            return render_template('admin.html', username=session['username'], data=data)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/userpage/enrolled')
def enrolled():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Courses C, Enrolled E WHERE E.id = %s and C.cid = E.cid", (session['id'],))
        data = cursor.fetchall()
        gpa = calculate_gpa(session['id'])
        cursor.close()
        #    return render_template('index.html', data=data)
        return render_template('enrolled.html', username=session['username'], data=data, gpa=gpa)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/admin/selectenrolled', methods=['GET', 'POST'])
def adminenrolled():
    # Check if the user is logged in
    if 'loggedin' in session:
        if request.method == 'POST':
            name = request.form['name']
            age = request.form['age']
            email = request.form['email']
            return render_template('adminenrolled.html', username=session['username'])
        return render_template('adminenrolled.html', username=session['username'])

    return redirect(url_for('login'))


@app.route('/admin/courses', methods=['GET', 'POST'])
def admincourses():
    # Check if the user is logged in
    if 'loggedin' in session:
        if request.method == 'POST':
            name = request.form['name']
            age = request.form['age']
            email = request.form['email']
            return render_template('admincourses.html', username=session['username'])
        return render_template('admincourses.html', username=session['username'])

    return redirect(url_for('login'))

@app.route('/enroll/<int:id>/<string:cid>')
def enroll(id, cid):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Enrolled VALUES (%s, %s, NULL)", (id, cid,))
    cursor.execute("UPDATE Courses SET enrolled = enrolled + 1 WHERE cid = %s", (cid,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('enrolled'))


@app.route('/withdraw/<int:id>/<string:cid>')
def withdraw(id, cid):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Enrolled WHERE id = %s and cid = %s", (id, cid,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('enrolled'))


def calculate_gpa(id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        WITH GradePoints AS (
        SELECT
        E.id AS student_id,
        E.cid, 
        CASE
        WHEN grade >= 94 THEN 4.0
        WHEN grade >= 90 THEN 3.7
        WHEN grade >= 87 THEN 3.3
         WHEN grade >= 84 THEN 3.0
        WHEN grade >= 80 THEN 2.7
        WHEN grade >= 77 THEN 2.3
        WHEN grade >= 74 THEN 2.0
        WHEN grade >= 70 THEN 1.7
        WHEN grade >= 67 THEN 1.3
        WHEN grade >= 64 THEN 1.0
        WHEN grade >= 60 THEN 0.7
        WHEN grade >= 0 THEN 0.0
        ELSE NULL
        END AS point,
        C.credits
        FROM
        Enrolled E
        JOIN Courses C ON E.cid = C.cid
        ),
        StudentQualityPoints AS (
        SELECT
        student_id,
        SUM(point * credits) AS total_quality_points,
        SUM(credits) AS total_credit_hours
        FROM
        GradePoints
        GROUP BY
        student_id
        ),
        StudentGPA AS (
        SELECT
        student_id,
        total_quality_points,
        total_credit_hours,
        CASE
            WHEN total_credit_hours > 0 THEN total_quality_points / total_credit_hours
            ELSE NULL
        END AS gpa
        FROM
        StudentQualityPoints)
        SELECT
        ROUND (SG.gpa, 2) AS gpa
        FROM
        Students S
        LEFT JOIN StudentGPA SG ON S.id = SG.student_id
        WHERE S.id = %s
    """, (id,))
    gpa = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()
    return gpa[0]


# -------------------------------------------------------------------------------------
# ORIGINAL INDEX PAGE!!!!
# @app.route('/')
# def index():

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
