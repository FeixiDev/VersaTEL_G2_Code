# coding=utf-8
import re
import subprocess
import time

"""
@author: Zane
@note: VersaTEL-iSCSI获取crm信息
@time: 2020/03/11
@uptime: 2020/04/07
"""


class crm():

    def re_data(self, crmdatas):
        crmdata = str(crmdatas)
        plogical = re.compile(
            r'primitive\s(\w*)\s\w*\s\\\s*\w*\starget_iqn="([a-zA-Z0-9.:-]*)"\s[a-z=-]*\slun=(\d*)\spath="([a-zA-Z0-9/]*)"\sallowed_initiators="([a-zA-Z0-9.: -]+)"(?:.*\s*){2}meta target-role=(\w*)')
        pvip = re.compile(r'primitive\s(\w*)\sIPaddr2\s\\\s*\w*\sip=([0-9.]*)\s\w*=(\d*)\s')
        ptarget = re.compile(
            r'primitive\s(\w*)\s\w*\s\\\s*params\siqn="([a-zA-Z0-9.:-]*)"\s[a-z=-]*\sportals="([0-9.]*):\d*"\s\\')
        redata = [plogical.findall(crmdata), pvip.findall(crmdata), ptarget.findall(crmdata)]
        print("get crm config data")
        return redata

    def get_data_crm(self):
        crmconfig = subprocess.getoutput('crm configure show')
        print("do crm configure show")
        # print("crmconfig:",crmconfig)
        return crmconfig

    def get_data_linstor(self):
        linstorres = subprocess.getoutput('linstor --no-color --no-utf8 r lv')
        print("do linstor r lv")
        return linstorres

    def createres(self, res, hostiqn, targetiqn):
        initiator = " ".join(hostiqn)
        lunid = str(int(res[1][1:]))
        op = " op start timeout=40 interval=0" \
             " op stop timeout=40 interval=0" \
             " op monitor timeout=40 interval=15"
        meta = " meta target-role=Stopped"
        mstr = "crm conf primitive " + res[0] \
               + " iSCSILogicalUnit params target_iqn=\"" + targetiqn \
               + "\" implementation=lio-t lun=" + lunid \
               + " path=\"" + res[2] \
               + "\" allowed_initiators=\"" + initiator + "\"" \
               + op + meta
        print(mstr)
        createcrm = subprocess.call(mstr, shell=True)
        print("call", mstr)
        if createcrm == 0:
            print("create iSCSILogicalUnit success")
            return True
        else:
            return False

    def delres(self, res):
        # crm res stop <LUN_NAME>
        stopsub = subprocess.call("crm res stop " + res, shell=True)
        if stopsub == 0:
            print("crm res stop " + res)
            n = 0
            while n < 10:
                n += 1
                if self.resstate(res):
                    print(res + " is Started, Wait a moment...")
                    time.sleep(1)
                else:
                    print(res + " is Stopped")
                    break
            else:
                print("Stop ressource " + res + " fail, Please try again.")
                return False

            time.sleep(3)
            # crm conf del <LUN_NAME>
            delsub = subprocess.call("crm conf del " + res, shell=True)
            if delsub == 0:
                print("crm conf del " + res)
                return True
            else:
                print("crm delete fail")
                return False
        else:
            print("crm res stop fail")
            return False

    def createco(self, res, target):
        # crm conf colocation <COLOCATION_NAME> inf: <LUN_NAME> <TARGET_NAME>
        print("crm conf colocation co_" + res + " inf: " + res + " " + target)
        coclocation = subprocess.call("crm conf colocation co_" + res + " inf: " + res + " " + target, shell=True)
        if coclocation == 0:
            print("set coclocation")
            return True
        else:
            return False

    def createor(self, res, target):
        # crm conf order <ORDER_NAME1> <TARGET_NAME> <LUN_NAME>
        print("crm conf order or_" + res + " " + target + " " + res)
        order = subprocess.call("crm conf order or_" + res + " " + target + " " + res, shell=True)
        if order == 0:
            print("set order")
            return True
        else:
            return False

    def resstart(self, res):
        # crm res start <LUN_NAME>
        print("crm res start " + res)
        start = subprocess.call("crm res start " + res, shell=True)
        if start == 0:
            return True
        else:
            return False

    def resstate(self, res):
        crm_show = self.get_data_crm()
        redata = self.re_data(crm_show)
        for s in redata[0]:
            if s[0] == res:
                if s[-1] == 'Stopped':
                    return False
                else:
                    return True



