from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
QRcode(app)

from app import views, models
