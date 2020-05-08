#coding:utf-8
import socketserver,socket,subprocess,datetime

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

host_port = 12144
host_ip = get_host_ip()
byteData = b'null'

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global byteData
        self.request.send(('%s connection succeeded' % h).encode())
        while True:
            data = self.request.recv(4096).decode()
            print ('recv:',data)
            if data=='exit':
                break
            elif 'CLIcommands' in data:
                self.request.send(b'data')
                ex_cmd=self.request.recv(8192).decode()#GUI rec
                subprocess.getoutput(ex_cmd)
                data_len = str(len(byteData))
                print('data_len:',data_len)
                self.request.sendall(data_len.encode())
                self.request.recv(8192)
                self.request.sendall(byteData)
            elif 'database' in data:
                self.request.send(b'ok')
                sql_script = self.request.recv(8192)
                byteData = sql_script
                self.request.send(b'over')
            else:
                pass





if __name__ == '__main__':
    h, p = host_ip,host_port
    server = socketserver.ThreadingTCPServer((h, p), MyTCPHandler)
    server.serve_forever()