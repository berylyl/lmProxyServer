from socket import *

class TcpClient:
    HOST='30.10.198.25'
    PORT=8888
    BUFSIZ=1024
    ADDR=(HOST, PORT)
    def __init__(self):
        self.client=socket(AF_INET, SOCK_STREAM)
        self.client.connect(self.ADDR)

        self.cnt="""CONNECT www.126.com:443 HTTP/1.1
Host: www.126.com:443"""
        while True:
            self.client.send(self.cnt.encode('utf8'))
            data=self.client.recv(self.BUFSIZ)
            if not data:
                break
            print(data.decode('utf8'))
            
if __name__ == '__main__':
    client=TcpClient()
