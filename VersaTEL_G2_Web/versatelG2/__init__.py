# coding:utf-8
'''
Created on 2020/3/2
@author: Paul
@note: data post
'''

from flask import Flask, Blueprint

from versatelG2.Data import datablue
from versatelG2.Show import showblue
from versatelG2.Interaction import interaction_blue

app = Flask(__name__)

# 将蓝图注册到app
app.register_blueprint(datablue)
app.register_blueprint(showblue)
app.register_blueprint(interaction_blue)
