from flask import render_template, flash, redirect, session, url_for, \
        request, g, send_file

from flask_login import current_user
from flask_qrcode import QRcode

import requests

from app import app, db, lm
from datetime import datetime
from config import STREAMLABS_CLIENT_ID, STREAMLABS_CLIENT_SECRET

from .forms import RegisterForm
from .models import User

import time
import qrcode

streamlabs_api_url = 'https://www.twitchalerts.com/api/v1.0/'
api_token = streamlabs_api_url + 'token'
api_user = streamlabs_api_url + 'user'


@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Alex' }
    return render_template(
            'index.html',
            user=user)

@app.route('/profile')
def profile():
    return "You are logged in!" + session['social_id']

@app.route('/login')
def login():
    if request.args.get('code'):
        session.clear()
        authorize_call = {
                'grant_type'    : 'authorization_code',
                'client_id'     : STREAMLABS_CLIENT_ID,
                'client_secret' : STREAMLABS_CLIENT_SECRET,
                'code'          : request.args.get('code'),
                'redirect_uri'  : 'http://coinstream.co:5000/login'
        }

        headers = []

        token_response = requests.post(
                api_token, 
                data=authorize_call, 
                headers=headers
        )

        token_data = token_response.json()

        a_token = token_data['access_token']
        r_token = token_data['refresh_token']

        user_get_call = {
                'access_token' : a_token
        }

        user_access = requests.get(api_user, params=user_get_call)

        session.clear()
        session['social_id'] = user_access.json()['twitch']['display_name']
        session['nickname'] = user_access.json()['twitch']['name']
        session['access_token'] = a_token
        session['refresh_token'] = r_token

        valid_user = User.query.filter_by(social_id=session['social_id']).first()
        if valid_user:
            valid_user.streamlabs_atoken = a_token
            valid_user.streamlabs_rtoken = r_token
            db.session.commit()
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('newuser'))

    return redirect(
            "http://www.twitchalerts.com/api/v1.0/authorize?client_id=" +
            STREAMLABS_CLIENT_ID +
            "&redirect_uri=http://coinstream.co:5000/login" +
            "&response_type=code" +
            "&scope=donations.read+donations.create", code=302
    )

@app.route('/newuser')
def newuser():
    try:
        new_user = User(
                streamlabs_atoken = session['access_token'],
                streamlabs_rtoken = session['refresh_token'],
                fiat= "USD",
                unit= "B",
                addr= "xpub6D4WvHcJsEdLjsbB3ot18dxHv7morZP9bBZ82Rjgb5FbpwqFtjSjywAryoTvZYgNWH3JTRWjn32sPSwWfyhZqk12VYtXPgHtyzub7NpCy1Q",
                social_id = session['social_id'],
                nickname = session['nickname']
        )
        db.session.add(new_user)
        db.session.commit()
    except:
        print "Whoops!"

    try:
        username = session['nickname']
    except KeyError: 
        username = "UNKNOWN USERNAME"

    return "Well hey there " + username + ". Unfortunately we " \
            + "haven't quite finished the registration page yet! Please let " \
            + "Amp know what you see here! Especially whether we got your " \
            + "name right! You look like a new user! Hope you enjoy!"

    


@app.route('/callback2', methods=['GET', 'POST'])
def callback2():
    if request.method == 'POST':
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
    return "no"

@app.route('/donatecallback', methods=['GET', 'POST'])
def donatecallback():
    print request.args
    return "Hello World!"

@app.route('/tip/<username>')
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
