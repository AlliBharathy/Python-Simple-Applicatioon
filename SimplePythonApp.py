from flask import Flask,render_template,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/address_book'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/address'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return render_template('addUser.html',users=Users.query.all())

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(20))

    def __init__(self, name,mobile, email):
        self.name = name
        self.mobile = mobile
        self.email = email

    @app.route('/viewContacts')
    def viewContacts():
        return render_template('addUser.html', users=Users.query.all())


    @app.route('/new', methods=['GET', 'POST'])
    def new():
        if request.method == 'POST':
            if not request.form['name'] or not request.form['pnumber'] or not request.form['email']:
                flash('Please enter all the fields', 'error')
            else:
                user = Users(request.form['name'],
                             request.form['pnumber'], request.form['email'])
                db.session.add(user)
                db.session.commit()
                flash('Record was successfully added')
            return redirect(url_for('viewContacts'))
        return render_template('addUser.html')

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        shutdown_server()
        return 'Server shutting down...'


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.run()
