import random
# pip install passlib
import sqlite3 as sql
import string

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

app = Flask(__name__)  # creates flask application

app.config['SECRET_KEY'] = 'b@D-$EcR3T_KEy!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db

sess = Session(app)

db.create_all()


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
        with sql.connect("Bank.db") as con:
            email = request.form['Email']
            cur = con.cursor()

            # connect to database and grab all info under the email input
            cur.execute("SELECT * FROM Client WHERE Email = ?", [email])
            test_email = cur.fetchall()
            if len(test_email) == 0:
                msg = "Error. Email not found in system"
                return render_template("result.html", msg=msg)

            # connect to database and grab all info to find password
            cur.execute("SELECT * FROM Client WHERE Email = ?", [email])
            data = cur.fetchone()[1]  # this fetches the second value. the password
            # now we compare the two passwords. the hashed and the input
            if sha256_crypt.verify(request.form['Password'], data):
                cur.execute("SELECT * FROM Client WHERE Email = ?", [email])
                firstName = cur.fetchone()[2]
                cur.execute("SELECT * FROM Client WHERE Email = ?", [email])
                lastName = cur.fetchone()[3]
                cur.execute("SELECT * FROM Client WHERE Email = ?", [email])
                employed = cur.fetchone()[4]

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
            password = sha256_crypt.encrypt((str(request.form['Password'])))
            with sql.connect("Bank.db") as con:
                cur = con.cursor()
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
                cur.execute("SELECT * FROM Client WHERE Email = ?", [email])
                # check if it is possible to pull a row and if you can then the email exists
                if cur.fetchone():
                    print("test")
                    msg = "this email is already in use"
                    raise Exception("email already in use")

                cur.execute("INSERT INTO Client (Email,Password,FirstName,LastName) VALUES (?,?,?,?)",
                            (email, password, first, last))
                con.commit()

                msg = "Account Made"
        except Exception as e:
            con.rollback()
        finally:
            con.close()
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
                cur.execute("DELETE FROM Issue WHERE Number = ?", [num])
                print("ok")
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
