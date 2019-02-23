# -*- coding: utf-8 -*-
'''
Created on 2016-08-14

@author: Wan
'''
import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import (Flask, g, jsonify, redirect, render_template, request,
                   url_for, send_from_directory)
from flask_principal import identity_loaded
from flask_wtf.csrf import CsrfProtect

from webapp import helper
from webapp.extensions import cache, db, login_manager, mail, principal


def create_app(config="config.py"):

    app = Flask(__name__)
    app.config.from_pyfile(config)

    load_extensions(app)

    configure_logging(app)
    config_login_manager(app)
    configure_errorhandlers(app)
    configure_handlers(app)
    configure_template_filters(app)
    configure_context_processors(app)

    load_basic_view(app)
    register_blueprints(app)
    # register_api(app)

    return app


def load_basic_view(app):
    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static/images'),
                                   filename='favicon.png',
                                   mimetype='image/vnd.microsoft.icon')

    @app.route("/")
    def index():
        return render_template('index.html')


def register_blueprints(app):
    from webapp.views.classified import classified
    from webapp.views.details import details
    app.register_blueprint(classified, url_prefix='/classified',
                           endpoint='classified')
    app.register_blueprint(details, url_prefix='/details',
                           endpoint='details')


# def register_api(app):
#     from webapp.services.v1 import api
#     api.init_app(app)


def load_extensions(app):
    CsrfProtect(app)
    mail.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)


def config_login_manager(app):
    from webapp.models.user import User

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('account.login'))

    @login_manager.user_loader
    def load_user(user_id):
        user = User.objects.get_by_id(user_id)
        if user and user.is_active():
            return user
        else:
            return None

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Get the user information from the db
        user = User.objects.from_identity(identity)
        # Add the UserNeed to the identity
        if user:
            identity.provides.update(user.provides)

        # Save the user somewhere so we only look it up once
        identity.user = user


def configure_context_processors(app):

    from webapp.models.option import Option
    from webapp.helper import Storage, gravatar, get_quarter_data

    @app.context_processor
    def helper():
        return dict(gravatar=gravatar,
                    get_quarter_data=get_quarter_data)

    @app.context_processor
    def config():
        options = cache.get("options")
        if options is None:
            options = Storage()
            for option in Option.objects.all():
                options[option.name] = option.value
        return dict(config=app.config,
                    options=options)


def configure_template_filters(app):

    @app.template_filter()
    def timesince(value):
        return helper.timesince(value)

    @app.template_filter()
    def endtags(value):
        return helper.endtags(value)

    @app.template_filter()
    def gravatar(email, size):
        return helper.gravatar(email, size)

    @app.template_filter()
    def html2textile(html):
        return helper.html2textile(html)


def configure_handlers(app):

    @app.after_request
    def per_request_callbacks(response):
        for func in getattr(g, 'call_after_request', ()):
            response = func(response)
        return response

    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin',
                             'http://localhost:8080')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers',
                             'Origin, X-Requested-With, Content-Type, Accept')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response
    '''


def configure_errorhandlers(app):

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonify(message="Please login to visit this page.",
                           code=401), 401
        return redirect(url_for("account.login", next=request.path))

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(message='You do not have permission.',
                           code=403), 403
        return render_template("errors/403.html", error=error), 403

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(message='The page can not be found.',
                           code=404), 404
        return render_template("errors/404.html", error=error), 404

    @app.errorhandler(500)
    def server_error(error):
        import traceback
        app.logger.error(traceback.format_exc())
        if request.is_xhr:
            return jsonify(message='Internal server error.',
                           code=500), 500
        return render_template("errors/500.html", error=error), 500


def configure_logging(app):

    from datetime import date
    today = date.today().strftime("%d %m %Y")
    mail_handler = SMTPHandler(mailhost=app.config['MAIL_SERVER'],
                               fromaddr=app.config['DEFAULT_MAIL_SENDER'],
                               toaddrs=app.config['LOG_MAILS'],
                               subject='application error -- %s' % today,
                               credentials=(app.config['MAIL_USERNAME'],
                                            app.config['MAIL_PASSWORD'])
                               )

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s

    Message:

    %(message)s
    '''))
    app.logger.addHandler(mail_handler)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    debug_logfile = os.path.join(app.root_path, app.config['DEBUG_LOG'])

    debug_file_handler = RotatingFileHandler(filename=debug_logfile,
                                             maxBytes=512000,
                                             backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_logfile = os.path.join(app.root_path, app.config['ERROR_LOG'])

    error_file_handler = RotatingFileHandler(filename=error_logfile,
                                             maxBytes=512000,
                                             backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)


def after_this_request(func):
    if not hasattr(g, 'call_after_request'):
        g.call_after_request = []
    g.call_after_request.append(func)
    return func
