from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from passlib.hash import sha256_crypt
# pip install passlib
import sqlite3 as sql

app = Flask(__name__)  # creates flask application

app.config['SECRET_KEY'] = 'my_secret'
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
                session['logged_in'] = True
                session['username'] = email
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
            password = sha256_crypt.encrypt((str(request.form['Password'])))
            with sql.connect("Bank.db") as con:
                cur = con.cursor()

                if request.form['Email'] == "":
                    msg = "no empty emails allowed"
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

                cur.execute("INSERT INTO Client (Email,Password) VALUES (?,?)", (email, password))
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
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('auth_user'))


@app.route('/auth_user/logout')
def logout():
    session.pop('logged_in', False)
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/helpReq')
def helpReq():
    return render_template('helpRequest.html', username=session['username'])


@app.route('/submitHelp', methods=['POST', 'GET'])
def submitHelp():
    if request.method == 'POST':
        try:
            problem = request.form['Problem']
            time = request.form['submissionTime']
            email = session['username']

            with sql.connect("Bank.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Issue (Email, Problem, Date) VALUES (?,?,?)",
                            (email, problem, time))
                con.commit()
                msg = "Message Sent. Expect to hear back from us soon!"
        except:
            con.rollback()
            msg = "Something went wrong..."
        finally:
            con.close()
            return render_template('dashboard.html', username=session['username'])


if __name__ == '__main__':
    app.run(debug=True)
