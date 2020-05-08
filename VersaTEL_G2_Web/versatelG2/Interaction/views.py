# coding:utf-8

from flask import views
from versatelG2.Interaction import interaction_blue
from versatelG2.Interaction import model

interaction_blue.add_url_rule('/send_message', view_func=model.sendmessageView.as_view('sendmessageview'))
interaction_blue.add_url_rule('/LINSTOR_message', view_func=model.LINSTORmessageView.as_view('LINSTORmessageview'))
