import os,time
import http.client
import socket 
from urllib.parse import urlparse
from socketserver import ThreadingMixIn,TCPServer,StreamRequestHandler
from http import HTTPStatus

_MAXLINE = 65536
_MAXBuffer = 2048
HOST_G = "127.0.0.1"
#HOST_G = gethostbyname(gethostname()) # python 2.7
PORT_G = 8106
CRLF = "\r\n"

class Client():
     def __init__(self):
        self.protocol = None
        self.headers = {}
        self.uri = None
        self.command=None
        self.ip="127.0.0.1"
        self.host=""
        self.demoain=""
        self.body=None
        self.url=""
 
         
class ProxyServerHandler(StreamRequestHandler):
    
    protocol_version = "HTTP/1.0"
    # MessageClass used to parse headers
    socket.timeout=10	
    
    def _CreateClientSocket(self,hst,prt):
        ADDR=(hst, int(prt))
        cs=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs.connect(ADDR)
        return cs 
#####
#HTTP Request:
#GET http://www.baidu.com/index.html HTTP/1.1
#Host: www.baidu.com
#
#HTTPS Request:
#CONNECT www.126.com:443 HTTP/1.1
#Host: www.126.com:443

    def parse_request(self):
        clt = Client()
        clt.ip = self.client_address[0]
        clt.host = self.client_address[1]
        clt.command = self.command
        clt.protocol = self.protocol_version
        clt.uri = self.path
        clt.headers = self.headers


    def handle_one_request(self):
        #parse uri
        src=self.rfile.readline()
        self.command=src.split()[0]
        self.url=src.split()[1]
        if self.command in ('GET','POST','PUT','HEAD'):
            do_tunnel_tansfer()
        elif self.command=='CONNECT':
            self.wfile.write("HTTP/1.0 200 Connection established\r\n\r\n".encode(encoding="utf-8"))    
        else:
            print('BAD_REQUEST,not support')   


 
    def handle(self):
        print("am in handle....................................")
        sc=None 
        print("got connection from",self.client_address[0]) 
        #print("self test",self.command)
        
        
        """Handle multiple requests if necessary."""
  
        self.close_connection = True

        self.handle_one_request()
        while not self.close_connection:
            self.handle_one_request()

         
        '''
        try: 
          #parse GET /index.html HTTP/1.1
          src=self.rfile.readline()
          #print("redlin....",src)
          #parse request headers
          
          try:
              self.headers = http.client.parse_headers(self.rfile)
          except http.client.LineTooLong:
              self.send_error(HTTPStatus.BAD_REQUEST,"Line too long")
              return False
          print("selfheaders=",self.headers)
  
          #self.headers.get('', "")
  
          req = Client()
          req.command=src.split()[0]
          req.url=src.split()[1] 
          #print("megh=,",type(req.command),"url=",req.url)
             
          if("GET"==req.command.decode):
              print("---in get---")
              do_GET()     
          elif("POST"==req.command.decode):
              print("---in post---")
              #self.do_POST()
              pass
          elif("CONNECT"==req.command.decode()):
              print("---in connect---")
              #self.do_CONNECT()
              sc=self._CreateClientSocket("www.126.com","443") 
              if(sc):
                   self.wfile.write("HTTP/1.0 200 Connection established\r\n\r\n".encode(encoding="utf-8"))
                   # receive from client
                   print("col......")
                   print("from client before")
                   #readtcp
                   while True:
                       #line=self.rfile.readline()
                       line=self.connection.recv(2048)
                       print("line...",len(line))
                       if len(line) > _MAXLINE:
                           raise http.client.LineTooLong("tcp content")
                       if not line:
                          break;
                       if len(line)<=2048:
                          break;
                       print("30buf=,",line)
                       print("from client  after")
                   print("out....while")
                   sc.send(line)
                   #buf=self.rfile.read()
                   scre=sc.recv(20480)
                   print("from sever source:")
                   #print(scre)
                   self.wfile.write(scre)
          else:
            pass
        except socket.timeout as e:
            print('time out')
        finally:
            self.connection.close()
            print("response achive....")
           ''' 

if __name__=='__main__':

    server = TCPServer(('',8901),ProxyServerHandler)
    server.serve_forever()
    #import thread
    #thread.start_new_thread(server.serve_forever,())
