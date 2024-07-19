from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Create Flask's `app` object
app = Flask(__name__)
# add database 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # Old SQL Lite
# MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost/users'
# secret key
app.config['SECRET_KEY'] = "super secret key"
# initialize the database
db = SQLAlchemy(app)

# Define the model Users with columns name, email and date_added
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now())

    # Create a string
    def __repr__(self) -> str:
        return '<Name %r>' % self.name

# Create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a form class
class NamerForum(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Define a route for the default URL, which loads the form
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jesper'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Jesper'},
            'body': 'I love my dog!'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# 
@app.errorhandler(505)
def page_not_found(e):
    return render_template("500.html"), 500

@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForum()

    # Validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submitted succesfully")

    return render_template('name.html',
                           name = name,
                           form = form)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    
    if form.validate_on_submit():

        user = Users.query.filter_by(email=form.email.data).first()
        if user is None: 
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        
        flash("User added succesfully")

    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
                           name=name,
                           form=form,
                           our_users=our_users)