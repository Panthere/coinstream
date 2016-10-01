from hashlib import md5

from app import ap, db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # fiat currency user desires conversion to, ISO 4217 currencies accepted
    # e.g. "USD", "GBP", "EUR", etc.
    fiat = db.Column(db.String(3))

    # either 'B' for BTC, 'm' for mBTC, or 'u' for uBTC/bits
    unit = db.Column(db.String(1)) 

    # streamlabs tokens, retreived from streamlabs authorization
    streamlabs_atoken = db.Column(db.String(40))
    streamlabs_rtoken = db.Column(db.String(40))

    # Bitcoin Address
    addr = db.Column(db.String(34))

    #BIP32 Extended Public Key
    xpub = db.Column(db.String(111))

    # Transaction Linkage
    transactions = db.relationship(
            "Transaction",
            backref='user',
            lazy='dynamic')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tx_id = db.Column(db.String(64), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime)

    # Amount in BTC
    amount = db.Column(db.Float)

    # derivation path for xpub keys
    # derivpath = db.Column(db.String(16)) 

    twi_user = db.Column(db.String(25))
    twi_message = db.Column(db.String(255))

