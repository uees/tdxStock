# -*- coding: utf-8 -*-
'''
Created on 2016-12-14

@author: Wan
'''
from datetime import datetime

from flask_login import AnonymousUserMixin, UserMixin
from flask_mongoengine import BaseQuerySet
from flask_principal import Permission, RoleNeed, UserNeed
from werkzeug import cached_property

from webapp.extensions import db, login_manager
from webapp.helper import validate_password
from webapp.permissions import admin

from .option import Option

# ROLES = ('admin', 'moderator', 'auth', 'everyone')

SOCIAL_NETWORKS = {
    'weibo': {'fa_icon': 'fa fa-weibo', 'url': None},
    'weixin': {'fa_icon': 'fa fa-weixin', 'url': None},
    'twitter': {'fa_icon': 'fa fa fa-twitter', 'url': None},
    'github': {'fa_icon': 'fa fa-github', 'url': None},
    'facebook': {'fa_icon': 'fa fa-facebook', 'url': None},
    'linkedin': {'fa_icon': 'fa fa-linkedin', 'url': None},
}


class UserQuery(BaseQuerySet):

    def delete(self, *args, **kwrds):
        super(UserQuery, self).delete(*args, **kwrds)
        Option.objects(name="user_count").update_one(dec__value=1)

    def from_identity(self, identity):
        """
        Loads user from flaskext.principal.Identity instance and
        assigns permissions from user.

        A "user" instance is monkeypatched to the identity instance.

        If no user found then None is returned.
        """

        try:
            user = self.get_by_login(identity.id)
        except ValueError:
            user = None

        return user

    def authenticate(self, login, password):

        user = self.filter(db.Q(login=login) |
                           db.Q(email=login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    def get_by_login(self, login):
        user = self.filter(db.Q(login=login) |
                           db.Q(email=login)).first()
        return user

    def get_by_id(self, id):
        user = self.filter(id=id).first()
        return user

    def search(self, key):
        query = self.filter(db.Q(email__icontains=key) |
                            db.Q(login__icontains=key) |
                            db.Q(name__icontains=key))
        return query


class User(db.Document, UserMixin):
    """ 用户表 """
    login = db.StringField(required=True, unique=True)
    email = db.StringField(max_length=200, default="")
    name = db.StringField(max_length=50, default="")
    display_name = db.StringField(max_length=255, default='Member')
    password = db.StringField(max_length=200, default="")
    code = db.ReferenceField("UserCode")
    open_email = db.BooleanField(default=True)
    url = db.StringField(max_length=200, default="")
    tel = db.StringField(max_length=50, default="")
    social_networks = db.DictField(default=SOCIAL_NETWORKS)
    gender = db.StringField(max_length=50, default="")     # 性别
    position = db.StringField(max_length=50, default="")   # 职位
    address = db.StringField(max_length=200, default="")
    idcard = db.StringField(max_length=50, default="")
    status = db.BooleanField(default=True)
    joined_time = db.DateTimeField(default=datetime.utcnow)
    last_login_time = db.DateTimeField(default=datetime.utcnow)
    activated = db.BooleanField(default=False)
    options = db.DictField()
    roles = db.ListField(db.StringField(max_length=20))
    meta = {
        "queryset_class": UserQuery,
        "indexes": ['login',
                    'email',
                    ('activated', 'login'),
                    ('activated', 'email'),
                    ('activated', 'status')]
    }

    @cached_property
    def edit_permission(self):
        return Permission(UserNeed(self.id)) & admin

    def o_save(self, *args, **kwrds):
        super(User, self).save(*args, **kwrds)
        Option.objects(name="user_count").update_one(inc__value=1)

    def check_password(self, password):
        if self.password is None:
            return False
        return validate_password(password, self.password)

    def is_active(self):
        return self.activated

    def add_role(self, role):
        self.roles.append(role)

    def add_roles(self, roles):
        for role in roles:
            self.add_role(role)

    def get_roles(self):
        for role in self.roles:
            yield role

    @cached_property
    def provides(self):
        needs = [UserNeed(self.id)]

        for role in self.roles:
            needs.append(RoleNeed(role))

        return needs

    def is_role(self, role):
        return role in self.roles

    @cached_property
    def json(self):
        return dict(
            login=self.login,
            display_name=self.display_name,
            name=self.name,
            code=self.code,
            gender=self.gender,
            position=self.position,
            email=self.email if self.open_email else "",
            url=self.url,
            tel=self.tel,
            address=self.address,
            status=self.status,
            idcard=self.idcard,
            joined_time=self.joined_time,
            last_login_time=self.last_login_time,
            activated=self.activated)

    def __str__(self):
        return "%s(name:%s)(email:%s)" % (self.login, self.name, self.email)

    def __repr__(self):
        return "<User: %s>" % self


class UserCode(db.Document):
    '''邀请码'''
    code = db.StringField(max_length=50)
    role = db.StringField(default="reader")
    is_used = db.BooleanField(default=False)
    meta = {
        "indexes": ['code']
    }

    def __str__(self):
        return self.code

    def __repr__(self):
        return "<%s>" % self


class MyAnonymousUser(AnonymousUserMixin):
    roles = ['everyone']


login_manager.anonymous_user = MyAnonymousUser
