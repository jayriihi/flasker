from os import lseek
from flask import Flask, render_template
from sqlalchemy import true

# create flask instance
app = Flask(__name__)

# create a route decorator
@app.route('/')

def index():

    first_name = 'Bruce'
    stuff = "This is <strong>Bold</strong> Text"
    wing_size = ['2', '2.5','3','4','5']
    return render_template('/index.html', first_name = first_name, stuff = stuff, wing_size = wing_size)


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












app.run(debug=true)

