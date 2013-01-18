from flask import request,Flask,render_template, url_for,redirect,request
import urllib2,json

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

if __name__=="__main__":
    app.debug=True
    app.run()
