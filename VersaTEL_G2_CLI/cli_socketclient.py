import pickle
import socket

def get_host_ip():
    try:
        obj_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        obj_socket.connect(('8.8.8.8', 80))
        ip = obj_socket.getsockname()[0]
    except Exception:
        return '127.0.0.0'
    finally:
        obj_socket.close()
    return ip

ip_port = (get_host_ip(),12144)


class SocketSend():
    def __init__(self):
        self.client = socket.socket()
        self.client.connect(ip_port)

    def send_result(self,func,*args):
        client = self.client
        func_result = func(*args)
        func_result_pickled = pickle.dumps(func_result)
        judge_conn = client.recv(8192).decode()
        print(judge_conn)
        client.send(b'database')
        client.recv(8192)
        client.sendall(func_result_pickled)
        client.recv(8192)
        client.send(b'exit')
        client.close()





