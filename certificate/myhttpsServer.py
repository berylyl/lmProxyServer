from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import ssl
import os
class HTTPRequestHandler(BaseHTTPRequestHandler):
    def setup(self):
        SSLSocket = ssl.wrap_socket(self.request,server_side=True, keyfile="key.pem", certfile="cert.pem",ca_certs="ca.crt",ssl_version=ssl.PROTOCOL_TLSv1)
        self.rfile = SSLSocket.makefile('rb', self.rbufsize)
        self.wfile = SSLSocket.makefile('wb', self.wbufsize)

    def do_GET(self):
        req_time = int(time.time())
        clt_IP = self.client_address[0]

        self.protocol_version = "HTTP/1.1"
        self.server_version = "CenterServiceMock"

        self.send_response(200)
        self.end_headers()
        self.wfile.write("This is ServiceSerice %s"%clt_IP)

if __name__=='__main__':

    server = HTTPServer(('',443),HTTPRequestHandler)
    #Thread.server.serve_forever()
    import thread
    thread.start_new_thread(server.serve_forever,())
