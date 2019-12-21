from flask import Flask
from flask import request,session
from flask_session import Session
import admin
import utill
from flask import render_template

app = Flask(__name__)
app.config["SESSION_TYPE"] ="filesystem"
app.config['DEBUG'] = True

Session(app)

@app.route('/users' )
def hello_world():
    customers =admin.getallusers()
    return render_template("customers.html",items=customers)


@app.route('/index', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.values.get('uname')
        password = request.values.get('psw')
        id=utill.checklogin(username,password)
        if id :
            userid = utill.getuseridbyusername(username)
            session["userid"] = userid
            if session["userid"] is not None:
                user = admin.getoneuser(userid)
                return render_template("userhome.html", item=user)


    return render_template("login.html")

@app.route('/loans')
def showloans():
    userid=session["userid"]
    if userid is not None:
        loans=utill.getuserloans(userid)
        return render_template("userhistory.html", items=loans)
    return render_template("login.html")

@app.route('/signout')
def signout():
    session["userid"]=None
    return (login())

@app.route('/Withdraw')
def showWithdraw():
    userid=session["userid"]
    if userid is not None:
        withdraw=utill.getuserWithdrawals(userid)
        return render_template("withdraw.html", items=withdraw)
    return render_template("login.html")

@app.route('/Depositor')
def showDepositor():
    userid=session["userid"]
    if userid is not None:
        Depositor=utill.getuserdepository(userid)
        return render_template("Depositor.html", items=Depositor)
    return render_template("login.html")

@app.route('/Transaction')
def showTransaction():
    userid=session["userid"]
    if userid is not None:
        Transaction=utill.getusertransationsmade(userid)
        return render_template("Transaction.html", items=Transaction)
    return render_template("login.html")
@app.route('/askforloan' ,  methods=['GET', 'POST'])
def askforloan():
    userid = session["userid"]
    print(userid)
    if userid is not None :
        if request.method == 'POST':
         newloan = int(request.form.get("loan"))
         utill.AskForLoan(userid, newloan)
        else:
            return render_template("askforloan.html")
    else:
        return login()
        return render_template("askforloan.html", Message ="your loan is successfully submited")
    return render_template("login.html")
