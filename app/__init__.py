import os
from flask import Flask, render_template, send_from_directory, request
from dotenv import load_dotenv
from flask_mail import Mail, Message 

load_dotenv()
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
