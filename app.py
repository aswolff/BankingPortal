from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        try:
            email = request.form['Email']
            password = request.form['Password']

            with sql.connect("Bank.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Client WHERE Email = ? AND Password = ?", (email, password))
                account = cur.fetchone()
                if account:
                    msg = "success"
                else:
                    msg = "Incorrect"
        except:
            con.rollback()
            msg = "error"
        finally:
            return render_template("result.html", msg=msg)
            con.close()


if __name__ == '__main__':
    app.run(debug=True)
