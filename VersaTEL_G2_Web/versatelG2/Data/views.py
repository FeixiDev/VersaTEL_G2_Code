# coding:utf-8
'''
Created on 2020/3/2
@author: Paul
@note: data
'''

from flask import views
from versatelG2.Data import datablue
from versatelG2.Data import model



datablue.add_url_rule('/node', view_func=model.nodeView.as_view('nodeview'))
datablue.add_url_rule('/resource', view_func=model.resourceView.as_view('resourceview'))
datablue.add_url_rule('/storagepool', view_func=model.storagepoolView.as_view('storagepoolview'))
datablue.add_url_rule('/configuration_data', view_func=model.iSCSIView.as_view('iSCSIview'))
datablue.add_url_rule('/socket', view_func=model.LINSTORView.as_view('LINSTORview'))
datablue.add_url_rule('/lvm', view_func=model.lvmView.as_view('lvmview'))
datablue.add_url_rule('/sp', view_func=model.spView.as_view('spview'))
datablue.add_url_rule('/node_create', view_func=model.nodecreateView.as_view('nodecreateview'))
datablue.add_url_rule('/node_num', view_func=model.nodenumView.as_view('nodenumview'))

 