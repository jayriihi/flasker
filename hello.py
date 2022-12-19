from os import lseek
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from sqlalchemy import true
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash



# create flask instance
app = Flask(__name__)

# create a string 
def __repr__(self):
    return '<Name %r>' % self.name

# old sqlite database
#app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#new mysql database
app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password123@localhost/our_users'

# secret key!
app.config['SECRET_KEY'] = "my secret key"
# initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    wing_brand = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


    

# create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators= [DataRequired()])
    email = StringField("Email", validators= [DataRequired()])
    wing_brand = StringField("Wing Brand")
    submit = SubmitField("Submit")

# create a form class
class NamerForm(FlaskForm):
    name = StringField("what's your name", validators= [DataRequired()])
    submit = SubmitField("Submit")

# create a route decorator
@app.route('/')
def index():

    first_name = 'Bruce'
    stuff = "This is <strong>Bold</strong> Text"
    wing_size = ['2', '2.5','3','4','5']
    return render_template('/index.html', first_name = first_name, stuff = stuff, wing_size = wing_size)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, wing_brand=form.wing_brand.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.wing_brand.data = ''
        flash("User Added Successfully!")

    our_users = Users.query.order_by(Users.date_added)


    return render_template('/add_user.html', form=form, name=name, our_users=our_users)

@app.route('/update/<int:id>', methods= ['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.wing_brand = request.form['wing_brand']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("/update.html", 
                form=form, 
                name_to_update=name_to_update,
                id=id)
        except:
            flash("Error looks like an issue, try again!")
            return render_template("/update.html", 
                form=form, 
                name_to_update=name_to_update)
    else:
        return render_template("/update.html", 
            form=form, 
            name_to_update=name_to_update,
            id = id)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")

        our_users = Users.query.order_by(Users.date_added)

        return render_template('/add_user.html', 
        form=form, 
        name=name, 
        our_users=our_users)

    

    except:
        flash("Whoops, try again!")
        return render_template('/add_user.html', 
        form=form, 
        name=name, 
        our_users=our_users)





# localhost:5000/user/Susan
@app.route('/user/<name>')
def user(name):
    return render_template('/user.html', user_name=name)

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('/404.html'), 404

# Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('/500.html'), 500

# create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
# validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submitted successfully")

    return render_template('/name.html', name = name, form = form)


app.run(debug=true)

