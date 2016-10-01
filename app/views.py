from flask import render_template, flash, redirect, session, url_for, \
        request, g

from app import app
from datetime import datetime

from .forms import RegisterForm
from .models import User

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname':"Amp" }
    return render_template(
            'index.html',
            user=user)

@app.route('/login')
def login():
    '''
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    '''

    form = RegisterForm()

    return render_template(
            'login.html',
            title = 'Login',
            form=form,
            )
