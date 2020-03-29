from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

@app.route('/',methods =['POST','GET'])
def index ():
    if(request.method == "POST"):

        sender=request.form['sender']

    else:
        return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)