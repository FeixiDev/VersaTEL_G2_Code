#coding:utf-8

import socket,pickle

ip_port = ('10.203.1.89',12144)
judge_len = 8192

command=b'CLIcommands'

def conn(ex_cmd):
    client=socket.socket()
    client.connect(ip_port)
    data = client.recv(8192).decode()
    print (data)
    client.send(command)
    client.recv(8192)
    client.send(ex_cmd)
    data_len = int(client.recv(8192).decode())
    client.send(b'ok')
    chunks = []
    bytes_recd = 0
    while bytes_recd < data_len:
        chunk = client.recv(min(data_len - bytes_recd,2048))
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
        if bytes_recd == data_len:break
    client.send(b'exit')
    return (pickle.loads(b''.join(chunks)))
