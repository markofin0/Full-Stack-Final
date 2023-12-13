import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

DATABASE = 'users.db'
app = Flask(__name__)
app.secret_key = 'some_secret_key'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_KEY_PREFIX'] = 'login_session:'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
def main_page():
    session['authenticated'] = False
    return render_template('test.html')


@app.route('/addingsoon', methods=['GET', 'POST'])
def addingsoon_page():
    return render_template('addingsoon.html')


@app.route('/snake', methods=['GET', 'POST'])
def snake():
    return render_template('snake.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['authenticated'] = False
    return render_template('logout.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        cur.execute("SELECT * from users WHERE email=? AND password=?",
                    (request.form['username'], request.form['password']))

        if cur.fetchone() is None:
            con.close()
            return render_template('index.html', error_message='Invalid credentials')
        else:
            con.close()
            session['authenticated'] = True
            session['name'] = request.form['username']
            return render_template('test.html')  # Redirect to the main page after login
    return render_template('index.html', error_message=None)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the email already exists in the database
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if user:
            # Email already exists, return an error
            error_message = 'Email already exists. Please choose a different email.'
            conn.close()
            return render_template('signup.html', error_message=error_message)

        # Email does not exist, insert the new user into the database
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        conn.close()

        # Redirect to a success page or login page
        return redirect(url_for('login'))

    return render_template('signup.html', error_message=None)


if __name__ == '__main__':
    app.run(debug=True, port=5150)
