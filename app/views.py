from flask import render_template, flash, redirect, session, url_for, \
        request, g

import requests as req

from app import app
from datetime import datetime
from config import STREAMLABS_CLIENT_ID, STREAMLABS_CLIENT_SECRET

from .forms import RegisterForm
from .models import User

streamlabs_api_url = 'https://www.twitchalerts.com/api/v1.0/'

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

@app.route('/sl_authorize')
def sl_authorize():
    token = streamlabs_api_url + 'token'

    sl_authorize_code = request.args.get('code')


    tipcall = {
                'grant_type'    : 'authorization_code',
                'client_id'     : STREAMLABS_CLIENT_ID,
                'client_secret' : STREAMLABS_CLIENT_SECRET,
                'code'          : sl_authorize_code,
                'redirect_uri'  : 'http://cs.amperture.com:5000/sl_authorize'
    }
    headers = []
    print token

    check = req.post(token, data=tipcall, headers=headers).json()
    print "Hello!"
    print check
    print "World!"

    return "Hello World!"


