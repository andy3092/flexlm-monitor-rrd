#!/usr/bin/env python2
from getpass import getpass
from flexlm_app import User, db

user = User()

user_name = raw_input('Enter a user name [admin]:')
if user_name == '':
    user_name = 'admin'

user.username = user_name

password1 = getpass('Enter password:')
password2 = getpass('Renter password:')

while password1 != password2:
    print('Passwords do not mtach . Try again.')
    password1 = getpass('Enter password:')
    password2 = getpass('Renter your password:')

user.password = password1

db.session.add(user)
db.session.commit()
