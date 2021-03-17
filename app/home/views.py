from flask import render_template
from . import home_blue

@home_blue.route('/')
def index():
    return render_template('home/index/index.html')