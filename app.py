from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_session import Session
from passlib.hash import sha256_crypt
# pip install passlib
import sqlite3 as sql

app = Flask(__name__)  # creates flask application


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
    if request.method == 'POST':
        try:
            with sql.connect("Bank.db") as con:
                email = request.form['Email']
                cur = con.cursor()
                # connect to database and grab all info under the email input
                cur.execute("SELECT * FROM Client WHERE Email = ?", [email])
                data = cur.fetchone()[1]  # this fetches the second value. the password
                # now we compare the two passwords. the hashed and the input
                if sha256_crypt.verify(request.form['Password'], data):
                    msg = "success"
                else:
                    msg = "Incorrect"
        except:
            con.rollback()
            msg = "error"
        finally:
            con.close()
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

                if email == "":
                    msg = "no empty strings allowed"
                    raise Exception("no empty strings")

                # if email exists in the system
                cur.execute("SELECT * FROM Client WHERE Email = ?", [email])
                #check if its possible to pull a row and if you can then the email exists
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


if __name__ == '__main__':
    app.run(debug=True)
