#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    manage.py
    ~~~~~~~~~~~
    :copyright: 2016 (c) Wan.
"""
from commands import GEventServer, ProfileServer
from datetime import datetime

from flask_script import Manager, Shell, prompt_bool
from flask_script.commands import ShowUrls

from webapp import create_app
from webapp.models.option import Option
from webapp import collection

app = create_app()
manager = Manager(app)
# manager.add_command("runserver", Server('0.0.0.0', port=5000))
manager.add_command("showurls", ShowUrls())
manager.add_command("gevent", GEventServer())
manager.add_command("profile", ProfileServer())


def _make_context():
    return dict(**locals())


manager.add_command("shell", Shell(make_context=_make_context))


@manager.command
def do():
    collection.forecast_data()


@manager.command
def init_stocks():
    from webapp.models.stock import StockBasic
    import tushare as ts
    df = ts.get_stock_basics().reset_index()
    stocks = StockBasic.objects.from_json(df.to_json(orient='records'))
    StockBasic.objects.delete()
    StockBasic.objects.insert(stocks)


@manager.option('-s', '--start', help='start_year', type=int, default=2000)
@manager.option("-e", "--end", help="stop_year", type=int, default=2017)
def collect_with_quarter(start, end):
    collection.collect_with_quarter(start, end)


@manager.option('-s', '--start', help='start_year', type=int, default=2010)
@manager.option("-e", "--end", help="stop_year", type=int, default=2017)
def collect_with_month(start, end):
    collection.collect_with_month(start, end)


@manager.command
def collect_no_args():
    collection.collect_no_args()


@manager.command
def collect_margins():
    # collection.collect_margins()
    # collection.collect_sh_margin_details()
    collection.collect_sz_margin_details()


@manager.command
def collect_profit_data():
    '''[(2004, 807), (2005, 682), (2006, 794), (2007, 938),
       (2008, 930), (2009, 1087), (2010, 1442), (2011, 1731),
       (2012, 1930), (2013, 1969), (2014, 2071), ]'''
    for year, top in [(2015, 2242), (2016, 196)]:
        collection.collect_profit_data(year, top)


@manager.command
def runserver():
    now = datetime.utcnow()
    Option.objects(name="start_time").update_one(set__value=now)
    app.run(host='0.0.0.0', debug=True)


@manager.command
def initdb():
    from webapp.helper import encrypt_password
    from webapp.models.user import User

    # 初始化Option表
    Option.objects.delete()
    Option.objects.insert([Option(name="allow_signup", value="yes",
                                  note="是否允许注册"),
                           Option(name="allow_comment", value="yes",
                                  note="是否允许评论"),
                           Option(name="allow_post", value="yes",
                                  note="是否允许发帖"),
                           Option(name="site_name", value="MYSTOCK",
                                  note="网站名称"),
                           Option(name="site_owner", value="Wan",
                                  note="网站所有者"),
                           Option(name="site_description", value="MYSTOCK SYSTEM",
                                  note="网站描述"),
                           Option(name="post_per_page", value=20,
                                  note="每页大小"),
                           Option(name="comment_per_page", value=50,
                                  note="每页大小"),
                           Option(name='user_count', value=0,
                                  note='用户数量'),
                           Option(name='post_count', value=0,
                                  note='帖子数量'),
                           Option(name='comment_count', value=0,
                                  note='评论数量'),
                           Option(name='tag_count', value=0,
                                  note='Tag数量'),
                           Option(name='start_time', value=datetime.utcnow(),
                                  note='APP启动时间'),
                           Option(name='google_site_verification', value="",
                                  note='google_site_verification'),
                           Option(name='baidu_site_verification', value="",
                                  note='baidu_site_verification'),
                           Option(name='sogou_site_verification', value="",
                                  note='sogou_site_verification'),
                           Option(name='qihu_site_verification', value="",
                                  note='qihu_site_verification'), ])

    # 初始化user表
    User.objects.delete()
    User(login='admin',
         name='管理员',
         email='admin@localhost',
         password=encrypt_password('admin'),
         activated=True,
         roles=['admin', 'moderator', 'authenticated', 'everyone']).save()

    # 修复option数据
    Option.objects(name='user_count').update_one(
        set__value=User.objects.count())


@manager.command
def dropdb():
    "Drops database"
    from pymongo import MongoClient
    client = MongoClient(manager.app.config['MONGODB_SETTINGS']['host'],
                         manager.app.config['MONGODB_SETTINGS']['port'])

    if prompt_bool("Are you sure ? You will lose all your data !"):
        client.drop_database(manager.app.config['MONGODB_SETTINGS']['db'])


if __name__ == "__main__":
    manager.run()
