# coding: utf-8
'''
Created on 2016-12-14

@author: Wan
'''
from flask_principal import Permission, RoleNeed

admin = Permission(RoleNeed('admin'))
moderator = Permission(RoleNeed('moderator')).union(admin)
auth = Permission(RoleNeed('authenticated')).union(moderator)
everyone = Permission(RoleNeed('everyone')).union(auth)
