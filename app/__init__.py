import os
from flask import Flask, render_template, send_from_directory, request
from dotenv import load_dotenv
from flask_mail import Mail, Message 

load_dotenv()
app = Flask(__name__)

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv("EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASSWORD")

mail = Mail(app)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        msg = Message(subject=f"Mail from {name}", body=f"Name: {name}\nEmail: {email}\n\nMessage: {message}", recipients=[os.getenv("EMAIL")], sender=os.getenv("EMAIL"))
        mail.send(msg)
        return render_template('index.html', success=True , title="MLH Fellow", url=os.getenv("URL"))


    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))
