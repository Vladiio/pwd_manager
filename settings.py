import os

import auth

BASE_DIR = os.path.abspath('.')
DATA_ROOT = os.path.join(BASE_DIR, 'data')

KEYRING_FILENAME = os.path.join(DATA_ROOT, '.keyring.dt')

ACTIONS = ('show', 'create', 'remove',
           'modify', 'get_pwd')

USERNAME = 'test'
PASSWORD = '222222'


def setup():
    try:
        auth.authenticator.add_user(USERNAME, PASSWORD)
    except auth.PasswordTooShort:
        print('Please create a user')
        raise SystemExit
    else:
        for action in ACTIONS:
            auth.authorizor.add_permission(action)
            auth.authorizor.permit_user(action, USERNAME)
