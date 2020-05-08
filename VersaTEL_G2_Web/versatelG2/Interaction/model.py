# coding:utf-8
from flask import views
import VersaTELSocket as vst

class sendmessageView(views.MethodView):
    def get(self):
        Host_create = ['Host_Name', 'Host_iqn']
        HostGroup_create = ['HostGroup_Name', 'Host']
        DiskGroup_create = ['DiskGroup_Name', 'Disk']
        Map_create = ['Map_Name', 'Disk_Group', 'Host_Group']
        data = {}

        if request.method == 'GET':
            data_all = request.args.items()
            for i in data_all:
                data_one_dict = {i[0]:i[1]}
                data.update(data_one_dict)
            for i in  data.keys():
                if i in Host_create:
                    str_cmd = "python3 vtel.py iscsi host create %s %s -gui gui" % (data["Host_Name"], data["Host_iqn"])
                    str_cmd = str_cmd.encode()
                    CLI_result = vst.conn(str_cmd)
                    break
                elif i in HostGroup_create:
                    hostgroup = data['Host'].replace(',',' ')
                    str_cmd = "python3 vtel.py iscsi hostgroup create %s %s -gui gui" % (data["HostGroup_Name"], hostgroup)
                    str_cmd = str_cmd.encode()
                    CLI_result = vst.conn(str_cmd)
                    break
                elif i in DiskGroup_create:
                    diskgroup = data['Disk'].replace(',',' ')
                    str_cmd = "python3 vtel.py iscsi diskgroup create %s %s -gui gui" % (data["DiskGroup_Name"], diskgroup)
                    str_cmd = str_cmd.encode()
                    CLI_result = vst.conn(str_cmd)
                    break
                elif i in Map_create:
                    str_cmd = "python3 vtel.py iscsi map create %s -hg %s -dg %s -gui gui" % (data["Map_Name"], data["Host_Group"], data["Disk_Group"])
                    str_cmd = str_cmd.encode()
                    CLI_result = vst.conn(str_cmd)
                    break   
            return 'SUCCESS' if CLI_result == True else 'Failed'
        else:
            return "test"

class LINSTORmessageView(views.MethodView):
    def get(self):
        Node = ['Node_Name']
        Storage_pool = ['SP_Name']
        Resource = ['Resource_Name_one']
        Resource_mirror =['Resource_Name_mirror']
        Resurce_auto = ['Resource_Name_two']
        Diskless = ['Diskless_name']
        data = {}

        if request.method == 'GET':
            data_all = request.args.items()
            for i in data_all:
                data_one_dict = {i[0]:i[1]}
                data.update(data_one_dict)
            for i in  data.keys():
                if i in Node:
                    str_cmd = "python3 vtel.py stor n c %s -ip %s -nt %s -gui" % (data['Node_Name'], data['IP'], data['Node_Type_Test'])
                    CLI_result = vst.conn(str_cmd.encode())
                    break
                elif i in Storage_pool:
                    str_cmd = "python3 vtel.py stor sp c %s -n %s %s %s -gui" % (data['SP_Name'], data['Node_One_Text'], data['lvm_name'], data['lv_Text'])
                    CLI_result = vst.conn(str_cmd.encode())
                    break
                elif i in Resource:
                    node_val = str(data['Storage_pool_val']).replace(',',' ')
                    sp_val = str(data['sp']).strip(",").replace(',',' ')
                    str_cmd = "python3 vtel.py stor r c %s -s %s%s -n %s -sp %s -gui" %(data['Resource_Name_one'],data['size_one'],data['select_one'],node_val,sp_val)
                    CLI_result = vst.conn(str_cmd.encode())
                    break
                elif i in Resource_mirror:
                    node_val = str(data['Storage_pool_val']).replace(',',' ')
                    sp_val = str(data['sp']).strip(",").replace(',',' ')
                    str_cmd = "python3 vtel.py stor r c %s -am -n %s -sp %s -gui" %(data['Resource_Name_mirror'],node_val,sp_val)
                    CLI_result = vst.conn(str_cmd.encode())
                    break
                elif i in Resurce_auto:
                    str_cmd = "python3 vtel.py stor r c %s -s %s%s -a -num %d -gui" % (data['Resource_Name_two'], data['size_two'], data['select_two'], int(data['Node_Num']))
                    CLI_result = vst.conn(str_cmd.encode())
                    break
                elif i in Diskless:
                    str_cmd = "python3 vtel.py stor r c %s -diskless -n %s -gui" % (data['Diskless_name'], data['Diskless_node'])
                    CLI_result = vst.conn(str_cmd.encode())
                    break 
            return 'SUCCESS' if CLI_result == True else  CLI_result
                
        else:
            return "request failed"
