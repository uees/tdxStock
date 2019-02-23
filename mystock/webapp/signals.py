# coding=utf-8
'''
Created on 2016-12-14

@author: Wan
'''

from blinker import Namespace

signals = Namespace()

comment_added = signals.signal("comment-added")
comment_deleted = signals.signal("comment-deleted")
