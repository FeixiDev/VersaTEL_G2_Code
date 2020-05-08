# coding:utf-8

from flask import Flask,Blueprint

interaction_blue = Blueprint("interaction_blue", __name__)

from versatelG2.Interaction import views
# from . import views