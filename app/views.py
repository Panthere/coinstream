from flask import render_template, flash, redirect, session, url_for, \
        request, g

from flask_login import current_user

import requests

from app import app, db
from datetime import datetime
from config import STREAMLABS_CLIENT_ID, STREAMLABS_CLIENT_SECRET

from .forms import RegisterForm
from .models import User

import time

streamlabs_api_url = 'https://www.twitchalerts.com/api/v1.0/'

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Alex' }
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

@app.route('/sl_callback')
def sl_authorize():
    api_token = streamlabs_api_url + 'token'
    api_user = streamlabs_api_url + 'user'

    sl_authorize_code = request.args.get('code')


    tipcall = {
            'grant_type'    : 'authorization_code',
            'client_id'     : STREAMLABS_CLIENT_ID,
            'client_secret' : STREAMLABS_CLIENT_SECRET,
            'code'          : sl_authorize_code,
            'redirect_uri'  : 'http://cs.amperture.com:5000/sl_callback'
    }

    headers = []

    token_response = requests.post(
            api_token, 
            data=tipcall, 
            headers=headers
    )
    token_data = token_response.json()

    a_token = token_data['access_token']
    r_token = token_data['refresh_token']

    user_get_call = {
            'access_token' : a_token
    }

    print a_token
    user_access = requests.get(api_user, params=user_get_call)

    print user_access.json()
    

    return redirect(
            url_for(
                'callback2', 
                a_token=a_token,
                r_token=r_token
            )
    )

@app.route('/callback2')
def callback2():
    a_token = request.args.get('a_token')
    r_token = request.args.get('r_token')

    new_user = User(
            streamlabs_atoken = a_token,
            streamlabs_rtoken = r_token,
            #TODO:Make forms ready
            fiat= 'USD',
            unit= 'u',
            addr= '1EnMhjCgoyVvhiN1SmeTYQgFgy1YZ5zEuj',
            social_id = 'Amp',
            nickname = 'Amp'

    )
    '''
    db.session.add(new_user)
    db.session.commit()
    '''

    return redirect(url_for('index'))

@app.route('/register')
def register():
    return redirect(
            "http://www.twitchalerts.com/api/v1.0/authorize?client_id=" +
            STREAMLABS_CLIENT_ID +
            "&redirect_uri=http://cs.amperture.com:5000/sl_callback" +
            "&response_type=code" +
            "&scope=donations.read+donations.create", code=302
    )
