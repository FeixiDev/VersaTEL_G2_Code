#coding:utf-8
import subprocess
import regex as reg
from collections import OrderedDict



def execute_cmd(cmd):
    action = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = action.stdout.read()
    if reg.judge_cmd_result_suc(str(result)):
        return True
    elif reg.judge_cmd_result_err(str(result)):
        print(result.decode('utf-8'))
        return result.decode()
    if reg.judge_cmd_result_war(str(result)):
        messege_war = reg.get_war_mes(result.decode('utf-8'))
        print(messege_war)
        return messege_war


def print_excute_result(cmd):
    result = execute_cmd(cmd)
    if result == True:
        print('SUCCESS')
        return True
    else:
        print('FAIL')
        return result


class Action():
    #创建resource相关 -- ok
    @staticmethod
    def linstor_delete_rd(res):
        cmd = 'linstor rd d %s'%res
        subprocess.check_output(cmd,shell=True)

    @staticmethod
    def linstor_delete_vd(res):
        cmd = 'linstor vd d %s' %res
        subprocess.check_output(cmd,shell=True)


    @staticmethod
    def linstor_create_rd(res):
        cmd_rd = 'linstor rd c %s' %res
        result = execute_cmd(cmd_rd)
        if result == True:
            return True
        else:
            print('FAIL')
            return result

    @staticmethod
    def linstor_create_vd(res,size):
        cmd_vd = 'linstor vd c %s %s' % (res, size)
        result = execute_cmd(cmd_vd)
        if result == True:
            return True
        else:
            print('FAIL')
            Action.linstor_delete_rd(res)
            return result

    #创建resource 自动
    @staticmethod
    def create_res_auto(res,size,num):
        cmd = 'linstor r c %s --auto-place %d' % (res, num)
        if Action.linstor_create_rd(res) is True and Action.linstor_create_vd(res,size) is True:
            result = execute_cmd(cmd)
            if result == True:
                print('SUCCESS')
                return True
            else:
                print('FAIL')
                Action.linstor_delete_rd(res)
                return result

        # 创建resource 手动
    @staticmethod
    def create_res_manual(res, size, node, stp):
        flag = OrderedDict()

        def print_fail_node():
            if len(flag.keys()):
                print('Creation failure on', *flag.keys(), sep=' ')
                for node,cause in flag.items():
                    print(node,':',cause)
                return flag
            else:
                return True


        def whether_delete_rd():
            if len(flag.keys()) == len(node):
                Action.linstor_delete_rd(res)

        def create_resource(cmd):
            action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            result = action.stdout
            if reg.judge_cmd_result_war(str(result)):
                print(reg.get_war_mes(result.decode('utf-8')))

            if reg.judge_cmd_result_suc(str(result)):
                print('Resource %s was successfully created on Node %s' % (res, node_one))
            elif reg.judge_cmd_result_err(str(result)):
                str_fail_cause = reg.get_err_detailes(result.decode('utf-8'))
                dict_fail = {node_one: str_fail_cause}
                flag.update(dict_fail)



        if len(stp) == 1:
            if Action.linstor_create_rd(res) is True and Action.linstor_create_vd(res, size) is True:
                for node_one in node:
                    cmd = 'linstor resource create %s %s --storage-pool %s' % (node_one, res, stp[0])
                    create_resource(cmd)
                whether_delete_rd()
                return print_fail_node()
            else:
                return ('The ResourceDefinition already exists') #need to be prefect
        elif len(node) == len(stp):
            if Action.linstor_create_rd(res) is True and Action.linstor_create_vd(res, size) is True:
                for node_one, stp_one in zip(node, stp):
                    cmd = 'linstor resource create %s %s --storage-pool %s' % (node_one, res, stp_one)
                    create_resource(cmd)
                whether_delete_rd()
                return print_fail_node()
            else:
                return ('The ResourceDefinition already exists')
        else:
            print('The number of Node and Storage pool do not meet the requirements')



    #添加mirror（自动）
    @staticmethod
    def add_mirror_auto(res,num):
        cmd = 'linstor r c %s --auto-place %d' % (res, num)
        return print_excute_result(cmd)

    @staticmethod
    def add_mirror_manual(res,node,stp):
        flag = OrderedDict()

        def print_fail_node():
            if len(flag.keys()):
                print('Creation failure on', *flag.keys(), sep=' ')
                return flag
            else:
                return True


        def add_mirror():
            action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            result = action.stdout
            if reg.judge_cmd_result_suc(str(result)):
                print('Resource %s was successfully created on Node %s'%(res,node_one))
            elif reg.judge_cmd_result_err(str(result)):
                str_fail_cause = reg.get_err_detailes(result.decode('utf-8'))
                dict_fail = {node_one: str_fail_cause}
                flag.update(dict_fail)


        if len(stp) == 1:
            for node_one in node:
                cmd = 'linstor resource create %s %s --storage-pool %s' % (node_one, res, stp[0])
                add_mirror()
            return print_fail_node()
        elif len(node) == len(stp):
            for node_one,stp_one in zip(node,stp):
                cmd = 'linstor resource create %s %s --storage-pool %s' % (node_one, res, stp_one)
                add_mirror()
            return print_fail_node()
        else:
            print('sp数量为1或者与node相等')



    #创建resource --diskless
    @staticmethod
    def create_res_diskless(node,res):
        cmd = 'linstor r c %s %s --diskless' %(node,res)
        return print_excute_result(cmd)

    #删除resource,指定节点 -- ok
    @staticmethod
    def delete_resource_des(node,res):
        cmd = 'linstor resource delete %s %s' %(node,res)
        return print_excute_result(cmd)

    #删除resource，全部节点 -- ok
    @staticmethod
    def delete_resource_all(res):
        cmd = 'linstor resource-definition delete %s' %res
        return print_excute_result(cmd)

    #创建storagepool  -- ok
    @staticmethod
    def create_storagepool_lvm(node,stp,vg):
        cmd = 'linstor storage-pool create lvm %s %s %s' %(node,stp,vg)
        action = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = action.stdout
        if reg.judge_cmd_result_war(str(result)):
            print(result.decode('utf-8'))
        #发生ERROR的情况
        if reg.judge_cmd_result_err(str(result)):
            #使用不存的vg
            if reg.get_err_not_vg(str(result),node,vg):
                print(reg.get_err_not_vg(str(result),node,vg))
                subprocess.check_output('linstor storage-pool delete %s %s'%(node,stp),shell=True)
            else:
                print(result.decode('utf-8'))
                print('FAIL')
                return result.decode()
        #成功
        elif reg.judge_cmd_result_suc(str(result)):
            print('SUCCESS')
            return True


    @staticmethod
    def create_storagepool_thinlv(node,stp,tlv):
        cmd = 'linstor storage-pool create lvmthin %s %s %s' %(node,stp,tlv)
        return print_excute_result(cmd)


    #删除storagepool -- ok
    @staticmethod
    def delete_storagepool(node,stp):
        cmd = 'linstor storage-pool delete %s %s' %(node,stp)
        return print_excute_result(cmd)


    #创建集群节点
    @staticmethod
    def create_node(node,ip,nt):
        cmd = 'linstor node create %s %s  --node-type %s' %(node,ip,nt)
        nt_value = ['Combined','combined','Controller','Auxiliary','Satellite']
        if nt not in nt_value:
            print('node type error,choose from ''Combined','Controller','Auxiliary','Satellite''')
        else:
            return print_excute_result(cmd)

    #删除node
    @staticmethod
    def delete_node(node):
        cmd = 'linstor node delete %s' %node
        return print_excute_result(cmd)

    #确认删除函数
    @staticmethod
    def confirm_del():
        print('Are you sure you want to delete it? If yes, enter \'y/yes\'')
        answer = input()
        if answer in ['y','yes']:
            return True
        else:
            return False


