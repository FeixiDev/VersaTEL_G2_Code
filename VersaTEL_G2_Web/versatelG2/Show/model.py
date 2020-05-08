
# coding:utf-8
'''
Created on 2020/3/2
@author: Paul
@note: data
'''

from flask import Flask, render_template, views


class indexView(views.MethodView):
    def get(self):
        return render_template("index.html")
    
class iSCSIcreateView(views.MethodView):
    def get(self):
        return render_template("iSCSI_create.html")

class LINSTORcreateView(views.MethodView):
    def get(self):
        return render_template("LINSTOR_create.html")

class showView(views.MethodView):
    def get(self):
        return render_template("show.html")

class NodeView(views.MethodView):
    def get(self):
        return render_template("Node.html")
    
class ResourceView(views.MethodView):
    def get(self):
        return render_template("Resource.html")
    
class StoragePoolView(views.MethodView):
    def get(self):
        return render_template("StoragePool.html")
    
class iSCSIShowView(views.MethodView):
    def get(self):
        return render_template("iSCSI_Show.html")
    
    
    
    
    