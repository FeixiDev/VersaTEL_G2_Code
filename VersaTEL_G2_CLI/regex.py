#conding:utf-8
import re


def judge_size(size):
    re_size = re.compile('^[1-9][0-9]*([KkMmGgTtPpB](iB|B)?)$')
    if re_size.match(size):
        return size

def judge_cmd_result_suc(cmd):
    re_suc = re.compile('SUCCESS')
    if re_suc.search(cmd):
        return True


def judge_cmd_result_err(cmd):
    re_err = re.compile('ERROR')
    if re_err.search(cmd):
        return True


def judge_cmd_result_war(cmd):
    re_err = re.compile('WARNING')
    if re_err.search(cmd):
        return True


def get_err_mes(cmd):
    re_mes_des = re.compile(r'(?<=Description:\\n)[\S\s]*(?=\\nCause:)')
    if re_mes_des.search(cmd):
        return (re_mes_des.search(cmd).group())


def get_cau_mes(cmd):
    re_mes_cau = re.compile(r'(?<=Cause:\\n)[\S\s]*(?=\\nDetails:)')
    if re_mes_cau.search(cmd):
        return re_mes_cau.search(cmd).group()

def get_err_mes_vd(cmd):
    re_mes_des = re.compile(r'(?<=Description:\\n)[\S\s]*(?=\\nDetails:)')
    if re_mes_des.search(cmd):
        return (re_mes_des.search(cmd).group())


def get_err_not_vg(result,node,vg):
    re_ = re.compile(r'\(Node: \''+node+'\'\) Volume group \''+vg+'\' not found')
    if re_.search(result):
        return (re_.search(result).group())


def get_err_detailes(result):
    re_ = re.compile(r'Description:\n[\t\s]*(.*)\n')
    if re_.search(result):
        return (re_.search(result).group(1))

def get_war_mes(result):
    re_ = re.compile(r'\x1b\[1;33mWARNING:\n\x1b(?:.*\s*)+\n$')
    if re_.search(result):
        return (re_.search(result).group())


def refine_thinlv(str):
    list_tb = str.splitlines()
    list_thinlv = []
    re_ = re.compile(r'\s*(\S*)\s*(\S*)\s*\S*\s*(\S*)\s*\S*\s*\S*\s*\S*\s*?')
    for list_one in list_tb:
        if 'twi' in list_one:
            thinlv_one = re_.findall(list_one)
            list_thinlv.append(list(thinlv_one[0]))
    return list_thinlv

def refine_vg(str):
    list_tb = str.splitlines()
    list_vg = []
    re_ = re.compile(r'\s*(\S*)\s*\S*\s*\S*\s*\S*\s*\S*\s*(\S*)\s*(\S*)\s*?')
    for list_one in list_tb[1:]:
        vg_one = re_.findall(list_one)
        list_vg.append(list(vg_one[0]))
    return list_vg

def refine_linstor(table_data):
    reSeparate = re.compile('(.*?\s\|)')
    list_table= table_data.split('\n')
    list_data_all = []

    def clear_symbol(list_data):
        for i in range(len(list_data)):
            list_data[i] = list_data[i].replace(' ', '')
            list_data[i] = list_data[i].replace('|', '')

    for i in range(len(list_table)):
        if list_table[i].startswith('|') and '=' not in list_table[i]:
            valid_data = reSeparate.findall(list_table[i])
            clear_symbol(valid_data)
            list_data_all.append(valid_data)
    try:
        list_data_all.pop(0)
    except IndexError:
        print('The data cannot be read, please check whether LINSTOR is normal.')
    return list_data_all