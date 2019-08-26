from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
import ctypes

app = Flask(__name__)

#auto reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

#session setting
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#DateBase
db = SQL("sqlite:///Stamp.db")

#Home page
@app.route("/")
@login_required
def index():

    #data processing
    budget = db.execute("SELECT budget FROM user WHERE id = :id",id = session["user_id"])

    alert = db.execute("SELECT alert1 FROM user WHERE id = :id",id = session["user_id"])
    alert = alert[0]["alert1"]


    if alert == None:
        alert = 0

    expenes = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND ei = 'Expense' ",id = session["user_id"])
    expenes = expenes[0]["SUM(amount)"]

    if expenes == None:
        expenes = 0

    income =  db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND ei = 'Income' ",id = session["user_id"])
    income = income[0]["SUM(amount)"]

    if income == None:
        income = 0

    food = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Food' ",id = session["user_id"])
    food = food[0]["SUM(amount)"]

    if food == None:
        food = 0

    transportation = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Transportation' ",id = session["user_id"])
    transportation = transportation[0]["SUM(amount)"]

    if transportation == None:
        transportation = 0

    daily = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Daily Supplies' ",id = session["user_id"])
    daily = daily[0]["SUM(amount)"]

    if daily == None:
        daily = 0

    social = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Social' ",id = session["user_id"])
    social = social[0]["SUM(amount)"]

    if social == None:
        social = 0

    enter = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Entertainment' ",id = session["user_id"])
    enter = enter[0]["SUM(amount)"]

    if enter == None:
        enter = 0

    snack = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Snack' ",id = session["user_id"])
    snack = snack[0]["SUM(amount)"]

    if snack == None:
        snack = 0

    clothes = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Clothes' ",id = session["user_id"])
    clothes = clothes[0]["SUM(amount)"]

    if clothes == None:
        clothes = 0

    rent = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Rent' ",id = session["user_id"])
    rent = rent[0]["SUM(amount)"]

    if rent == None:
        rent = 0

    medical = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Medical' ",id = session["user_id"])
    medical = medical[0]["SUM(amount)"]

    if medical == None:
        medical = 0

    Eother = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Other' AND ei = 'Expense' ",id = session["user_id"])
    Eother = Eother[0]["SUM(amount)"]

    if Eother == None:
        Eother = 0


    salary = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Salary' ",id = session["user_id"])
    salary = salary[0]["SUM(amount)"]

    if salary == None:
        salary = 0

    gift = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Gift' ",id = session["user_id"])
    gift = gift[0]["SUM(amount)"]

    if gift == None:
        gift = 0

    credit = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Credit' ",id = session["user_id"])
    credit = credit[0]["SUM(amount)"]

    if credit == None:
        credit = 0

    Iother = db.execute("SELECT SUM(amount) FROM trans WHERE id = :id AND type = 'Other' AND ei = 'Income' ",id = session["user_id"])
    Iother = Iother[0]["SUM(amount)"]

    if Iother == None:
        Iother = 0
    #finish

    #status
    if expenes > income:
        word1 = " You spend more than you get "
        wordtype1 = "danger"
    else:
        word1 = " Good "
        wordtype1 = "success"

    if expenes > budget[0]["budget"]:
        word2 = "Over Budget"
        wordtype2 = "danger"
    else:
        word2 = "Not Over Budget"
        wordtype2 = "success"

    if expenes > alert:
        word3 = "Over Alert Amount"
        wordtype3 = "danger"
    else:
        word3 = "Not Over Alert Amount"
        wordtype3 = "success"

    return render_template("home.html",expenes = expenes,income = income
    ,budget = budget[0]["budget"],total = income - expenes,food = food
    ,transportation = transportation,daily = daily,social = social,enter = enter,snack = snack, clothes = clothes
    ,rent = rent,medical = medical,Eother = Eother,salary = salary,gift = gift,credit = credit,Iother = Iother, word1 = word1,wordtype1 = wordtype1,word2 = word2,wordtype2 = wordtype2,word3 = word3,wordtype3 = wordtype3)


#login
@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        check = db.execute("SELECT username FROM user WHERE username = :username",username = request.form.get("username"))

        rows = db.execute("SELECT * FROM user WHERE username = :username",username=request.form.get("username"))


        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Password or Username not correct")
            return render_template("login.html",type = "danger")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("Success")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#logout
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

#register
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        check = db.execute("SELECT username FROM user WHERE username = :username",username = request.form.get("username"))
        if not request.form.get("password") == request.form.get("confirmation"):
            flash("Password confirmation not correct")
            return render_template("register.html",type = "danger")
        try:
            if not check[0]['username'] == None:
                flash("Username have been used")
                return render_template("register.html",type = "danger")
        except:
            pass

        hash = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO user (username, password) VALUES(:username, :hash)",username=request.form.get("username"),hash = hash)

        id = db.execute("SELECT id FROM user WHERE :username",username=request.form.get("username"))

        rows = db.execute("SELECT * FROM user WHERE username = :username",username=request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        flash("Success")
        return redirect("/")
    else:
        return render_template("register.html")

#expenses page
@app.route("/expenses", methods=["GET","POST"])
@login_required
def expenses():
    if request.method == "POST":
        if not float(request.form.get("amount")) > 0  :
            flash("Please input number to amount greater than 0 ")
            return render_template("income.html",type = "danger")

        db.execute("INSERT INTO trans (id,type,amount,ei) VALUES(:id,:type,:amount,:ei)",id = session["user_id"], type=request.form.get("type"), amount = round(float(request.form.get("amount")),2),ei = "Expense")
        flash("Success")
        return redirect("/")
    else:
        return render_template("expenses.html")

#income page
@app.route("/income", methods=["GET","POST"])
@login_required
def income():

    if request.method == "POST":
        if not float(request.form.get("amount")) > 0  :
            flash("Please input number to amount greater than 0 ")
            return render_template("income.html",type = "danger")

        db.execute("INSERT INTO trans (id,type,amount,ei) VALUES(:id,:type,:amount,:ei)",id = session["user_id"], type=request.form.get("type"), amount = round(float(request.form.get("amount")),2),ei = "Income")
        flash("Success")
        return redirect("/")
    else:
        return render_template("income.html")
#history page
@app.route("/history", methods=["GET","POST"])
@login_required
def hisory():
    rows = db.execute("SELECT * FROM trans WHERE id = :id ORDER BY time DESC ",id = session["user_id"])
    return render_template("history.html",rows = rows)

#delete page
@app.route("/delete", methods=["GET","POST"])
@login_required
def delete():
    if request.method == "POST":
        caseidcheck = db.execute("SELECT caseid FROM trans WHERE id = :id AND caseid = :caseid",id = session["user_id"],caseid = request.form.get("caseid"))
        try:
            if caseidcheck[0]['caseid'] == request.form.get("caseid"):
                pass
        except:
            flash("CaseID worng or you not own this case")
            return render_template("delete.html",type = "danger")

        rows = db.execute("DELETE FROM trans WHERE caseid = :caseid",caseid = request.form.get("caseid"))
        flash("Success")
        return redirect("/")
    else:
        return render_template("delete.html")


#budget page ---budget function
@app.route("/budget", methods=["GET","POST"])
@login_required
def budget():
    if request.method == "POST":
        if not float(request.form.get("budget")) > 0  :
            flash("Please input number to amount greater than 0 ")
            return render_template("income.html",type = "danger")
        db.execute("UPDATE user SET budget = :budget WHERE id = :id",budget = round(float(request.form.get("budget")),2),id = session["user_id"])
        flash("Success")
        return redirect("/")
    else:
        return render_template("budget.html")

#budget page ----alert function
@app.route("/alert", methods=["GET","POST"])
@login_required
def alert():
    if request.method == "POST":
        if not float(request.form.get("alert")) > 0  :
            flash("Please input number to amount greater than 0 ")
            return render_template("income.html",type = "danger")
        db.execute("UPDATE user SET alert1 = :alert WHERE id = :id",alert = round(float(request.form.get("alert")),2),id = session["user_id"])
        flash("Success")
        return redirect("/")
    else:
        return render_template("budget.html")