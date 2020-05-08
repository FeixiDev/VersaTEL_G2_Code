# coding:utf-8
import re

class GetLinstor():
    def __init__(self,table_data):
        self.tale = table_data
        self.reSeparate = re.compile('(.*?\s\|)')


    def get_data(self):
        list_table= self.tale.split('\n')
        list_data_all = []

        def clear_symbol(list_data):
            for i in range(len(list_data)):
                list_data[i] = list_data[i].replace(' ', '')
                list_data[i] = list_data[i].replace('|', '')

        for i in range(len(list_table)):
            if list_table[i].startswith('|') and '=' not in list_table[i]:
                valid_data = self.reSeparate.findall(list_table[i])
                clear_symbol(valid_data)
                list_data_all.append(valid_data)
        list_data_all.pop(0)
        return list_data_all

