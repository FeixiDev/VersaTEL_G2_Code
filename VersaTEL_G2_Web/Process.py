# coding:utf-8
# coding:utf-8

import sqlite3
import VersaTELSocket as vst


class LINSTORDB(object):

    def __init__(self):
        self.con = sqlite3.connect(':memory:', check_same_thread=False)
        self.cur = self.con.cursor()
        sql_script = vst.conn(b'python3 vtel.py stor gui -db')
        self.cur.executescript(sql_script)


class Process_data(LINSTORDB):

    def __init__(self):
        LINSTORDB.__init__(self)

    # 获取表单行数据的通用方法
    def sql_fetch_one(self, sql):
        cur = self.cur
        cur.execute(sql)
        date_set = cur.fetchone()
        if len(date_set) == 1:
            return date_set[0]
        else:
            return list(date_set)

    # 获取表全部数据的通用方法
    def sql_fetch_all(self, sql):
        cur = self.cur
        cur.execute(sql)
        date_set = cur.fetchall()
        return date_set

    # 选项node数据
    def get_option_node(self):

        def get_online_node():
            select_sql = "SELECT Node FROM nodetb WHERE State = 'Online'"
            return self.sql_fetch_all(select_sql)

        list_node = get_online_node()  # E.g:[('klay1',), ('klay2',)]
        list_result = []
        for node in list_node:
            dict_one = {'key_node':node[0]}
            list_result.append(dict_one)
        return list_result

    # 选项sp数据
    def get_option_sp(self):

        def get_online_node():
            select_sql = "SELECT Node FROM nodetb WHERE State = 'Online'"
            return self.sql_fetch_all(select_sql)

        def get_ok_sp(node):
            select_sql = "SELECT Storagepool FROM storagepooltb WHERE Node = \'%s\' " \
                         "and FreeCapacity is not null and State = 'Ok'" % node
            return self.sql_fetch_all(select_sql)

        list_node = get_online_node()
        list_result = []
        for node in list_node:
            list_sp = get_ok_sp(node)
            list_result_sp = []
            for sp in list_sp:
                dict_sp = {'key_sp':sp}
                list_result_sp.append(dict_sp)
            dict_one = {'NodeName':node, 'Spool':list_result_sp}
            list_result.append(dict_one)
        return list_result

    # 选项lvm/thinlv数据
    def get_option_lvm(self):
        sql_vg = "SELECT VG FROM vgtb"
        sql_thinlv = "SELECT LV FROM thinlvtb"

        vg = self.sql_fetch_all(sql_vg)
        thinlv = self.sql_fetch_all(sql_thinlv)

        list_vg = []
        list_thinlv = []
        for vg_one in vg:
            dict_vg = {"cityName": vg_one}
            list_vg.append(dict_vg)

        for thinlv_one in thinlv:
            dict_thinlv = {"cityName": thinlv_one}
            list_thinlv.append(dict_thinlv)

        dict_all = {"lvm": list_vg, "thin_lvm": list_thinlv}
        return dict_all

    # 选项node num数据
    def get_option_nodenum(self,):

        def get_node_num():
            select_sql = "SELECT COUNT(Node) FROM nodetb"
            return self.sql_fetch_one(select_sql)

        num_node = int(get_node_num()) + 1
        list_result = []
        for i in range(1, num_node):
            dict_one = {'key_nodenum':i}
            list_result.append(dict_one)
        return list_result

    # node表格格式
    def process_data_node(self):
        # cur = self.linstor_db.cur
        cur = self.cur
        date = []

        sql_count_node = "select count(Node) from nodetb"
        sql_node = lambda id:"select Node,NodeType,Addresses,State from nodetb where id = %s" % id
        sql_count_res = lambda id:"SELECT COUNT(Resource) FROM resourcetb WHERE Node IN (SELECT Node FROM nodetb WHERE id = %s)" % id
        sql_count_stp = lambda id:"SELECT COUNT(Node) FROM storagepooltb WHERE Node IN (SELECT Node FROM nodetb WHERE id = %s)" % id
        sql_res = lambda id:"SELECT Resource,StoragePool,Allocated,DeviceName,InUse,State FROM resourcetb WHERE Node IN ((SELECT Node FROM nodetb WHERE id = %s))" % id

        node_num = self.sql_fetch_one(sql_count_node)

        # 通用的select

        # def _count_node():
        #     select_sql = "select count(Node) from nodetb"
        #     cur.execute(select_sql)
        #     date_set = cur.fetchone()
        #     return list(date_set)
        #
        # def _select_nodetb(n):
        #     select_sql = "select Node,NodeType,Addresses,State from nodetb where id = ?"  # sql语言：进行查询操作
        #     cur.execute(select_sql, str(n))
        #     date_set = cur.fetchone()
        #     return list(date_set)
        #
        # def _select_res_num(n):
        #     select_sql = "SELECT COUNT(Resource) FROM resourcetb WHERE Node IN (SELECT Node FROM nodetb WHERE id = ?)"
        #     cur.execute(select_sql, str(n))
        #     date_set = cur.fetchone()
        #     return list(date_set)
        #
        # def _select_stp_num(n):
        #     select_sql = "SELECT COUNT(Node) FROM storagepooltb WHERE Node IN (SELECT Node FROM nodetb WHERE id = ?)"
        #     cur.execute(select_sql, str(n))
        #     date_set = cur.fetchone()
        #     return list(date_set)
        #
        # def _select_resourcetb(n):
        #     select_sql = "SELECT Resource,StoragePool,Allocated,DeviceName,InUse,State FROM resourcetb WHERE Node IN ((SELECT Node FROM nodetb WHERE id = ?))"
        #     cur.execute(select_sql, (str(n)))
        #     date_set = cur.fetchall()
        #     return list(date_set)
        for i in range(1, (node_num + 1)):  # 从1开始循环到给定的整数，有没有更好的办法
            node, nodetype, addr, status = self.sql_fetch_one(sql_node(i))
            res_num = self.sql_fetch_one(sql_count_res(i))
            stp_num = self.sql_fetch_one(sql_count_stp(i))
            print("res_num:", res_num)
            print("stp_num:", stp_num)
            list_resdict = []
            for res in self.sql_fetch_all(sql_res(i)):
                res_name, stp_name, size, device_name, used, status = res
                dic = {"res_name": res_name, "stp_name": stp_name, "size": size, "device_name": device_name,
                       "used": used, "status": status}
                list_resdict.append(dic)
            # for #返回res_num 对应的几个resource信息，
            date_ = {"node": node,
                     "node_type": nodetype,
                     "res_num": str(res_num),
                     "stp_num": str(stp_num),
                     "addr": addr,
                     "status": status,
                     "res_num_son": list_resdict}
            date.append(date_)
        dict = {"code": 0, "msg": "", "count": 1000, "data": date}
        cur.close()
        return dict

    # resourece表格格式
    def process_data_resource(self):
        cur = self.cur
        date = []

        sql_mirror_way_num = lambda rn: "SELECT COUNT(Resource) FROM resourcetb WHERE Resource = \'%s\' " % rn
        sql_mirror_way = lambda rn: "SELECT Node,StoragePool,InUse,State FROM resourcetb WHERE Resource = \'%s\' " % rn

        def _get_resource():
            res = []
            sql_resource_all = "SELECT distinct Resource,Allocated,DeviceName,InUse FROM resourcetb "
            sql_resource_inuse = "SELECT distinct Resource,Allocated,DeviceName,InUse FROM resourcetb WHERE InUse = 'InUse'"
            res_all = self.sql_fetch_all(sql_resource_all)
            res_inuse = self.sql_fetch_all(sql_resource_inuse)
            for i in res_inuse:
                res.append(i[0])
            for i in res_all:
                if i[0] in res and i[3] == 'Unused':
                    res_all.remove(i)
            return res_all

        for i in _get_resource():
            if i[1]:
                resource, size, device_name, used = i
                mirror_way_num = self.sql_fetch_one(sql_mirror_way_num(str(i[0])))
                list_resdict = []
                for res_one in self.sql_fetch_all(sql_mirror_way(str(i[0]))):
                    node_name, stp_name, drbd_role, status = list(res_one)
                    if drbd_role == u'InUse':
                        drbd_role = u'primary'
                    elif drbd_role == u'Unused':
                        drbd_role = u'secondary'
                    dic = {"node_name": node_name, "stp_name": stp_name, "drbd_role": drbd_role, "status": status}
                    list_resdict.append(dic)
                date_one = {"resource": resource,
                            "mirror_way": mirror_way_num,
                            "size": size,
                            "device_name": device_name,
                            "used": used,
                            "mirror_way_son": list_resdict}
                date.append(date_one)
        dict = {"code": 0, "msg": "", "count": 1000, "data": date}
        cur.close()
        return dict

    # storage pool表格格式
    def process_data_stp(self):
        # linstor_db = Linst_db()
        cur = self.cur
        date = []

        sql_stp = "SELECT StoragePool,Node,Driver,PoolName,FreeCapacity,TotalCapacity,SupportsSnapshots,State FROM storagepooltb"
        sql_res_num = lambda node, stp: "SELECT COUNT(DISTINCT Resource) FROM resourcetb WHERE Node = \'%s\' AND StoragePool = \'%s\'" % (
        node, stp)
        sql_res = lambda node, stp: "SELECT Resource,Allocated,DeviceName,InUse,State FROM resourcetb WHERE Node = \'%s\' AND StoragePool = \'%s\'" % (
        node, stp)

        for i in self.sql_fetch_all(sql_stp):
            stp_name, node_name, driver, pool_name, free_size, total_size, snapshots, stp_status = i
            res_num = self.sql_fetch_one(sql_res_num(str(node_name), str(stp_name)))
            list_resdict = []
            for res in self.sql_fetch_all(sql_res(str(node_name), str(stp_name))):
                res_name, size, device_name, used, res_status = res
                dic = {"res_name": res_name, "size": size, "device_name": device_name, "used": used, "status": res_status}
                list_resdict.append(dic)

            # 返回res_num 对应的几个resource信息，
            date_ = {"stp_name": stp_name,
                     "node_name": node_name,
                     "res_num": str(res_num),
                     "driver": driver,
                     "pool_name": pool_name,
                     "free_size": free_size,
                     "total_size": total_size,
                     "snapshots": snapshots,
                     "status": stp_status,
                     "res_name_son": list_resdict}
            date.append(date_)
        dict = {"code": 0, "msg": "", "count": 1000, "data": date}
        cur.close()
        return dict

