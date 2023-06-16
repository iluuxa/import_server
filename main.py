from flask import Flask, render_template, request, session
from flask_login import LoginManager

app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)

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
