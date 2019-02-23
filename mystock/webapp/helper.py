# -*- coding: utf-8 -*-
'''
Created on 2016-12-14

@author: Wan
'''
import binascii
import functools
import hashlib
import hmac
import os
import random
import re
import socket
import struct
import sys
from html.parser import HTMLParser
from math import ceil
from traceback import print_exc
from urllib.parse import urlparse

import markdown
from pandas import isnull
from pypinyin import lazy_pinyin

markdown = functools.partial(markdown.markdown,
                             safe_mode='remove',
                             output_format="html")


def get_quarter_data(df, field, year, quarter):

    result = df.loc[(df.year == year) & (df.quarter == quarter), field]

    value = ''
    if result.size:
        value = result.iat[0]

    if isnull(value):
        value = ''

    if value == "--":
        value = ''

    return value


def get_at_users(comment):
    '''返回@标识的User'''
    users = re.findall(r'@([\u4e00-\u9fa5\w\-]+)', comment)
    return users


def setting_from_object(obj):
    '''从object对象提取配置'''
    settings = dict()
    for key in dir(obj):
        if key.isupper():
            settings[key.lower()] = getattr(obj, key)
    return settings


def ip2long(ip):
    '''ip转为long型'''
    return struct.unpack("!I", socket.inet_aton(ip))[0]


def long2ip(num):
    '''long型转为ip'''
    return socket.inet_ntoa(struct.pack("!I", num))


def domain(url):
    """ Returns the domain of a URL
    e.g. http://reddit.com/ > reddit.com
    """
    rv = urlparse(url).netloc
    if rv.startswith("www."):
        rv = rv[4:]
    return rv


def endtags(html):
    """ close all open html tags at the end of the string """

    NON_CLOSING_TAGS = ['AREA', 'BASE', 'BASEFONT', 'BR', 'COL',
                        'FRAME', 'HR', 'IMG', 'INPUT', 'ISINDEX',
                        'LINK', 'META', 'PARAM']

    opened_tags = re.findall(r"<([a-z]+)[^<>]*>", html)
    closed_tags = re.findall(r"</([a-z]+)>", html)

    opened_tags = [i.lower()
                   for i in opened_tags if i.upper() not in NON_CLOSING_TAGS]
    closed_tags = [i.lower() for i in closed_tags]

    len_opened = len(opened_tags)

    if len_opened == len(closed_tags):
        return html

    opened_tags.reverse()

    for tag in opened_tags:
        if tag in closed_tags:
            closed_tags.remove(tag)
        else:
            html += "</%s>" % tag

    return html


def dehtml(text):
    '''去除html标识'''
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=sys.stderr)
        return text


def html2textile(html):
    '''just dehtml'''
    return dehtml(html)


def get_all_files(dir_path):
    ''' 递归获取文件夹下所有的文件 '''
    files = list()
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            files.extend(get_all_files(item_path))
        else:
            files.append(item_path)
    return files


def slugify(text, delim='-'):
    '''转换为slug'''
    result = []
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    for word in _punct_re.split(text.lower()):
        if word:
            result.extend(lazy_pinyin(word))
    return delim.join(result)


def safe(text):
    """ 过滤不安全字符 """
    if text is None:
        text = ""
    unsafe_re = re.compile(r"[&\"'=!+#*~;\^()<>\[\]]")
    return unsafe_re.sub("", text)


def rnd_numberstring(length=8):
    """Generate random number string."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


def rnd_string(length=8):
    """Generate random string."""
    return ''.join([rnd_char() for i in range(length)])


def rnd_char():
    ''' 随机字母 '''
    return chr(random.randint(65, 90))


def is_chinese(text):
    '''判断是否中文字符'''
    if text:
        for uchar in text:
            if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
                return True
    return False


def is_number(value):
    '''判断是否为数字'''
    try:
        value + 1
    except TypeError:
        return False
    else:
        return True


def is_number_str(value):
    '''判断是否为数字字符串'''
    try:
        int(value)
    except:
        return False
    else:
        return True


def encrypt_password(password, salt=None):
    """ Hash password, return bytes object """
    if salt is None:
        salt = os.urandom(8)
    # assert isinstance(salt, bytes)
    result = password.encode('utf-8')  # str 转 bytes
    for i in range(10):
        result = hmac.HMAC(result, salt, hashlib.sha256).digest()
    return binascii.hexlify(salt + result).decode('utf-8')  # bytes 转 str


def validate_password(input_password, hashed):
    """验证密码"""
    salt = binascii.unhexlify(hashed.encode('utf-8'))[:8]
    return encrypt_password(input_password, salt=salt) == hashed


class _DeHTMLParser(HTMLParser):
    '''HTML Parser'''

    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = re.sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.
    >>> o = storage(a=1)
    >>> o.a
    1
    >>> o['a']
    1
    >>> o.a = 2
    >>> o['a']
    2
    >>> del o.a
    >>> o.a
    Traceback (most recent call last):
    ...
    AttributeError: 'a'
    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'


storage = Storage


class Gravatar(object):
    """
    Simple object for create gravatar link.
    gravatar = Gravatar(
        size=100,
        rating='g',
        default='retro',
        force_default=False,
        force_lower=False
    )
    :param app: Your Flask app instance
    :param size: Default size for avatar
    :param rating: Default rating
    :param default: Default type for unregistred emails
    :param force_default: Build only default avatars
    :param force_lower: Make email.lower() before build link
    From flask-gravatar http://packages.python.org/Flask-Gravatar/
    """

    def __init__(self, size=100, rating='g', default='mm',
                 force_default=False, force_lower=False):

        self.size = size
        self.rating = rating
        self.default = default
        self.force_default = force_default
        self.force_lower = force_lower

    def __call__(self, email, size=None, rating=None, default=None,
                 force_default=None, force_lower=False):
        """Build gravatar link."""

        if size is None:
            size = self.size

        if rating is None:
            rating = self.rating

        if default is None:
            default = self.default

        if force_default is None:
            force_default = self.force_default

        if force_lower is None:
            force_lower = self.force_lower

        if force_lower:
            email = email.lower()

        hash = hashlib.md5(email.lower().encode("utf8")).hexdigest()

        link = 'http://www.gravatar.com/avatar/{hash}'\
               '?s={size}&d={default}&r={rating}'.format(**locals())

        if force_default:
            link = link + '&f=y'

        return link


gravatar = Gravatar()


class Pagination(object):
    '''http://flask.pocoo.org/snippets/44/'''

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
