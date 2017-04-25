from  http.server  import BaseHTTPRequestHandler,HTTPServer  #python2.7
class HTTPProxyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.abc=None
        self.abc=self.command
        print("self=",self.command)


if __name__=='__main__':
    server = HTTPServer(('',8232),HTTPProxyHandler)
    #server = ThreadingHTTPServer(('',8203),HTTPProxyHandler)
    server.serve_forever()
