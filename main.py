import os
import csv
import flask_login
from flask import Flask, render_template, request, session, flash, get_flashed_messages, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import psycopg2

app = Flask(__name__)
app.secret_key = '73280e257935a69d4489030386bd6e050a75c596da2c8d0604082c6d3423e62d'
UPLOAD_FOLDER = '/Документы/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
lm = LoginManager()
lm.init_app(app)
crypt = Bcrypt(app)


def get_connection():
    try:
        return psycopg2.connect(dbname='file_import_db', user='postgres', password='ling5089', host='127.0.0.1')
    except:
        print('Can`t establish connection to database')


def register_user(username, password):
    with get_connection() as conn:
        conn.cursor().execute('INSERT INTO users (username, password) values (%s,%s)',
                              (username, crypt.generate_password_hash(password).decode('UTF-8')))
        conn.commit()
    return


def get_user_by_id(user_id):
    with get_connection().cursor() as cur:
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_tuple = cur.fetchone()
        if not user_tuple:
            return
        return User(user_tuple[0], user_tuple[1], user_tuple[2])


def get_user_by_name(username):
    with get_connection().cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_tuple = cur.fetchone()
        if not user_tuple:
            return
        return User(user_tuple[0], user_tuple[1], user_tuple[2])


class User(UserMixin):
    id = "0"
    username = "root"
    password = "root"

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


@app.route('/import', methods=["GET", "POST"])
@login_required
def import_page():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and (file.filename[-3:].__eq__("csv")):
            filename = secure_filename(file.filename)
            print(os.path.join(app.config['UPLOAD_FOLDER'], str(flask_login.current_user.id)))
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], str(flask_login.current_user.id)), exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(flask_login.current_user.id), filename))
            flash("File " + file.filename + " saved!")
            return redirect(request.url)
    return render_template("import.html")


@app.route('/profile')
@login_required
def profile_page():
    files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], str(flask_login.current_user.id)))
    return render_template("profile.html", files=files)


@app.route('/')
def main():
    if flask_login.user_logged_in:
        return redirect("/profile", 301)
    return redirect("/login", 301)


def read_csv(user_id, filename):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], str(user_id), filename)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        table = []
        for row in csv_reader:
            table.append(row)
        print(table)
        return table


@app.route('/view', methods=["GET", "POST"])
@login_required
def document_view():
    content = read_csv(flask_login.current_user.id, request.form["Open"])
    return render_template("view.html", content=content)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_rep = request.form['password_rep']
        if password_rep.__eq__(password):
            register_user(username, password)
            flash('Registration successful')
            return redirect("/login", code=302)
        flash("Passwords don't match")
    return render_template('registration.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        _username = request.form['username']
        _password = request.form['password']
        _user = get_user_by_name(_username)
        if not _user:
            flash('No registered user with this username')
            return render_template("index.html")
        if not crypt.check_password_hash(str(_user.password), str(_password)):
            flash('Wrong password')
            return render_template("index.html")
        login_user(_user)
        return redirect("/profile", 301)
    return render_template("index.html")


@lm.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


if __name__ == '__main__':
    app.run()
