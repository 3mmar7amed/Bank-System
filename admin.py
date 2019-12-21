import random
import string
import datetime
import utill
from werkzeug.security import  generate_password_hash,check_password_hash




def getallusers():
    return getusers('CustomerID')

def getoneuser(userid):
    return getusers(userid)

def getusers(query):
    connection=utill.getconnection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Customers WHERE CustomerID = ? ',query)
    result=utill.converttolist(cursor)
    connection.close()
    return result

def acceptloan(loanid,amountofloan , userid):
    connection = utill.getconnection()
    cursor = connection.cursor()
    cursor.execute('SELECT CustomerID,Balance FROM Customers WHERE  CustomerID =?;',userid)
    customer = cursor.fetchone()
    accepted='Accepted'
    cancelled="Under-consideration"
    print(loanid)
    print(userid)
    if customer.__getattribute__('Balance') >amountofloan :
        cursor.execute('UPDATE Loan SET status = ? WHERE ID = =?',accepted,loanid)
    else:
        cursor.execute('UPDATE Loan SET status = ? WHERE ID = =?', cancelled, loanid)
    connection.commit()
    connection.close()

def deposite (userid, amount):
    connection = utill.getconnection()
    cursor = connection.cursor()
    status = 'Accepted'
    today = datetime.date.today()
    day = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
    if (utill.isuserexisit(userid)):
        cursor.execute('SELECT CustomerID,Balance FROM Customers WHERE  CustomerID =?', userid)
        depositor = cursor.fetchone()
        balance = depositor.__getattribute__('Amount')
        balance += amount
        cursor.execute("INSERT INTO Depositor (Amount, OwnerID, status,DateOfCreation)values(?,?,?,?)",
                       (balance, userid, status, day))
        cursor.execute("UPDATE Customers SET Balance = ? WHERE ID = =?", balance, userid)
        connection.commit()
    connection.close()


def makecustomer(firstname , lastname , address,city):
    connection = utill.getconnection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Customer (FirstName , LastName , Address , City , Balance) values(?,?,?,?,?)",
                   (firstname,lastname,address,city,0))
    connection.commit()
    connection.close()

def withdraw(userid, amount):
    connection = utill.getconnection()
    cursor = connection.cursor()
    today = datetime.date.today()
    day = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
    cursor.execute('SELECT Balance FROM Customers WHERE  CustomerID =?;', [userid])
    customer = cursor.fetchone()
    balence = customer.__getattribute__('Balance')
    if (utill.isuserexisit(userid) and amount <= balence and amount<1000000):
        balence-=amount
        cursor.execute('SELECT * FROM Customers')
        cursor.execute('UPDATE Customers SET Balance = ? WHERE ID = =?', balence, userid)
        cursor.execute("INSERT INTO Withdraw ( DateOfCreation , Amount  , OwnerID  ) values(?,?,?)",
                       (day, amount, userid))



def makepsw():
    stringLength=10
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def makeuser(userid):
    psw=makepsw()
    print(psw)
    password_hash = generate_password_hash(psw)
    connection=utill.getconnection()
    cursor = connection.cursor()
    user=getoneuser(userid)
    firstname=utill.getuserattribute(user,"FirstName")
    username = firstname+userid
    cursor.execute ("INSERT INTO Users ( CustomerID , UserName  , Psw  ) values(?,?,?)",
                       (userid, username, password_hash))
    cursor.commit()
    connection.close()

