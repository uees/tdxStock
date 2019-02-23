# -*- coding: utf-8 -*-
'''
Created on 2016-12-14

@author: Wan
'''
from webapp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
