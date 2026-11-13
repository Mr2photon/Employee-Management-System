
from flask import Flask, render_template
from database import init_db

#initialize flask application
app = Flask(__name__)

#Home page route
@app.route("/")
def home():
    return render_template("index.html")

#Start the development server
if __name__=="__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)