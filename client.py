from http.client import HTTPConnection

conn =  HTTPConnection("127.0.0.1:8127",timeout=30)
conn.request("CONNECT","www.126.com:443",body=None,headers={"Host":"www.126.com:443","User-Agent":"vivo X6D_5.1_weibo_6.5.0_android","Connection":"Alive","Content-Length":"0"})
conn.set_debuglevel(1)
r1=conn.getresponse()
r1.read()
