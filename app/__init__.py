from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
QRcode(app)
Bootstrap(app)

from app import views, models
