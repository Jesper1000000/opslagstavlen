from flask import Flask, render_template


# Create Flask's `app` object
app = Flask(__name__)


# Define a route for the default URL, which loads the form
@app.route('/')
@app.route('/index')

def index():
    user = {'username': 'Jesper'}
    return render_template('index.html', title='Home', user=user)

    
    


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(505)
def page_not_found(e):
    return render_template("500.html"), 500