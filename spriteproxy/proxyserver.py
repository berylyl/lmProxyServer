# -*- coding: utf-8 -*-
#python3

import os,time
import socket 
from urllib.parse import urlparse
from socketserver import ThreadingTCPServer,ThreadingMixIn,TCPServer,StreamRequestHandler
from http import HTTPStatus

CRLF="\r\n"
MAXLINE = 65536
CLTMAXBUFFER = 1048576
SevMAXBUFFER = 1048576

class Client():
     def __init__(self):
        self.method=None
        self.uri = None
        self.protocol = None
        self.headers =''
        self.ip="127.0.0.1"
        self.host=''
        self.demoain=''
        self.header=''
        self.body=None
        self.request=''
        self.hostname=''
        self.port=0

#class ThreadingProxyServer(ThreadingMixIn, TCPServer):
#    pass      
 
         
class ProxyServerHandler(StreamRequestHandler):
    def _CreateClientSocket(self,hst,prt):
        ADDR=(hst, int(prt))
        cs=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #cs.setsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        print(ADDR,"connecting.....")
        cs.connect(ADDR)
        #cs.settimeout(10)
        return cs 
#####
#HTTP Request:
#GET http://www.baidu.com/index.html HTTP/1.1
#Host: www.baidu.com
#
#HTTPS Request:
#CONNECT www.126.com:443 HTTP/1.1
#Host: www.126.com:443

    def parse_request(self,clt_tunnel):
        clt_req=Client()
        #while True: 
        request=clt_tunnel.recv(CLTMAXBUFFER)
        #    if len(request)==0:
        #        break;
        if len(request) <= CLTMAXBUFFER: 
            request  = request.decode('iso-8859-1').split(CRLF+CRLF,1) # header\r\n\r\nbody
            print("*****","request=",request,"length=",len(request),"*****")
            req_len = len(request)
            if req_len == 2:
                print('reqeust_len=',req_len)
                req_header=request[0].split(CRLF)
                req_body=request[1]
                header_line=req_header[0]
                #print("header before=",header_line)
                header_list=req_header[1:]
                #print("header before=",header_list)
                #parse header line
                clt_req.method,clt_req.url,clt_req.protocol=header_line.split()
                #clt_req.protocol="HTTP/1.0"
                #parse url
                clt_req.uri = urlparse(clt_req.url).path
                clt_req.header=[' '.join([clt_req.method,clt_req.uri,clt_req.protocol])]
                #parse header headers
                for hd in header_list:
                    #print("header before=",hd.split(':',maxsplit=1))
                    k=hd.split(':',maxsplit=1)[0]
                    v=hd.split(':',maxsplit=1)[1]
                    if k=='Proxy-Connection':
                        hd=":".join(['Connection',v])
                    elif k.lower()=='host':
                        hostname=v.split(':')
                        if len(hostname)==2:
                            clt_req.host=hostname[0].strip() 
                            clt_req.port=int(hostname[1])
                        elif len(hostname)==1:
                            #print("hostname=",hostname)
                            clt_req.host=socket.gethostbyname(hostname[0].strip()) 
                            clt_req.port=80
                    clt_req.header.append(hd)
                clt_req.header=CRLF.join(clt_req.header)
                clt_req.request=clt_req.header+CRLF+CRLF
                if req_body != None:
                    clt_req.request+=req_body
            else:
                print("[ERROR`]not a  http request....",request)
                return
         
        else:
            print("[ERROR]too long request....",request)
            return
        return clt_req         
        


    def handle_request(self):
        clt_tunnel=self.connection
        clt_req=self.parse_request(clt_tunnel)
        if clt_req==None:
           return;
        src_tunnel=self._CreateClientSocket(clt_req.host,clt_req.port) 
        try:
            if clt_req.method in ('GET','POST','PUT','HEAD'):
                print('HTTP...................................................')
                
                # transfer client to server
                print("[%s BEGIN CtoS]--------------from client to server------------------"%clt_req.method)
                src_tunnel.send(clt_req.request.encode(encoding='utf-8')) 
                print("[%s END CtoS]--------------from client to server------------------"%clt_req.method)
                
                # transfer server to client
                print("[%s BEGIN StoC]--------------from server to client------------------"%clt_req.method)
                self.do_tunnel_transfer(src_tunnel,clt_tunnel,flag=0)
                print("[%s END StoC]--------------from server to client------------------"%clt_req.method)
            elif clt_req.method == 'CONNECT':
                print('HTTPS...................................................')
                print('plus................A')
                # plus tunnel
                src_tunnel.send(clt_req.request.encode(encoding='utf-8')) 
                self.do_tunnel_transfer(src_tunnel,clt_tunnel,flag=0)
                print('plus................B')
                
                # response 200 to client
                #clt_tunnel.send('HTTP/1.0 200 Connection established\r\n\r\n'.encode(encoding='utf-8'))  
                
                # transfer client to server
                print("[CONNECT BEGIN CtoS]--------------from client to server------------------")
                self.do_tunnel_transfer(clt_tunnel,src_tunnel,flag=1)
                print("[CONNECT END CtoS]--------------from client to server------------------")
                
                # transfer server to client
                print("[CONNECT BEGIN StoC]--------------from server to client------------------")
                self.do_tunnel_transfer(src_tunnel,clt_tunnel,flag=0)
                print("[CONNECT END StoC]--------------from server to client------------------")
            else:
                print('BAD_REQUEST,not support')   
                return 
        except socket.timeout as e:
            print('time out')
        finally:
            #close connetion
            clt_tunnel.close()
            src_tunnel.close()
            print("response achive....")
                 
    
    def do_tunnel_transfer(self,tunnelX,tunnelY,flag):
        print('from %s transfer before'%tunnelX)
        while True:
             if flag==1:
                 tmp=tunnelX.recv(CLTMAXBUFFER)
             else:
                 tmp=tunnelX.recv(SevMAXBUFFER)
             print("transfer content =",tmp)
             tunnelY.sendall(tmp)
             if len(tmp)==0 :
                 break;  
             if not tmp:
                 break;
             print("tmp=",tmp)
             
             if(tmp[-2:]==bytes(2)):
                 break; 
             if flag==1: 
                 if len(tmp)<CLTMAXBUFFER:
                     break;
        print('from %s transfer after'%tunnelX)

 
    def handle(self):
        print("am in handle....................................")
        print("got connection from",self.client_address[0]) 
        
        
        """Handle multiple requests if necessary."""
  
        self.handle_request()


if __name__=='__main__':

    #server = TCPServer(('',8890),ProxyServerHandler)
    server = ThreadingTCPServer(('',8080),ProxyServerHandler)
    server.serve_forever()  
    #import thread
    #thread.start_new_thread(server.serve_forever,())
