# -*- coding: utf-8 -*-
# @Date    : 2015-11-03 14:26:37
# @Author  : Rafael Fernandes (basask@collabo.com.br)
# @Link    : http://www.collabo.com.br/

from __future__ import unicode_literals

SECRET_KEY = 'nosecret'

INSTALLED_APPS = [
    "tests",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
