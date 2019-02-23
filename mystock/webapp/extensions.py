# -*- coding: utf-8 -*-
'''
Created on 2016-12-14

@author: Wan
'''
from flask_cache import Cache
from flask_login import LoginManager
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from flask_principal import Principal

cache = Cache()
mail = Mail()
db = MongoEngine()
principal = Principal()

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "account.login"
login_manager.login_message = "Please log in before visiting this page."
login_manager.login_message_category = "info"
