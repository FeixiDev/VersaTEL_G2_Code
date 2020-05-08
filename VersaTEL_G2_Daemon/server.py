#coding:utf-8
import socketserver,socket,subprocess,datetime

def nowTimes():
    now_time = datetime.datetime.now()
    return now_time

host_port = 12144
# host_ip = "192.168.36.61"
host_ip = "10.203.1.89"
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

                # #接收记录时间的字典
                # cli_reve_time = self.request.recv(8192).decode()
                # for i,j in eval(cli_reve_time).items():
                #     print(i,j)
                # self.request.send(b'ok')
            else:
                pass





if __name__ == '__main__':
    h, p = host_ip,host_port
    server = socketserver.ThreadingTCPServer((h, p), MyTCPHandler)
    server.serve_forever()