# coding:utf-8
'''
Created on 2020/3/2
@author: Paul
@note: data
'''

from flask import Flask,views
from versatelG2.Show import showblue
from versatelG2.Show import model

showblue.add_url_rule('/', view_func=model.indexView.as_view('indexview'))
showblue.add_url_rule('/iSCSI_create', view_func=model.iSCSIcreateView.as_view('iSCSIcreateview'))
showblue.add_url_rule('/LINSTOR_create', view_func=model.LINSTORcreateView.as_view('LINSTORcreateview'))
showblue.add_url_rule('/show', view_func=model.showView.as_view('showview'))
showblue.add_url_rule('/Node', view_func=model.NodeView.as_view('Nodeview'))
showblue.add_url_rule('/Resource', view_func=model.ResourceView.as_view('Resourceview'))
showblue.add_url_rule('/StoragePool', view_func=model.StoragePoolView.as_view('StoragePoolview'))
showblue.add_url_rule('/iSCSIShow', view_func=model.iSCSIShowView.as_view('iSCSIShowview'))




