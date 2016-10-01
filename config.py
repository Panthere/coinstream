# -*- coding: utf8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'try-and-guess-you-chode'

# Streamlabs Keys, These are only for the testapp, replace when in production
STREAMLABS_CLIENT_ID = 'JD8Mwed8eJ1S1LgwqfCSCccbSKGtsr0FuVfk35Gw'
STREAMLABS_CLIENT_SECRET = 'IrLNl9zYTu5MQwUUQqsC9KGfyC31RtzdPThQ0gyU'

SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                                       '?check_same_thread=False')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

