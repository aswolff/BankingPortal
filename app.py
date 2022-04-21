import random
# pip install passlib
import sqlite3 as sql
import string

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from passlib.hash import sha256_crypt

app = Flask(__name__)  # creates flask application

app.secret_key = 'b@D-$EcR3T_KEy!'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Bank'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/closeIssue')
def closeIssue():
    return render_template('closeIssue.html', email=session['email'])


@app.route('/deleteReq')
def deleteReq():
    return render_template('deleteRequest.html')


@app.route('/auth_user', methods=['POST', 'GET'])
def auth_user():
    msg = ""
    if request.method == 'POST':
        email = request.form['Email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # connect to database and grab all info under the email input
        cur.execute("SELECT * FROM Client WHERE Email = %s", [email])

        test_email = cur.fetchall()
        if len(test_email) == 0:
            msg = "Error. Email not found in system"
            return render_template("result.html", msg=msg)

        # connect to database and grab all info to find password
        cur.execute("SELECT * FROM Client WHERE Email = %s", [email])
        data = cur.fetchone()  # this fetches the second value. the password
        data = data.get('Password')
        # now we compare the two passwords. the hashed and the input
        if sha256_crypt.verify(request.form['Password'], data):
            cur.execute("SELECT * FROM Client WHERE Email = %s", [email])
            values = cur.fetchone()
            firstName = values.get('FirstName')
            lastName = values.get('LastName')
            employed = values.get('Employee')
            session['logged_in'] = True
            session['email'] = email
            session['firstName'] = firstName
            session['lastName'] = lastName

            if employed == 1:
                session['employee'] = True

            msg = "Successfully logged in"
            return redirect(url_for('dashboard'))
        else:
            msg = "Incorrect password"
    return render_template("result.html", msg=msg)


@app.route('/register_user', methods=['POST', 'GET'])
def register_user():
    msg = ""
    if request.method == 'POST':
        try:
            email = request.form['Email']
            first = request.form['FirstName']
            last = request.form['LastName']

            password = sha256_crypt.hash((str(request.form['Password'])))

            if request.form['Email'] == "":
                msg = "no empty emails allowed"
                raise Exception("no empty strings")

            if request.form['FirstName'] == "":
                msg = "Must Fill Out First Name"
                raise Exception("no empty strings")

            if request.form['LastName'] == "":
                msg = "Must Fill Out Last Name"
                raise Exception("no empty strings")

            if request.form['Password'] == "":
                msg = "must have a password entered"
                raise Exception("no empty passwords")

            # if email exists in the system
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM Client WHERE Email = %s', [email])
            # check if it is possible to pull a row and if you can then the email exists
            if cur.fetchone():
                print("test")
                msg = "this email is already in use"
                raise Exception("email already in use")

            cur.execute('INSERT INTO Client (Email,Password,FirstName,LastName) VALUES (%s,%s,%s,%s)',
                        (email, password, first, last))
            mysql.connection.commit()
            msg = "Account Made"

        finally:
            return render_template("result.html", msg=msg)


@app.route('/auth_user/dashboard')
def dashboard():
    if 'logged_in' in session:
        if 'employee' in session:
            return render_template('employee.html', firstName=session['firstName'], lastName=session['lastName'])
        return render_template('dashboard.html', firstName=session['firstName'], lastName=session['lastName'])
    return redirect(url_for('auth_user'))


@app.route('/auth_user/logout')
def logout():
    session.pop('logged_in', False)
    session.pop('email', None)
    session.pop('employee', False)
    session.pop('firstName', None)
    session.pop('lastName', None)
    return redirect(url_for('home'))


@app.route('/helpReq')
def helpReq():
    return render_template('helpRequest.html', firstName=session['firstName'], lastName=session['lastName'])


@app.route('/submitHelp', methods=['POST', 'GET'])
def submitHelp():
    if request.method == 'POST':
        try:
            problem = request.form['Problem']
            time = request.form['submissionTime']
            email = session['email']
            ''' 
            Used this source to generate random HelpNumber used below. by Worrisome Wallaby on May 11 2020
            https://www.codegrepper.com/code-examples/python/python+get+random+uppercase+letter
            '''
            HelpNumber = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            with sql.connect("Bank.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Issue (Email, Problem, Date, Number) VALUES (?,?,?,?)",
                            (email, problem, time, HelpNumber))
                con.commit()
        except:
            con.rollback()
            msg = "Something went wrong..."
        finally:
            con.close()
            if 'employee' in session:
                return render_template('employee.html', firstName=session['firstName'], lastName=session['lastName'])
            return render_template('dashboard.html', firstName=session['firstName'], lastName=session['lastName'])


@app.route('/viewHelp', methods=['POST', 'GET'])
def viewHelp():
    con = sql.connect("Bank.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Issue ORDER BY Date ASC")
    rows = cur.fetchall()
    con.close()
    return render_template('viewHelp.html', rows=rows)


@app.route('/viewUsersRequests', methods=['POST', 'GET'])
def viewUsersRequests():
    con = sql.connect("Bank.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Issue WHERE Email = ? ORDER BY Date ASC", [session['email']])
    rows = cur.fetchall()
    con.close()
    return render_template('viewUsersRequests.html', rows=rows)


@app.route('/closing', methods=['POST', 'GET'])
def closing():
    if request.method == 'POST':
        try:
            resolved = request.form['Problem']
            number = request.form['HelpNumber']
            email = session['email']

            with sql.connect("Bank.db") as con:
                cur = con.cursor()

                cur.execute("SELECT * FROM Issue WHERE Number = ?", [number])
                check_num = cur.fetchall()
                if len(check_num) == 0:
                    msg = "Unable to find this help request number"
                    return render_template("result.html", msg=msg)

                sqlstate = "UPDATE Issue SET Resolution = ?, ClosedBy = ? WHERE Number = ?"
                cur.execute(sqlstate, (resolved, email, number))
                con.commit()
        except:
            con.rollback()
            msg = "Something went wrong..."
            return render_template("result.html", msg=msg)
        finally:
            con.close()
            if 'employee' in session:
                return render_template('employee.html', firstName=session['firstName'], lastName=session['lastName'])
            return render_template('dashboard.html', firstName=session['firstName'], lastName=session['lastName'])


@app.route('/deleteRequest', methods=['POST', 'GET'])
def deleteRequest():
    if request.method == 'POST':
        try:
            num = request.form['HelpNum']
            with sql.connect("Bank.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Issue WHERE Number = ?", [num])
                check_email = cur.fetchone()[0]
                if session['email'] == check_email:
                    cur.execute("DELETE FROM Issue WHERE Number = ?", [num])
                con.commit()
        except:
            con.rollback()
            msg = "Something went wrong..."
            return render_template("result.html", msg=msg)
        finally:
            con.close()
            if 'employee' in session:
                return render_template('employee.html', firstName=session['firstName'], lastName=session['lastName'])
            return render_template('dashboard.html', firstName=session['firstName'], lastName=session['lastName'])


if __name__ == '__main__':
    app.run(debug=True)
