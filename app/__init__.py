import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()
app = Flask(__name__)

## Data base configuration

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
    user=os.getenv("POSTGRES_USER"),
    passwd=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    table=os.getenv("POSTGRES_DB"),
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserModel(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}>"


# Configuration for flask_mail
# This setup is specifically for gmail, other email servers have different configuration settings
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
# These need to be setup in .env file
app.config["MAIL_USERNAME"] = os.getenv("EMAIL")
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASSWORD")

# Emails are managed through a mail instance
mail = Mail(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Compose email and send
        msg = Message(
            subject=f"Mail from {name}",
            body=f"Name: {name}\nEmail: {email}\n\nMessage: {message}",
            recipients=[os.getenv("EMAIL")],
            sender=os.getenv("EMAIL"),
        )
        mail.send(msg)

        # success value determines that success alert will appear
        return render_template(
            "index.html", success=True, title="MLH Fellow", url=os.getenv("URL")
        )

    return render_template("index.html", title="MLH Fellow", url=os.getenv("URL"))


@app.route("/health")
def health():
    return "Its working!"


@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = f"User {username} is already registered."

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            return render_template("register.html", error=error)

    ## TODO: Return a restister page
    return render_template("register.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error=error)

    return render_template("login.html")
