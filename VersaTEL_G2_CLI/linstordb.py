#coding:utf-8
import colorama as ca
import prettytable as pt
from functools import wraps
import sqlite3,socket,subprocess,datetime,threading
import multiprocessing as mp
import regex
from excute_sys_command import (linstor,lvm)

def nowtime():
    time = datetime.datetime.now()
    return time



class LINSTORDB():
    #LINSTOR表
    crt_sptb_sql = '''
    create table if not exists storagepooltb(
        id integer primary key, 
        StoragePool varchar(20),
        Node varchar(20),
        Driver varchar(20),
        PoolName varchar(20),
        FreeCapacity varchar(20),
        TotalCapacity varchar(20),
        SupportsSnapshots varchar(20),
        State varchar(20)
        );'''

    crt_rtb_sql = '''
    create table if not exists resourcetb(
        id integer primary key,
        Node varchar(20),
        Resource varchar(20),
        Storagepool varchar(20),
        VolumeNr varchar(20),
        MinorNr varchar(20),
        DeviceName varchar(20),
        Allocated varchar(20),
        InUse varchar(20),
        State varchar(20)
        );'''

    crt_ntb_sql = '''
    create table if not exists nodetb(
        id integer primary key,
        Node varchar(20),
        NodeType varchar(20),
        Addresses varchar(20),
        State varchar(20)
        );'''

    crt_vgtb_sql = '''
        create table if not exists vgtb(
        id integer primary key,
        VG varchar(20),
        VSize varchar(20),
        VFree varchar(20)
        );'''

    crt_thinlvtb_sql = '''
        create table if not exists thinlvtb(
        id integer primary key,
        LV varchar(20),
        VG varchar(20),
        LSize varchar(20)
        );'''

    replace_stb_sql = '''
    replace into storagepooltb
    (
        id,
        StoragePool,
        Node,
        Driver,
        PoolName,
        FreeCapacity,
        TotalCapacity,
        SupportsSnapshots,
        State
        )
    values(?,?,?,?,?,?,?,?,?)
    '''

    replace_rtb_sql = '''
        replace into resourcetb
        (   
            id,
            Node,
            Resource,
            StoragePool,
            VolumeNr,
            MinorNr,
            DeviceName,
            Allocated,
            InUse,
            State
            )
        values(?,?,?,?,?,?,?,?,?,?)
    '''

    replace_ntb_sql = '''
        replace into nodetb
        (
            id,
            Node,
            NodeType,
            Addresses,
            State
            )
        values(?,?,?,?,?)
    '''

    replace_vgtb_sql = '''
        replace into vgtb
        (
            id,
            VG,
            VSize,
            VFree
            )
        values(?,?,?,?)
    '''

    replace_thinlvtb_sql = '''
        replace into thinlvtb
        (
            id,
            LV,
            VG,
            LSize
            )
        values(?,?,?,?)
    '''
    #连接数据库,创建光标对象
    def __init__(self):
        #linstor.db
        self.con = sqlite3.connect(":memory:", check_same_thread=False)
        self.cur = self.con.cursor()

    #执行获取数据，删除表，创建表，插入数据
    def rebuild_tb(self):
        self.drop_tb()
        self.create_tb()
        self.exc_get_vg()
        self.exc_get_thinlv()
        self.get_output()
        # self.create_tb()
        # self.run_insert()
        self.con.commit()

    def get_output(self):
        #threading
        threads = []
        thread_ins_node = threading.Thread(target=self.thread_get_node())
        threads.append(thread_ins_node)
        thread_ins_res = threading.Thread(target=self.thread_get_res())
        threads.append(thread_ins_res)
        thread_ins_sp = threading.Thread(target=self.thread_get_sp())
        threads.append(thread_ins_sp)

        for i in range(len(threads)):
            threads[i].start()
        for i in range(len(threads)):
            threads[i].join()

    def exc_get_vg(self):
        vg = regex.refine_vg(lvm.get_vg())
        self.insert_data(self.replace_vgtb_sql,vg)


    def exc_get_thinlv(self):
        thinlv = regex.refine_thinlv(lvm.get_thinlv())
        self.insert_data(self.replace_thinlvtb_sql, thinlv)

    def thread_get_node(self):
        node = regex.refine_linstor(linstor.get_node())
        self.insert_data(self.replace_ntb_sql,node)

    def thread_get_res(self):
        res = regex.refine_linstor(linstor.get_res())
        self.insert_data(self.replace_rtb_sql,res)

    def thread_get_sp(self):
        sp = regex.refine_linstor(linstor.get_sp())
        self.insert_data(self.replace_stb_sql,sp)


    #创建表
    def create_tb(self):
        self.cur.execute(self.crt_vgtb_sql)
        self.cur.execute(self.crt_thinlvtb_sql)
        self.cur.execute(self.crt_sptb_sql)#检查是否存在表，如不存在，则新创建表
        self.cur.execute(self.crt_rtb_sql)
        self.cur.execute(self.crt_ntb_sql)
        self.con.commit()

    #删除表，现不使用
    def drop_tb(self):
        tables_sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        self.cur.execute(tables_sql)
        tables = self.cur.fetchall()
        for table in tables:
            drp_sql = "drop table if exists %s"%table
            self.cur.execute(drp_sql)
        self.con.commit()


    def insert_data(self,sql,list_data):
        for i in range(len(list_data)):
            list_data[i].insert(0,i+1)
            self.cur.execute(sql,list_data[i])


    def data_base_dump(self):
        cur = self.cur
        con = self.con
        self.rebuild_tb()
        SQL_script = con.iterdump()
        cur.close()
        return "\n".join(SQL_script)



class DataProcess():
    def __init__(self):
        self.linstor_db = LINSTORDB()
        self.linstor_db.rebuild_tb()
        self.cur = self.linstor_db.cur

    #获取表单行数据的通用方法
    def sql_fetch_one(self,sql):
        self.cur.execute(sql)
        date_set = self.cur.fetchone()
        return date_set

    # 获取表全部数据的通用方法
    def sql_fetch_all(self,sql):
        cur = self.cur
        cur.execute(sql)
        date_set = cur.fetchall()
        return list(date_set)


    #node
    def _select_nodetb_all(self):
        select_sql = "SELECT Node,NodeType,Addresses,State FROM nodetb"
        return self.sql_fetch_all(select_sql)


    def _select_nodetb_one(self,node):
        select_sql = "SELECT Node,NodeType,Addresses,State FROM nodetb WHERE  Node = \'%s\'"%node
        return self.sql_fetch_one(select_sql)

    def _select_res_num(self,node):
        select_sql = "SELECT COUNT(Resource) FROM resourcetb WHERE  Node = \'%s\'"%node
        return self.sql_fetch_one(select_sql)

    def _select_stp_num(self,node):
        select_sql = "SELECT COUNT(Node) FROM storagepooltb WHERE Node = \'%s\'"%node
        return self.sql_fetch_one(select_sql)

    def _select_resourcetb(self,node):
        select_sql = "SELECT DISTINCT Resource,StoragePool,Allocated,DeviceName,InUse,State FROM resourcetb WHERE Node = \'%s\'"%node
        return self.sql_fetch_all(select_sql)

    #resource
    def _get_resource(self):
        res = []
        sql_res_all = "SELECT DISTINCT Resource,Allocated,DeviceName,InUse FROM resourcetb"
        res_all = self.sql_fetch_all(sql_res_all)

        sql_res_inuse = "SELECT DISTINCT Resource,Allocated,DeviceName,InUse FROM resourcetb WHERE InUse = 'InUse'"
        in_use =  self.sql_fetch_all(sql_res_inuse)

        for i in in_use:
            res.append(i[0])

        for i in res_all:
            if i[0] in res and i[3] == 'Unused':
                res_all.remove(i)
        return res_all

    def _get_mirro_way(self,res):
        select_sql = "SELECT COUNT(Resource) FROM resourcetb WHERE Resource = \'%s\'"%res
        return self.sql_fetch_one(select_sql)

    def _get_mirror_way_son(self,res):
        select_sql = "SELECT Node,StoragePool,InUse,State FROM resourcetb WHERE Resource = \'%s\'"%res
        return self.sql_fetch_all(select_sql)

    #storagepool
    # 查询storagepooltb全部信息
    def _select_storagepooltb(self):
        select_sql = '''SELECT
            StoragePool,
            Node,
            Driver,
            PoolName,
            FreeCapacity,   
            TotalCapacity,
            SupportsSnapshots,
            State
            FROM storagepooltb
            '''
        return self.sql_fetch_all(select_sql)

    def _res_sum(self,node, stp):
        select_sql = "SELECT COUNT(DISTINCT Resource) FROM resourcetb WHERE Node = '{}' AND StoragePool = '{}'".format(
            node, stp)
        num = self.sql_fetch_one(select_sql)
        return num[0]

    def _res(self,stp):
        select_sql = "SELECT Resource,Allocated,DeviceName,InUse,State FROM resourcetb WHERE StoragePool = \'%s\'"%stp
        return self.sql_fetch_all(select_sql)

    def _node_num_of_storagepool(self,stp):
        select_sql = "SELECT COUNT(Node) FROM storagepooltb WHERE StoragePool = \'%s\'"%stp
        num = self.sql_fetch_one(select_sql)
        return num[0]

    def _node_name_of_storagepool(self,stp):
        select_sql = "SELECT Node FROM storagepooltb WHERE StoragePool = \'%s\'"%stp
        date_set = self.sql_fetch_all(select_sql)
        if len(date_set) == 1:
            names = date_set[0][0]
        else:
            names = [n[0] for n in date_set]
        return names

    def process_data_node_all(self):
        date_list = []
        for i in self._select_nodetb_all():
            node,node_type,addr,status = i
            res_num = self._select_res_num(node)[0]
            stp_num = self._select_stp_num(node)[0]
            list_one = [node,node_type,res_num,stp_num,addr,status]
            date_list.append(list_one)
        self.cur.close()
        return date_list


    #置顶文字
    def process_data_node_one(self,node):
        n = self._select_nodetb_one(node)
        node, node_type, addr, status = n
        res_num = self._select_res_num(node)[0]
        stp_num = self._select_stp_num(node)[0]
        list = [node,node_type,res_num,stp_num,addr,status]
        return tuple(list)

    def process_data_node_specific(self,node):
        date_list = []
        for n in self._select_resourcetb(node):
            res_name, stp_name, size, device_name, used, status = n
            list_one = [res_name, stp_name, size, device_name, used, status]
            date_list.append(list_one)
        return date_list

    def process_data_resource_all(self):
        date_list = []
        list_one = []
        for i in self._get_resource():
            if i[1]: #过滤size为空的resource
                resource, size, device_name, used = i
                mirror_way = self._get_mirro_way(str(i[0]))[0]
                list_one = [resource,mirror_way,size,device_name,used]
                date_list.append(list_one)
        self.cur.close()
        return date_list

    #置顶文字
    def process_data_resource_one(self,resource):
        list_one = []
        for i in self._get_resource():
            if i[0] == resource:
                if i[1]:
                    resource, size, device_name, used = i
                    mirror_way = self._get_mirro_way(str(i[0]))[0]
                    list_one = [resource, mirror_way, size, device_name, used]
        return tuple(list_one)

    def process_data_resource_specific(self,resource):
        data_list = []
        for res_one in self._get_mirror_way_son(resource):
            node_name, stp_name, drbd_role, status = list(res_one)
            if drbd_role == u'InUse':
                drbd_role = u'primary'
            elif drbd_role == u'Unused':
                drbd_role = u'secondary'
            list_one = [node_name,stp_name,drbd_role,status]
            data_list.append(list_one)
        self.cur.close()
        return data_list

    def process_data_stp_all(self):
        date_list = []
        for i in self._select_storagepooltb():
            stp_name, node_name, driver, pool_name, free_size, total_size, snapshots, status = i
            res_num = self._res_sum(str(node_name), str(stp_name))
            list_one = [stp_name,node_name,res_num,driver,pool_name,free_size,total_size,snapshots,status]
            date_list.append(list_one)
        self.cur.close()
        return date_list

    def process_data_stp_all_of_node(self,node):
        date_list = []
        for i in self._select_storagepooltb():
            stp_name, node_name, driver, pool_name, free_size, total_size, snapshots, status = i
            res_num = self._res_sum(str(node_name), str(stp_name))
            if node_name == node:
                list_one = [stp_name,node_name,res_num,driver,pool_name,free_size,total_size,snapshots,status]
                date_list.append(list_one)
        self.cur.close()
        return date_list



    def process_data_stp_specific(self,stp):
        date_list = []
        for res in self._res(stp):
            res_name, size, device_name, used, status = res
            list_one = [res_name,size,device_name,used,status]
            date_list.append(list_one)
        self.cur.close()
        return date_list



#有颜色输出表格装饰器
def table_color(func):
    @wraps(func)
    def wrapper(*args):
        table = pt.PrettyTable()
        status_true = ['UpToDate', 'Online', 'Ok','InUse']
        data,table.field_names = func(*args)
        for lst in data:
            if lst[-1] in status_true:
                lst[-1] = ca.Fore.GREEN + lst[-1] + ca.Style.RESET_ALL
            else:
                lst[-1] = ca.Fore.RED + lst[-1] + ca.Style.RESET_ALL
        for i in data:
            table.add_row(i)
        print(table)
    return wrapper

#无颜色输出表格装饰器
def table(func):
    @wraps(func)
    def wrapper(*args):
        table = pt.PrettyTable()
        data, table.field_names = func(*args)
        for i in data:
            table.add_row(i)
        print(table)
    return wrapper




class OutputData(DataProcess):
    def __init__(self):
        DataProcess.__init__(self)

    """Node视图
    """
    @table_color
    def node_all_color(self):
        data = super().process_data_node_all()
        header = ["node", "node type", "res num", "stp num", "addr", "status"]
        return data,header

    @table
    def node_all(self):
        data = super().process_data_node_all()
        header = ["node", "node type", "res num", "stp num", "addr", "status"]
        return data,header

    @table_color
    def node_one_color(self,node):
        data = super().process_data_node_specific(node)
        header = ['res_name', 'stp_name', 'size', 'device_name', 'used', 'status']
        return data,header

    @table_color
    def node_stp_one_color(self,node):
        data = super().process_data_stp_all_of_node(node)
        header = ['stp_name', 'node_name', 'res_num', 'driver', 'pool_name', 'free_size', 'total_size',
                                  'snapshots', 'status']
        return data,header

    @table
    def node_one(self,node):
        data = super().process_data_node_specific(node)
        header = ['res_name', 'stp_name', 'size', 'device_name', 'used', 'status']
        return data,header

    @table
    def node_stp_one(self,node):
        data = super().process_data_stp_all_of_node(node)
        header = ['stp_name', 'node_name', 'res_num', 'driver', 'pool_name', 'free_size', 'total_size',
                                  'snapshots', 'status']
        return data,header


    # 指定的node视图
    def show_node_one_color(self, node):
        try:
            print(
                "node:%s\nnodetype:%s\nresource num:%s\nstoragepool num:%s\naddr:%s\nstatus:%s" % self.process_data_node_one(
                    node))
            self.node_one_color(node)
            self.node_stp_one_color(node)
        except TypeError:
            print('Node %s does not exist.' % node)


    def show_node_one(self, node):
        try:
            print(
                "node:%s\nnodetype:%s\nresource num:%s\nstoragepool num:%s\naddr:%s\nstatus:%s" % self.process_data_node_one(
                    node))
            self.node_one(node)
            self.node_stp_one(node)
        except TypeError:
            print('Node %s does not exist.' % node)


    """Resource视图
    """
    @table_color
    def res_all_color(self):
        data = super().process_data_resource_all()
        header = ["resource", "mirror_way", "size", "device_name", "used"]
        return data,header

    @table
    def res_all(self):
        data = super().process_data_resource_all()
        header = ["resource", "mirror_way", "size", "device_name", "used"]
        return data,header


    @table_color
    def res_one_color(self,res):
        data = super().process_data_resource_specific(res)
        header = ['node_name', 'stp_name', 'drbd_role', 'status']
        return data,header


    @table
    def res_one(self,res):
        data = super().process_data_resource_specific(res)
        header = ['node_name', 'stp_name', 'drbd_role', 'status']
        return data,header

    def show_res_one_color(self,res):
        try:
            print("resource:%s\nmirror_way:%s\nsize:%s\ndevice_name:%s\nused:%s" % self.process_data_resource_one(
                res))
            self.res_one_color(res)
        except TypeError:
            print('Resource %s does not exist.' % res)

    def show_res_one(self,res):
        try:
            print("resource:%s\nmirror_way:%s\nsize:%s\ndevice_name:%s\nused:%s" % self.process_data_resource_one(
                res))
            self.res_one(res)
        except TypeError:
            print('Resource %s does not exist.' % res)


    """stp视图
    """

    @table_color
    def sp_all_color(self):
        data = super().process_data_stp_all()
        header = ['stp_name', 'node_name', 'res_num', 'driver', 'pool_name', 'free_size', 'total_size',
                              'snapshots', 'status']
        return data,header

    @table
    def sp_all(self):
        data = super().process_data_stp_all()
        header = ['stp_name', 'node_name', 'res_num', 'driver', 'pool_name', 'free_size', 'total_size',
                              'snapshots', 'status']
        return data,header


    @table_color
    def sp_one_color(self,sp):
        data = super().process_data_stp_specific(sp)
        header = ['res_name','size','device_name','used','status']
        return data,header

    @table
    def sp_one(self, sp):
        data = super().process_data_stp_specific(sp)
        header = ['res_name', 'size', 'device_name', 'used', 'status']
        return data, header


    def show_sp_one_color(self,sp):
        node_num = self._node_num_of_storagepool(sp)
        node_name = self._node_name_of_storagepool(sp)
        if node_num == 0:
            print('The storagepool does not exist')
        elif node_num == 1:
            print('Only one node (%s) exists in the storage pool named %s' % (node_name, sp))
            self.sp_one_color(sp)
        else:
            node_name = ' and '.join(node_name)
            print('The storagepool name for %s nodes is %s,they are %s.' % (node_num, sp, node_name))
            self.sp_one_color(sp)


    def show_sp_one(self,sp):
        node_num = self._node_num_of_storagepool(sp)
        node_name = self._node_name_of_storagepool(sp)
        if node_num == 0:
            print('The storagepool does not exist')
        elif node_num == 1:
            print('Only one node (%s) exists in the storage pool named %s' % (node_name, sp))
            self.sp_one(sp)
        else:
            node_name = ' and '.join(node_name)
            print('The storagepool name for %s nodes is %s,they are %s.' % (node_num, sp, node_name))
            self.sp_one(sp)


