# coding:utf-8

import argparse
import usage



# 多节点创建resource时，storapoo多于node的异常类
class NodeLessThanSPError(Exception):
    pass


class InvalidSize(Exception):
    pass


class CLI():
    def __init__(self):
        self.parser_vtel()
        # self.parser_stor()
        # self.parser_iscsi()


    def parser_vtel(self):
        self.vtel = argparse.ArgumentParser(prog='vtel')
        sub_vtel = self.vtel.add_subparsers(dest='vtel_sub')

        # add all sub parse
        self.vtel_stor = sub_vtel.add_parser('stor', help='Management operations for LINSTOR', add_help=False,
                                             usage=usage.stor)
        self.vtel_iscsi = sub_vtel.add_parser('iscsi', help='Management operations for iSCSI', add_help=False)
        self.vtel_fc = sub_vtel.add_parser('fc', help='for fc resource management...', add_help=False)
        self.vtel_ceph = sub_vtel.add_parser('ceph', help='for ceph resource management...', add_help=False)
        self.vtel_stor.add_argument('-gui', dest='db', action='store_true', help=argparse.SUPPRESS, default=False)

    def parser_stor(self):
        ##stor
        sub_stor = self.vtel_stor.add_subparsers(dest='stor_sub')
        self.stor_node = sub_stor.add_parser('node', aliases='n', help='Management operations for node',
                                             usage=usage.node)
        self.stor_resource = sub_stor.add_parser('resource', aliases='r', help='Management operations for storagepool',
                                                 usage=usage.resource)
        self.stor_storagepool = sub_stor.add_parser('storagepool', aliases=['sp'],
                                                    help='Management operations for storagepool',
                                                    usage=usage.storagepool)
        self.stor_snap = sub_stor.add_parser('snap', aliases=['sn'], help='Management operations for snapshot')
        # self.stor_gui = sub_stor.add_parser('gui',help='for GUI')

        ###node
        sub_node = self.stor_node.add_subparsers(dest='node_sub')
        self.node_create = sub_node.add_parser('create', aliases='c', help='Create the node', usage=usage.node_create)
        self.node_modify = sub_node.add_parser('modify', aliases='m', help='Modify the node', usage=usage.node_modify)
        self.node_delete = sub_node.add_parser('delete', aliases='d', help='Delete the node', usage=usage.node_delete)
        self.node_show = sub_node.add_parser('show', aliases='s', help='Displays the node view', usage=usage.node_show)

        ###resource
        sub_resource = self.stor_resource.add_subparsers(dest='resource_sub')
        self.resource_create = sub_resource.add_parser('create', aliases='c', help='Create the resource',
                                                       usage=usage.resource_create)
        self.resource_modify = sub_resource.add_parser('modify', aliases='m', help='Modify the resource',
                                                       usage=usage.resource_modify)
        self.resource_delete = sub_resource.add_parser('delete', aliases='d', help='Delete the resource',
                                                       usage=usage.resource_delete)
        self.resource_show = sub_resource.add_parser('show', aliases='s', help='Displays the resource view',
                                                     usage=usage.resource_show)

        ###storagepool
        sub_storagepool = self.stor_storagepool.add_subparsers(dest='storagepool_sub')
        self.storagepool_create = sub_storagepool.add_parser('create', aliases='c', help='Create the storagpool',
                                                             usage=usage.storagepool_create)
        self.storagepool_modify = sub_storagepool.add_parser('modify', aliases='m', help='Modify the storagpool',
                                                             usage=usage.storagepool_modify)
        self.storagepool_delete = sub_storagepool.add_parser('delete', aliases='d', help='Delete the storagpool',
                                                             usage=usage.storagepool_delete)
        self.storagepool_show = sub_storagepool.add_parser('show', aliases='s', help='Displays the storagpool view',
                                                           usage=usage.storagepool_show)

        ###snap
        sub_snap = self.stor_snap.add_subparsers(dest='snap_sub')
        self.snap_create = sub_snap.add_parser('create', help='Create the snapshot')
        self.snap_modify = sub_snap.add_parser('modify', help='Modify the snapshot')
        self.snap_delete = sub_snap.add_parser('delete', help='Delete the snapshot')
        self.snap_show = sub_snap.add_parser('show', help='Displays the snapshot view')

        ###stor node create
        self.node_create.add_argument('node', metavar='NODE', action='store',
                                      help='Name of the new node, must match the nodes hostname')
        self.node_create.add_argument('-ip', dest='ip', action='store',
                                      help='IP address of the new node, if not specified it will be resolved by the name.',
                                      required=True)
        self.node_create.add_argument('-nt', dest='nodetype', action='store',
                                      help='node type: {Controller,Auxiliary,Combined,Satellite}', required=True)
        self.node_create.add_argument('-gui', dest='gui', action='store_true', help=argparse.SUPPRESS, default=False)

        ###stor node modify

        ###stor node delete
        self.node_delete.add_argument('node', metavar='NODE', action='store', help=' Name of the node to remove')
        self.node_delete.add_argument('-y', dest='yes', action='store_true', help='Skip to confirm selection',
                                      default=False)
        self.node_delete.add_argument('-gui', dest='gui', action='store_true', help=argparse.SUPPRESS, default=False)

        ###stor node show
        self.node_show.add_argument('node', metavar='NODE', help='Print information about the node in LINSTOR cluster',
                                    action='store', nargs='?', default=None)
        self.node_show.add_argument('--no-color', dest='nocolor', help='Do not use colors in output.',
                                    action='store_true', default=False)
        ###stor resource create

        self.resource_create.add_argument('resource', metavar='RESOURCE', action='store', help='Name of the resource')
        self.resource_create.add_argument('-s', dest='size', action='store',
                                          help=' Size of the resource.In addition to creating diskless resource, you must enter SIZE.'
                                               'Valid units: B, K, kB, KiB, M, MB,MiB, G, GB, GiB, T, TB, TiB, P, PB, PiB.\nThe default unit is GB.')
        self.resource_create.add_argument('-gui', dest='gui', action='store_true', help=argparse.SUPPRESS,
                                          default=False)

        # 自动创建在num个节点上
        group_auto = self.resource_create.add_argument_group(title='auto create')
        group_auto.add_argument('-a', dest='auto', action='store_true', default=False,
                                help='Auto create method Automatic create')
        group_auto.add_argument('-num', dest='num', action='store',
                                help='Number of nodes specified by auto creation method', type=int)

        # 手动选择节点和存储池
        group_manual = self.resource_create.add_argument_group(title='manual create')
        group_manual.add_argument('-n', dest='node', action='store', nargs='+',
                                  help='Name of the node to deploy the resource')
        group_manual.add_argument('-sp', dest='storagepool', nargs='+', help='Storage pool name to use.')

        # 创建diskless
        group_manual_diskless = self.resource_create.add_argument_group(title='diskless create')
        group_manual_diskless.add_argument('-diskless', action='store_true', default=False, dest='diskless',
                                           help='Will add a diskless resource on all non replica nodes.')

        # 创建mirror way，可用于自动创建和手动创建
        group_add_mirror = self.resource_create.add_argument_group(title='add mirror way')
        group_add_mirror.add_argument('-am', action='store_true', default=False, dest='add_mirror',
                                      help='Add resource mirror on other nodes')

        ###stor resource modify
        self.resource_modify.add_argument('resource', metavar='RESOURCE', action='store',
                                          help='resources to be modified')
        self.resource_modify.add_argument('-n', dest='node', action='store', help='node to be modified')
        self.resource_modify.add_argument('-sp', dest='storagepool', action='store', help='Storagepool')

        ###stor resource delete
        self.resource_delete.add_argument('resource', metavar='RESOURCE', action='store',
                                          help='Name of the resource to delete')
        self.resource_delete.add_argument('-n', dest='node', action='store',
                                          help='The name of the node. In this way, the cluster retains the attribute of the resource, including its name and size.')
        self.resource_delete.add_argument('-y', dest='yes', action='store_true', help='Skip to confirm selection',
                                          default=False)
        self.resource_delete.add_argument('-gui', dest='gui', action='store_true', help=argparse.SUPPRESS,
                                          default=False)

        ###stor resource show
        self.resource_show.add_argument('resource', metavar='RESOURCE',
                                        help='Print information about the resource in LINSTOR cluster', action='store',
                                        nargs='?')
        self.resource_show.add_argument('--no-color', dest='nocolor', help='Do not use colors in output.',
                                        action='store_true', default=False)

        ###stor storagepool create
        self.storagepool_create.add_argument('storagepool', metavar='STORAGEPOOL', action='store',
                                             help='Name of the new storage pool')
        self.storagepool_create.add_argument('-n', dest='node', action='store',
                                             help='Name of the node for the new storage pool', required=True)
        self.storagepool_create.add_argument('-gui', dest='gui', action='store_true', help=argparse.SUPPRESS,
                                             default=False)
        group_type = self.storagepool_create.add_mutually_exclusive_group()
        group_type.add_argument('-lvm', dest='lvm', action='store', help='The Lvm volume group to use.')
        group_type.add_argument('-tlv', dest='tlv', action='store',
                                help='The LvmThin volume group to use. The full name of the thin pool, namely VG/LV')

        ###stor storagepool modify

        ###stor storagepool delete
        self.storagepool_delete.add_argument('storagepool', metavar='STORAGEPOOL',
                                             help='Name of the storage pool to delete', action='store')
        self.storagepool_delete.add_argument('-n', dest='node', action='store',
                                             help='Name of the Node where the storage pool exists', required=True)
        self.storagepool_delete.add_argument('-y', dest='yes', action='store_true', help='Skip to confirm selection',
                                             default=False)
        self.storagepool_delete.add_argument('-gui', dest='gui', action='store_true', help=argparse.SUPPRESS,
                                             default=False)

        ###stor storgagepool show
        self.storagepool_show.add_argument('storagepool', metavar='STORAGEPOOL',
                                           help='Print information about the storage pool in LINSTOR cluster',
                                           action='store', nargs='?')
        self.storagepool_show.add_argument('--no-color', dest='nocolor', help='Do not use colors in output.',
                                           action='store_true', default=False)

        ###stor snap create

        ###stor snap modify

        ###stor snap delete

        ###stor snap show

    def parser_iscsi(self):
        ## iscsi
        sub_iscsi = self.vtel_iscsi.add_subparsers(dest='iscsi')
        self.iscsi_host = sub_iscsi.add_parser('host', aliases='h', help='host operation')
        self.iscsi_disk = sub_iscsi.add_parser('disk', aliases='d', help='disk operation')
        self.iscsi_hostgroup = sub_iscsi.add_parser('hostgroup', aliases=['hg'], help='hostgroup operation')
        self.iscsi_diskgroup = sub_iscsi.add_parser('diskgroup', aliases=['dg'], help='diskgroup operation')
        self.iscsi_map = sub_iscsi.add_parser('map', aliases='m', help='map operation')
        self.iscsi_show = sub_iscsi.add_parser('show', aliases='s')

        ### iscsi show
        self.iscsi_show.add_argument('js', help='js show')

        ### iscsi host
        sub_iscsi_host = self.iscsi_host.add_subparsers(dest='host')
        self.iscsi_host_create = sub_iscsi_host.add_parser('create', aliases='c',
                                                           help='host create [host_name] [host_iqn]')
        self.iscsi_host_show = sub_iscsi_host.add_parser('show', aliases='s', help='host show / host show [host_name]')
        self.iscsi_host_delete = sub_iscsi_host.add_parser('delete', aliases='d', help='host delete [host_name]')
        # self.iscsi_host_modify = sub_iscsi_host.add_parser('modify',help='host modify')

        ### iscsi disk
        sub_iscsi_disk = self.iscsi_disk.add_subparsers(dest='disk')
        self.iscsi_disk_show = sub_iscsi_disk.add_parser('show', aliases='s', help='disk show')

        ### iscsi hostgroup
        sub_iscsi_hostgroup = self.iscsi_hostgroup.add_subparsers(dest='hostgroup')
        self.iscsi_hostgroup_create = sub_iscsi_hostgroup.add_parser('create', aliases='c',
                                                                     help='hostgroup create [hostgroup_name] [host_name1] [host_name2] ...')
        self.iscsi_hostgroup_show = sub_iscsi_hostgroup.add_parser('show', aliases='s',
                                                                   help='hostgroup show / hostgroup show [hostgroup_name]')
        self.iscsi_hostgroup_delete = sub_iscsi_hostgroup.add_parser('delete', aliases='d',
                                                                     help='hostgroup delete [hostgroup_name]')

        ### iscsi diskgroup
        sub_iscsi_diskgroup = self.iscsi_diskgroup.add_subparsers(dest='diskgroup')
        self.iscsi_diskgroup_create = sub_iscsi_diskgroup.add_parser('create', aliases='c',
                                                                     help='diskgroup create [diskgroup_name] [disk_name1] [disk_name2] ...')
        self.iscsi_diskgroup_show = sub_iscsi_diskgroup.add_parser('show', aliases='s',
                                                                   help='diskgroup show / diskgroup show [diskgroup_name]')
        self.iscsi_diskgroup_delete = sub_iscsi_diskgroup.add_parser('delete', aliases='d',
                                                                     help='diskgroup delete [diskgroup_name]')

        ### iscsi map
        sub_iscsi_map = self.iscsi_map.add_subparsers(dest='map')
        self.iscsi_map_create = sub_iscsi_map.add_parser('create', aliases='c',
                                                         help='map create [map_name] -hg [hostgroup_name] -dg [diskgroup_name]')
        self.iscsi_map_show = sub_iscsi_map.add_parser('show', aliases='s', help='map show / map show [map_name]')
        self.iscsi_map_delete = sub_iscsi_map.add_parser('delete', aliases='d', help='map delete [map_name]')

        #### iscsi host argument
        self.iscsi_host_create.add_argument('iqnname', action='store', help='host_name')
        self.iscsi_host_create.add_argument('iqn', action='store', help='host_iqn')
        self.iscsi_host_create.add_argument('-gui', help='iscsi gui', nargs='?', default='cmd')
        self.iscsi_host_show.add_argument('show', action='store', help='host show [host_name]', nargs='?',
                                          default='all')
        self.iscsi_host_delete.add_argument('iqnname', action='store', help='host_name', default=None)

        #### iscsi disk argument
        self.iscsi_disk_show.add_argument('show', action='store', help='disk show [disk_name]', nargs='?',
                                          default='all')

        #### iscsi hostgroup argument
        self.iscsi_hostgroup_create.add_argument('hostgroupname', action='store', help='hostgroup_name')
        self.iscsi_hostgroup_create.add_argument('iqnname', action='store', help='host_name', nargs='+')
        self.iscsi_hostgroup_create.add_argument('-gui', help='iscsi gui', nargs='?', default='cmd')
        self.iscsi_hostgroup_show.add_argument('show', action='store', help='hostgroup show [hostgroup_name]',
                                               nargs='?', default='all')
        self.iscsi_hostgroup_delete.add_argument('hostgroupname', action='store', help='hostgroup_name', default=None)

        #### iscsi diskgroup argument
        self.iscsi_diskgroup_create.add_argument('diskgroupname', action='store', help='diskgroup_name')
        self.iscsi_diskgroup_create.add_argument('diskname', action='store', help='disk_name', nargs='+')
        self.iscsi_diskgroup_create.add_argument('-gui', help='iscsi gui', nargs='?', default='cmd')
        self.iscsi_diskgroup_show.add_argument('show', action='store', help='diskgroup show [diskgroup_name]',
                                               nargs='?', default='all')
        self.iscsi_diskgroup_delete.add_argument('diskgroupname', action='store', help='diskgroup_name', default=None)

        #### iscsi map argument
        self.iscsi_map_create.add_argument('mapname', action='store', help='map_name')
        self.iscsi_map_create.add_argument('-hg', action='store', help='hostgroup_name')
        self.iscsi_map_create.add_argument('-dg', action='store', help='diskgroup_name')
        self.iscsi_map_create.add_argument('-gui', help='iscsi gui', nargs='?', default='cmd')
        self.iscsi_map_show.add_argument('show', action='store', help='map show [map_name]', nargs='?', default='all')
        self.iscsi_map_delete.add_argument('mapname', action='store', help='map_name', default=None)


if __name__ == '__main__':
    pass
