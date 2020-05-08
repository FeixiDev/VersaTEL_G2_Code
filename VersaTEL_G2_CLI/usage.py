#coding:utf-8

#stor部分使用手册
stor = '''
stor {node(n)/resource(r)/storagepool(sp)/snap(sn)}'''

#node部分使用手册
node = '''
node(n) {create(c)/modify(m)/delete(d)/show(s)}'''

node_create = '''
node(n) create(c) NODE -ip IP -nt NODETYPE'''

node_delete ='''
node(n) delete(d) NODE'''

#待完善
node_modify ='''
node(n) modify(m) NODE ...'''

node_show ='''
node(n) show(s) [NODE]'''

#storagepool部分使用手册
resource = '''
resource(r) {create(c)/modify(m)/delete(d)/show(s)}'''

resource_create = '''
resource(r) create(c) RESOURCE -s SIZE -n NODE[NODE...] -sp STORAGEPOOL[STORAGEPOOL...]
                      RESOURCE -s SIZE -a -num NUM
                      RESOURCE -dikless -n NODE[NODE...]
                      RESOURCE -am -n NODE[NODE...] -sp STORAGEPOOL[STORAGEPOOL...]
                      RESOURCE -am -a -num NUM'''

resource_delete ='''
resource(r) delete(d) RESOURCE [-n NODE]'''

#待完善
resource_modify ='''
resource(r) modify(m) RESOURCE ...'''

resource_show ='''
resource(r) show(s) [RESOURCE]'''




#storagepool部分使用手册
storagepool = '''
storagepool(sp) {create(c)/modify(m)/delete(d)/show(s)}'''

storagepool_create = '''
storagepool(sp) create(c) STORAGEPOOL -n NODE -lvm LVM/-tlv THINLV'''

storagepool_delete ='''
storagepool(sp) delete(d) STORAGEPOOL -n NODE'''

#待完善
storagepool_modify ='''
storagepool(sp) modify(m) STORAGEPOOL ...'''

storagepool_show ='''
storagepool(sp) show(s) [STORAGEPOOL]'''




