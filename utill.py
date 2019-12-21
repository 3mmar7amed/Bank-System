import pyodbc
import datetime
import admin
from werkzeug.security import generate_password_hash,check_password_hash

def getuserattribute(user,attribute):
    dic=user[0]
    return dic[attribute]

def getconnection():
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-IBU03MH\AMMARSQL;'
                      'Database=master;'
                      'Trusted_Connection=yes;')
    return conn
def converttolist(cursor):
    results = []
    columns = [column[0] for column in cursor.description]
    customers=cursor.fetchall()
    for customer in customers:
        results.append(dict(zip(columns, customer)))
    return results

def getuserhistory(userid):
    result=[]
    result.extend(getuserloans(userid))
    result.extend(getusertransationsmade(userid))
    result.extend(getusertransationsrec(userid))
    result.extend(getuserdepository(userid))
    result.extend(getuserWithdrawals(userid))
    result=sorted(result, key=lambda k: k['DateOfCreation'])
    result.reverse()
    return result
def getuserdepository(userid) :
    conn = getconnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Depositor WHERE OwnerID = ? ', userid)
    deposit = converttolist(cursor)
    deposit = sorted(deposit, key=lambda k: k['DateOfCreation'])
    deposit.reverse()
    conn.close()
    return deposit

def acceptloan(loanid,amountofloan , userid):
    connection = getconnection()
    cursor = connection.cursor()
    cursor.execute('SELECT CustomerID,Balance FROM Customers WHERE  CustomerID =?;',userid)

    customer = cursor.fetchone()
    balance = customer.__getattribute__('Balance')
    accepted='Accepted'
    cancelled="Under-consideration"
    if balance >amountofloan :
        cursor.execute('UPDATE Loan SET status = ? WHERE ID = =?',accepted,loanid)
    else:
        cursor.execute('UPDATE Loan SET status = ? WHERE ID = =?', cancelled, loanid)
    connection.commit()
    connection.close()

def getuserWithdrawals(userid) :
    conn = getconnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Withdraw WHERE OwnerID = ? ', userid)
    withdraw = converttolist(cursor)
    withdraw = sorted(withdraw, key=lambda k: k['DateOfCreation'])
    withdraw.reverse()
    conn.close()
    return withdraw


def getuserloans(userid):
    conn = getconnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Loan WHERE OwnerID = ? ', userid)
    loans = converttolist(cursor)
    loans = sorted(loans, key=lambda k: k['DateOfCreation'])
    loans.reverse()
    conn.close()
    return loans

def getusertransationsmade(userid):
    conn = getconnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Transations WHERE OwnerID = ? ', userid)
    transationsmade = converttolist(cursor)
    transationsmade = sorted(transationsmade, key=lambda k: k['DateOfCreation'])
    transationsmade.reverse()

    conn.close()
    return transationsmade

def getusertransationsrec(userid):
    conn = getconnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Transations WHERE RecieverID = ? ', userid)
    transationtrecived = converttolist(cursor)
    transationtrecived = sorted(transationtrecived, key=lambda k: k['DateOfCreation'])
    transationtrecived.reverse()
    conn.close()
    return transationtrecived

def transact(senderid,recevierid,amount):
    connection = getconnection()
    cursor = connection.cursor()
    senderbalance=0
    recevierbalance =0
    isfound = isuserexisit(recevierid)
    cursor.execute('SELECT CustomerID,Balance FROM Customers')
    customers=cursor.fetchall()
    for customer in customers:
         balance =customer.__getattribute__('Balance')
         if customer.__getattribute__('CustomerID') == senderid:
             senderbalance=balance
         elif customer.__getattribute__('CustomerID') == recevierid:
             recevierbalance= balance
    if isfound and senderbalance > amount:
        senderbalance-=amount
        recevierbalance+=amount
        cursor.execute()

    connection.close()

def AskForLoan(id , amountofloan):
    today = datetime.date.today()
    day=str(today.year) +'-' +str(today.month) +'-' +str(today.day)
    status="Under-consideration"
    isexist=isuserexisit(id)
    if (isexist) :
        connection = getconnection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Loan (Amount, OwnerID, status,DateOfCreation)values(?,?,?,?)",(amountofloan,id,status,day))
        connection.commit()
        loanid = cursor.execute("SELECT ID FROM Loan WHERE Amount = ? AND OwnerID =? AND DateOfCreation = ? AND status =?   ",(amountofloan,id,day,status))
        loanid=loanid.fetchone()
        loanid=loanid.__getattribute__('ID')
        acceptloan(loanid , amountofloan, id)
        connection.close()

def isuserexisit(id):
    connection = getconnection()
    cursor = connection.cursor()
    cursor.execute('SELECT CustomerID,Balance FROM Customers')
    customers = cursor.fetchall()
    for customer in customers:
         if  customer.__getattribute__('CustomerID') == id :
            return  True
    connection.close()
    return False

def checklogin(username,psw):
    connection = getconnection()
    cursor = connection.cursor()
    checkpsw=False
    cursor.execute('SELECT Psw FROM Users Where UserName =? ',username)
    user=cursor.fetchone()
    if user is not None:
       password_hash=user.__getattribute__('Psw')
       checkpsw=check_password_hash(password_hash,psw)
    connection.close()
    return checkpsw

def getuseridbyusername(username):
    connection = getconnection()
    cursor = connection.cursor()
    cursor.execute('SELECT CustomerID FROM Users Where UserName =? ', username)
    user=cursor.fetchone()
    CustomerID=user.__getattribute__('CustomerID')
    connection.close()
    return CustomerID
