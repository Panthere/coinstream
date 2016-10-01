from flask import render_template, flash, redirect, session, url_for, \
        request, g

import requests as req

from app import app, db
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

    token_data = req.post(token, data=tipcall, headers=headers).json()
    a_token = token_data['access_token']
    r_token = token_data['refresh_token']

    return redirect(
            url_for(
                'register', 
                a_token=a_token,
                r_token=r_token
            )
    )

@app.route('/register')
def register():
    a_token = request.args.get('a_token')
    r_token = request.args.get('r_token')

    new_user = User(
            streamlabs_atoken = a_token,
            streamlabs_rtoken = r_token,
            #TODO:Make forms ready
            fiat= 'USD',
            unit= 'u',
            addr= '1EnMhjCgoyVvhiN1SmeTYQgFgy1YZ5zEuj'
    )
    db.session.add(new_user)
    db.session.commit()

    return "Register Page"

