import os
from flask import Flask, render_template, send_from_directory, request
import flask
from dotenv import load_dotenv
from flask_mail import Mail, Message
from . import db 
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db

load_dotenv()
app = Flask(__name__)

app.config['DATABASE'] = os.path.join(os.getcwd(), 'flask.sqlite')
db.init_app(app)

# Configuration for flask_mail 
# This setup is specifically for gmail, other email servers have different configuration settings 
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# These need to be setup in .env file 
app.config['MAIL_USERNAME'] = os.getenv("EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASSWORD")

# Emails are managed through a mail instance 
mail = Mail(app)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data 
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Compose email and send 
        msg = Message(subject=f"Mail from {name}", body=f"Name: {name}\nEmail: {email}\n\nMessage: {message}", recipients=[os.getenv("EMAIL")], sender=os.getenv("EMAIL"))
        mail.send(msg)

        # success value determines that success alert will appear 
        return render_template('index.html', success=True , title="MLH Fellow", url=os.getenv("URL"))


    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/health')
def health():
    status_code = flask.Response(status=200)
    return status_code

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return f"User {username} created successfully"
        else:
            return error, 418

    ## TODO: Return a restister page
    return "Register Page not yet implemented", 501


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            return "Login Successful", 200 
        else:
            return error, 418
    
    ## TODO: Return a login page
    return "Login Page not yet implemented", 501



# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000, debug=False)


