from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from datetime import datetime

# Create Flask's `app` object
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # Old SQL Lite
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost/users'

# secret key needed. 
app.config['SECRET_KEY'] = "super secret key"

# initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the model Users with columns name, email and date_added
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(120))
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now())

    # Create a string 
    def __repr__(self) -> str:
        return '<Name %r>' % self.name

# Create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    city = StringField('city')
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
            user = Users(name=form.name.data, email=form.email.data, city=form.city.data)
            db.session.add(user)
            db.session.commit()
        
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.city.data = ''
        
        flash("User added successfully")

    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
                           name=name,
                           form=form,
                           our_users=our_users)

@app.route('/delete/<int:id>' , methods=['GET', 'POST'])
def delete(id):

    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully")
        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html', name=name,
                           form=form,
                           our_users=our_users)

    except:
        flash("Error! Couldn't delete user, try again.")
        return render_template("update.html",
                                form=form,
                                name=name,
                                name_to_update=user_to_delete)



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.city = request.form['city']
        try: 
            db.session.commit()
            flash('User is updated successfully')
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
        except:
            flash('Error! Looks like there was a problem - try again')
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template("update.html",
                        form=form,
                        name_to_update=name_to_update,
                        id = id)