import configparser
import csv
import os

import flask_login
import psycopg2
from psycopg2 import OperationalError, ProgrammingError
from flask import Flask, render_template, request, flash, redirect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.utils import secure_filename

app = Flask(__name__)
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'config.ini'), encoding='utf-8')
app.secret_key = config['DEFAULT']['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = config['DEFAULT']['UPLOAD_FOLDER']
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
crypt = Bcrypt(app)


def register_user(username, password):
    with psycopg2.connect(dbname=config['DATABASE']['DB_NAME'], user=config['DATABASE']['DB_USER'],
                          password=config['DATABASE']['DB_PASSWORD'],
                          host=config['DATABASE']['DB_HOST'], port=5432) as conn:
        conn.cursor().execute('INSERT INTO users (username, password) values (%s,%s)',
                              (username, crypt.generate_password_hash(password).decode('UTF-8')))
        conn.commit()
    return


def get_user_by_id(user_id):
    with psycopg2.connect(dbname=config['DATABASE']['DB_NAME'], user=config['DATABASE']['DB_USER'],
                          password=config['DATABASE']['DB_PASSWORD'],
                          host=config['DATABASE']['DB_HOST'], port=5432).cursor() as cur:
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_tuple = cur.fetchone()
        if not user_tuple:
            return
        return User(user_tuple[0], user_tuple[1], user_tuple[2])


def get_user_by_name(username):
    with psycopg2.connect(dbname=config['DATABASE']['DB_NAME'], user=config['DATABASE']['DB_USER'],
                          password=config['DATABASE']['DB_PASSWORD'],
                          host=config['DATABASE']['DB_HOST'], port=5432).cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user_tuple = cur.fetchone()
        if not user_tuple:
            return
        return User(user_tuple[0], user_tuple[1], user_tuple[2])


class User(UserMixin):
    id = "0"
    username = "root"
    password = "root"

    def __init__(self, user_id, username, password):
        self.id = user_id
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
            # print(os.path.join(app.config.ini['UPLOAD_FOLDER'], str(flask_login.current_user.id)))
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], str(flask_login.current_user.id)), exist_ok=True)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(flask_login.current_user.id), filename))
            flash("File " + file.filename + " saved!")
            return redirect(request.url)
    return render_template("import.html")


@app.route('/profile')
@login_required
def profile_page():
    files = []
    preview = []
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], str(flask_login.current_user.id))):
        files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], str(flask_login.current_user.id)))
        for file in files:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], str(flask_login.current_user.id), file)) as csv_file:
                preview.append(next(csv.reader(csv_file, delimiter=',')))
    return render_template("profile.html", files=files, preview=preview)


@app.route('/')
def main():
    return redirect("/profile", 301)


def read_csv(user_id, filename):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], str(user_id), filename)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        table = []
        for row in csv_reader:
            table.append(row)
        # print(table)
        return table


@app.route('/view', methods=["GET", "POST"])
@login_required
def document_view():
    # print(request.form["Open"])
    content = read_csv(flask_login.current_user.id, request.form["Open"])
    return render_template("view.html", content=content)


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete_file():
    if request.method == "POST":
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"], str(flask_login.current_user.id), request.form["Delete"]))

    return profile_page()


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_rep = request.form['password_rep']
        if username and password and password_rep.__eq__(password):
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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login', 301)


@lm.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


def db_init():
    with psycopg2.connect(dbname=config['DATABASE']['DB_NAME'], user=config['DATABASE']['DB_USER'],
                          password=config['DATABASE']['DB_PASSWORD'],
                          host=config['DATABASE']['DB_HOST'], port=5432) as conn:
        conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS public.users
            (
                id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
                username text COLLATE pg_catalog."default",
                password text COLLATE pg_catalog."default",
                CONSTRAINT users_pkey PRIMARY KEY (id)
            )
            
            TABLESPACE pg_default;
            """)
        conn.commit()
    return


if __name__ == '__main__':
    db_init()
    app.run(host="0.0.0.0", port=5000)
