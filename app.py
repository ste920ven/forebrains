from flask import request,Flask,render_template, url_for,redirect,request,session
import urllib2,json,util

app=Flask(__name__)
app.secret_key = "JackStevenDinaandBiggsAreAwesomeExceptNotReallyDina1"

@app.route("/",methods=["POST","GET"])
def index():
    if request.method=="GET":
        return render_template("index.html")
    else:
        pending = request.form.keys()[0]
        if "tab" in pending:
            return handleTabs(pending)

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="GET":
        return render_template("login.html")	
    else:
        pending = request.form.keys()[0]
        if "tab" in pending:
            return handleTabs(pending)
        else: 
            if request.form.has_key("submitlogin"):
                user = str(request.form["Username"])
                password = str(request.form["Password"])
                validate = util.checkUserPass(user,password)
                if validate == 0:
                    #User doesn't exist
                    return render_template("login.html")
                if validate == True:
                    session['user'] = user
                    return redirect(url_for("index"))
                if validate == False:
                    #Password Incorrect
                    return render_template("login.html")

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="GET":
        return render_template("signup.html")
    else:
        pending = request.form.keys()[0]
        if "tab" in pending:
            return handleTabs(pending)
        user = str(request.form["user"])
        password = str(request.form["pass1"])
        if password != str(request.form["pass2"]):
            return render_template("signup.html",notmatching=True)
        if util.createUser(user,password):
            return redirect(url_for("login"))
        else:
            return render_template("signup.html",taken=True)

@app.route("/creategame",methods=["POST","GET"])
def creategame():
    if request.method == "GET":
        return render_template("creategame.html")
    else:
        pending = request.form.keys()[0]
        if "tab" in pending:
            return handleTabs(pending)
        if request.form.has_key("submitgame"):
            name = str(request.form["name"])
            password = str(request.form["pass1"])
            if not util.createGame(session["user"],password,name):
                return render_template("creategame.html",taken=True)
            return redirect(url_for("index"))

@app.route("/joingame",methods=["POST","GET"])
def joingame():
    if request.method == "GET":
        return render_template("joingame.html",games=util.getGames())
    else:
        pending = request.form.keys()[0]
        if "tab" in pending:
            return handleTabs(pending)
        if request.form.has_key("submitjoin"):
            name = str(request.form["Gamename"])
            password = str(request.form["Password"])
            if util.checkGamePass(name,password):
                util.addPlayer(name,session["user"])
                return redirect(url_for("index"))
            else:
                return render_template("joingame.html",games=util.getGames())

def handleTabs(pressed):
    if "home" in pressed:
        return redirect(url_for("index"))
    if "login" in pressed:
        return redirect(url_for("login"))
    if "signup" in pressed:
        return redirect(url_for("signup"))
    if "creategame" in pressed:
        return redirect(url_for("creategame"))
    if "joingame" in pressed:
        return redirect(url_for("joingame"))

@app.route("/updatelocation")
def updatelocation():
    game = request.args.get('game', '')
    player = request.args.get('player', '')
    xcor = request.args.get('xcor', '-1')
    ycor = request.args.get('ycor', '-1')
    util.setLoc(game,player, [xcor, ycor])
    return True

@app.route("/getCurrentUser")
def getCurrentUser():
    return session["user"]


if __name__=="__main__":
    app.debug=True
    app.run()
