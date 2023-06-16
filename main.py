from flask import Flask, render_template, request, session
from flask_login import LoginManager

app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)


class User:
    auth = False
    activity = True
    anon = False
    id = "root"

    def is_authenticated(self):
        return self.auth

    def is_active(self):
        return self.activity

    def is_anonymous(self):
        return self.anon

    def get_id(self):
        return self.id


@app.route('/import')
def import_page():
    return render_template("import.html")


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/login', methods=["POST"])
def login():
    _username = request.form['username']
    _password = request.form['password']
    if _username and _password:
        return import_page()
    else:
        return main()


@lm.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    app.run()
