# -*- coding: utf8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'try-and-guess-you-chode'

SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                                       '?check_same_thread=False')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

