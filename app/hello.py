import os

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="MLH Fellow", url=os.getenv("URL"))


# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000, debug=False)
