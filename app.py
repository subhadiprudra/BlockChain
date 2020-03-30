from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import base64

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db= SQLAlchemy(app)



class Todo(db.Model):
    id= db.Column(db.Integer , primary_key=True)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.Column(db.String(200), nullable=False)
    receiver = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.String(200), nullable=False)
    hash=db.Column(db.String(200), nullable=False)


    def __repr__(self):
        return '<Task %r>' % self.id

def make_hash(item):

    encodedBytes = base64.b64encode((item.sender+item.receiver+item.amount+item.hash).encode("utf-8"))
    encodedStr = str(encodedBytes)
    encodedBytes = base64.b64encode(encodedStr.encode("utf-8"))
    return str(encodedBytes)


def getLastHash():
    list= Todo.query.order_by(Todo.date_created).all()


    try:

       return make_hash(list[-1])

    except:
        firstObject = Todo(sender="default",receiver="default",amount="default",hash="default")
        try:
            db.session.add(firstObject)
            db.session.commit()
            getLastHash()

        except:
            return "there was an error"

def deleteAll():
    list = Todo.query.order_by(Todo.date_created).all()
    print list[0]
    for i in list:

        try:

            db.session.delete(i)
            db.session.commit()
            print ("deleted")

        except:
            print ("error")


def isNotBroken():
    list = Todo.query.order_by(Todo.date_created).all()
    i=0

    for x in range (len(list)-1):
        if(list[x+1].hash==make_hash(list[x])):
            print ("ok")
        else:
            i=1
            break
    print (x)

    if(i==0):
        return True
    else:
        return False


def makeChange():
    list = Todo.query.order_by(Todo.date_created).all()

    list[1].sender = "hibn"
    db.session.commit()


@app.route('/',methods =['POST','GET'])
def index ():


    if(request.method == "POST"):

        sender=request.form['sender']
        receiver = request.form['receiver']
        amount = request.form['amount']

        try:
            int(amount)
        except:
            return ("Amount must be an integer")





        item= Todo(sender=sender,receiver=receiver,amount=amount,hash=getLastHash())


        try:
            db.session.add(item)
            db.session.commit()

            list = Todo.query.order_by(Todo.date_created).all()

            for i in list:
                print (i.sender + "\n" +i.receiver +"\n" +i.amount+"\n" +i.hash+"\n\n")


            return redirect("/")

        except:
            return "there was an error"

    else:
        return render_template('index.html')

@app.route('/all_transaction',methods =['POST','GET'])
def all_transaction():

    try:
        if(isNotBroken()):

            datas=Todo.query.order_by(Todo.date_created).all()
            del datas[0]
            return render_template("all_transaction.html", datas=datas)


        else:
            return ("Blockchain is broken")

    except:
        return ("No transaction found")



if __name__ == "__main__":
    app.run(debug=True)

