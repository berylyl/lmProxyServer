#from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer  #python2.7
from http.server  import BaseHTTPRequestHandler,HTTPServer
#import ssl
import os,time
import subprocess
from http.client import  HTTPConnection 
import hashlib  
from socketserver import ThreadingMixIn
class Client():
     def __init__(self):
        self.protocol = None
        self.headers = None 
        self.uri = None
        self.command=None
        self.ip="127.0.0.1"
        self.host=""
        self.demoain=""
        self.body=None
         
class HTTPProxyHandler(BaseHTTPRequestHandler):
    
    ###
    #def setup(self):
    #    SSLSocket = ssl.wrap_socket(self.request,server_side=True, keyfile="key.pem", certfile="cert.pem",ca_certs="ca.crt",ssl_version=ssl.PROTOCOL_TLSv1)
    #    self.rfile = SSLSocket.makefile('rb', self.rbufsize)
    #    self.wfile = SSLSocket.makefile('wb', self.wbufsize)
    ###
  

    def get_client_request(self):
        clt = Client()
        clt.ip = self.client_address[0]
        clt.host = self.client_address[1]
        clt.command = self.command
        print("comman=",clt.command)
        clt.protocol = self.protocol_version
        clt.uri = self.path
        clt.headers = self.headers
        if(self.command.lower()=="get"):
            print("url=%s,method=%s,protocol=%s"%(clt.uri,clt.command,clt.protocol))
        
        for k,v in  self.headers.items():
            content_length=self.headers['content-length']
            if("host"==k.lower()):
                clt.domain=self.headers[k]
            elif("content-length"==k.lower()  and content_length!=None and int(content_length)>0):
                clt.body = self.rfile.read(int(content_length))
            clt.headers[k]= self.headers[k]
        return clt
 
    def do_proxy_request(self,req):
        conn =  HTTPConnection(req.domain,timeout=30)
        conn.request(req.command,req.uri, body=req.body,headers=req.headers)
        conn.set_debuglevel(2)
        r1=conn.getresponse()
        resp = r1.read()
        return resp
 
 
    def do_GET(self):
        print("a get requst ready...")
        self.log_request(400)
        req_time = int(time.time())
        clt_req = self.get_client_request()
        #do request to src
        response = self.do_proxy_request(clt_req) 
        self.wfile.write(response)

  
    def do_POST(self):
        print ("a post requst ready...............")
        self.do_GET()
        print ("a post requst gone.................")


    def do_CONNECT(self):
        print ("a connect requst ready...")
                
     
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


if __name__=='__main__':

    server = HTTPServer(('',7001),HTTPProxyHandler)
    #server = ThreadingHTTPServer(('',8203),HTTPProxyHandler)
    server.serve_forever()
    #import thread
    #thread.start_new_thread(server.serve_forever,())
