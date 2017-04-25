import os,time
import http.client
import socket 
from urllib.parse import urlparse
from socketserver import ThreadingMixIn,TCPServer,StreamRequestHandler
_MAXLINE = 65536

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

    def do_GET(self):
        pass
        """
        self.log_request(400)
        req_time = int(time.time())
        clt_req = self.get_client_request()
        response = self.do_proxy_request(clt_req)
        self.wfile.write(response)
        """

    def do_POST(self):
        pass
        """
        #self.log_request(200)
        req_time = int(time.time())
        clt_req = self.get_client_request()
        #print("request{method=%s,uri=%s,protocol=%s}"%(clt_req.command,clt_req.uri,clt_req.protocol))
        clt_headers=clt_req.headers
        #print("req_headers:\n")
        #for k,v in clt_headers.items():
        #    print("{%s:%s}"%(k,v))
        #print("---POST header end ----")
        response = self.do_proxy_request(clt_req)
        self.wfile.write(response)
        """
    
    def do_Connect(self):
        pass
 
    def handle(self):
        print("am in handle....................................")
        sc=None 
        print("got connection from",self.client_address[0]) 
        
        try: 
          #parse GET /index.html HTTP/1.1
          src=self.rfile.readline()
          print("redlin....",src)
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
          print("megh=,",type(req.command),"url=",req.url)
             
          if("GET"==req.command.decode):
              print("---in get--")
              self.wfile.write("HTTP/1.0 200 OK\r\ncontent-length:3\r\n\r\n123\r\n".encode(encoding="utf-8"))
          elif("POST"==req.command.decode):
              print("---in post--")
              #self.do_POST()
              pass
          elif("CONNECT"==req.command.decode()):
              print("---in connect--")
              #self.do_CONNECT()
              sc=self._CreateClientSocket("www.baidu.com","443") 
              if(sc):
                   self.connection.send("HTTP/1.0 200 Connection established\r\n\r\n".encode(encoding="utf-8"))
                   # receive from client
                   print("col......")
                   print("from client before")
                   #readtcp
                   while True:
                       #line=self.rfile.readline()
                       line=self.connection.recv(2048)
                       print("line...",len(line))
                       print("30buf=,",line)
                       if len(line) > _MAXLINE:
                           raise http.client.LineTooLong("tcp content")
                       if not line:
                          break;
                       if len(line)<2048:
                          break;
                       print("from client  after")
                   print("out....while")
                   sc.send(line)
                   #buf=self.rfile.read()
                   while True:
                       print("from sever source:")
                       scre=sc.recv(20480)
                       print("------------------------from sever source achive:")
                       self.connection.send(scre)
                       print(scre)
                       if(scre[-2:]==bytes(2)):
                           break;            
                       if len(scre)==0:
                           break;            
                       #self.wfile.write(scre)
          else:
              print("tcp request,not support")
              #buf=self.request.recv(1024)  
              #print(buf)
              """
              buf=self.rfile.read()
              print(buf)
              print("from client  after")
                   
              sc.send(buf)
              scre=sc.recv(20480)
              print("from sever source:")
              print(scre)
              self.wfile.write(scre)
              """
        except socket.timeout as e:
            print('time out')
        finally:
            self.connection.close()
            print("response achive....")
    def pase_request(self):
        req = Clinet()
        request_list=request.split()
        req.command=request_list[0]
        req.url=request_list[1]

if __name__=='__main__':

    server = TCPServer(('',8546),ProxyServerHandler)
    server.serve_forever()
    #import thread
    #thread.start_new_thread(server.serve_forever,())
