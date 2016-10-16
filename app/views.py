from flask import render_template, flash, redirect, session, url_for, \
        request, g, send_file

from flask_login import current_user
from flask_qrcode import QRcode

import requests

from app import app, db
from datetime import datetime
from config import STREAMLABS_CLIENT_ID, STREAMLABS_CLIENT_SECRET

from .forms import RegisterForm
from .models import User

import time
import qrcode

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

    user_access = requests.get(api_user, params=user_get_call)

    session['twitch_name'] = user_access.json()['twitch']['name']
    session['twitch_display'] = user_access.json()['twitch']['display_name']
    session['access_token'] = a_token
    session['refresh_token'] = r_token
    

    return redirect(
            url_for(
                'callback2', 
            )
    )

@app.route('/callback2', methods=['GET', 'POST'])
def callback2():

    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
                streamlabs_atoken = session['access_token'],
                streamlabs_rtoken = session['refresh_token'],
                fiat= form.fiat_field.data,
                unit= form.unit_field.data,
                addr= form.addr_field.data,
                social_id = session['twitch_display'],
                nickname = session['twitch_name']

        )
        db.session.add(new_user)
        db.session.commit()

    return render_template(
            'login.html',
            title = 'Login',
            form=form,
            )

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

@app.route('/donatecallback', methods=['GET', 'POST'])
def donatecallback():
    print request.args
    return "Hello World!"

@app.route('/tip')
def tip():
    from pycoin.key import Key
    test_xpub = 'xpub6D4WvHcJsEdLjsbB3ot18dxHv7morZP9bBZ82Rjgb5FbpwqFtjSjywAryoTvZYgNWH3JTRWjn32sPSwWfyhZqk12VYtXPgHtyzub7NpCy1Q'
    key = Key.from_text(test_xpub).subkey(0).subkey(0)
    address = key.address(use_uncompressed=False)
    btc_addr = 'bitcoin:' + address

    print btc_addr

    return render_template(
            'tip.html',
            btc_addr = btc_addr)
