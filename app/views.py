#!flask/bin/python
from flask import render_template, flash, redirect, session, url_for, \
        request, g, send_file, abort, jsonify 

from flask_login import current_user
from flask_qrcode import QRcode

import requests

from app import app, db, lm
from datetime import datetime
from config import STREAMLABS_CLIENT_ID, STREAMLABS_CLIENT_SECRET

from .forms import RegisterForm
from .models import User

import time
import sys
import qrcode

streamlabs_api_url = 'https://www.twitchalerts.com/api/v1.0/'
api_token = streamlabs_api_url + 'token'
api_user = streamlabs_api_url + 'user'
callback_result = 0


@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Alex' }
    return render_template(
            'index.html',
            user=user)

@app.route('/profile')
def profile():
    return render_template(
            'registerpage.html')

@app.route('/login')
def login():
    if 'nickname' in session:
            return redirect(url_for('profile'))

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
        session['social_id'] = user_access.json()['twitch']['name']
        session['nickname'] = user_access.json()['twitch']['display_name']
        session['access_token'] = a_token
        session['refresh_token'] = r_token

        valid_user = User.query.filter_by(social_id=session['social_id']) \
                .first()
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

@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    form = RegisterForm()
    print form.xpub_field.data

    if 'social_id' in session and request.method == 'POST':
        try:
            new_user = User(
                    streamlabs_atoken = session['access_token'],
                    streamlabs_rtoken = session['refresh_token'],
                    xpub = form.xpub_field.data,
                    social_id = session['social_id'],
                    nickname = session['nickname'],
                    #latest_derivation = 0
            )
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('profile'))
        except Exception,e:
            print str(e)

    try:
        username = session['nickname']
    except KeyError: 
        username = "UNKNOWN USERNAME"

    return render_template(
            'login.html',
            form=form)

@app.route('/register')
def register():
    return "no"

@app.route('/donatecallback', methods=['GET', 'POST'])
def donatecallback():
    print request.args
    return "Hello World!"

@app.route('/tip/<username>')
def tip(username):
    u = User.query.filter_by(social_id=username.lower()).first()
    if u:
        from pycoin.key import Key
        xpub = u.xpub
        deriv = u.latest_derivation
        key = Key.from_text(xpub).subkey(0).subkey(deriv)
        address = key.address(use_uncompressed=False)
        btc_addr = 'bitcoin:' + address

        network,addr_hist = payment_verify(address)

        if addr_hist:
            u.latest_derivation = deriv + 1 
            db.session.commit()

        network.stop()

        return render_template(
                'tip.html',
                btc_addr = address,
                username = u.nickname,
                )
    return abort(404)

@app.route('/_get_unused_address')
def get_unused_address():
    return jsonify(result = 1 + 2)

@app.errorhandler(404)
def handle404(e):
    return "That user or page was not found in our system! " \
            + "Tell them to sign up for CoinStream!"

def payment_verify(btc_addr):
    from electrum import SimpleConfig, Network
    from electrum.util import print_msg, json_encode

    # start network
    c = SimpleConfig()
    network = Network(c)
    network.start()

    # wait until connected
    while network.is_connecting():
        time.sleep(0.1)

    if not network.is_connected():
        print_msg("daemon is not connected")
        sys.exit(1)

    h = network.synchronous_get(('blockchain.address.get_history', [btc_addr]))
    return network,h

