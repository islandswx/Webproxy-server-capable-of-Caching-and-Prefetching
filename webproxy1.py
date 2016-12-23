import socket
import sys
import threading
import hashlib
import time
import urllib.request
import os
from bs4 import BeautifulSoup

def mthread2():  #Handles Keyboard Interrupt
    while 1:
        try:
            input()
        except Exception:
            os._exit(1)
    
def mthread1(a1, port, method, http1, z):    #Responsible for prefetching    
    url3 ="http://"+a1
    htmlpage = urllib.request.urlopen(url3)
    soup = BeautifulSoup(htmlpage, "html.parser")
    for link in soup.findAll('a'):
        list1.append(link.get('href'))
        xyz=list(set(list1))           #print(xyz)
    
    for i in xyz:
        if (i.startswith("http")):
            p1=method+" "+i+" "+http1
        elif(i.startswith("/")):
            p1=method+" "+"http://"+a1+i+" "+http1
        else:
            p1=method+" "+"http://"+a1+"/"+i+" "+http1       
        hash1=hashlib.sha256(p1.encode("utf8")).hexdigest()
        
        if hash1 not in classes.keys():
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            url2=socket.gethostbyname(a1)
            s2.connect((url2, port))
            p2=p1+"\nHost: ngn.cs.colorado.edu\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\nAccept-Language: en-US,en;q=0.5\nAccept-Encoding: gzip, deflate\nDNT: 1\nConnection: keep-alive\nUpgrade-Insecure-Requests: 1\nPragma: no-cache\nCache-Control: no-cache\n\n"
            s2.send(p2.encode("utf8"))
            response=s2.recv(65535)
            if(len(response)>0):
                classes[hash1]=response
                classes1[hash1]=z
                print("Prefetch Content==>"+p1)      #print("hash: "+hash1)
                print("length of dictionary: "+str(len(classes)))          

def call(a1, b1, port, http1, method, hash, conn):  #Responsible for serving requests after time out or new requests
    global classes, classes1
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:        
        url1=socket.gethostbyname(a1)
        s1.connect((url1, port))
    
        s1.send((method+" "+b1+" "+http1+"\nHost: ngn.cs.colorado.edu\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\nAccept-Language: en-US,en;q=0.5\nAccept-Encoding: gzip, deflate\nDNT: 1\nConnection: keep-alive\nUpgrade-Insecure-Requests: 1\nPragma: no-cache\nCache-Control: no-cache\n\n").encode("utf8"))
        
        response=s1.recv(65535) 
        if(len(response)>0):
            z=time.time()
            classes[hash]=response
            classes1[hash]=z     
            conn.send(response)
        print("length of dictionary: "+str(len(classes)))
        #t1=threading.Thread(target=mthread1, args=(a1, port, method, http1, z))
        #t1.start()
        mthread1(a1, port, method, http1, z)     
    except:        
        print("*****Error: 1)Please check your Internet connection OR 2) Invalid address entered.*****")  
        
def proxy(method, a1, b1, http1, conn, clientaddr, port):   #Responsible for serving requests from cache if within timeout
    read=method+" "+"http://"+a1+b1+" "+http1     #print("read:", read)
    hash=hashlib.sha256(read.encode("utf8")).hexdigest()   #print(hash+" "+read)
    if hash in classes.keys():
        z1=time.time()                     
        if((z1-classes1[hash])<sec):    
            conn.send(classes[hash])
            print("##=====Sent via cache=====##")
        else:               
            del classes[hash]
            print("Length of dictionary on deletion of key-value pair after timeout: "+str(len(classes)))
            print("Note: Time out. Data would be sent from server.")
            call(a1, b1, port, http1, method, hash, conn)  
    else:
        call(a1, b1, port, http1, method, hash, conn)
        
def mthread(conn, clientaddr):      #Responsible for parsing through the incoming requests for different parameters
    data=conn.recv(65535)
    data1=data.decode("utf8")
    firstline=data1.split("\n")[0]
    method=firstline.split(" ")[0]
    if (firstline==""):
        return(0)                     
    else:
        print("Main Content--->"+firstline)           #print("method:"+method)
        mainurl=firstline.split(" ")[1]         #print("mainurl:"+mainurl)
        pos=mainurl.find("://")             #print("pos of '://':"+str(pos))
        if (pos==-1):
            temp=mainurl            #print("temp if:"+temp)
        else:
            temp=mainurl[(pos+3):]          #print("temp:"+temp)
        server=temp.find("/")
        a1=temp[:server]            #print("Specific Url a1:"+str(a1))
        b1=temp[server:]            #print("Remaining path b1:"+str(b1))
        pos2=firstline.find("HTTP/1.")
        http1=firstline[(pos2):(pos2)+8]         #print("http:"+str(http1))
        port=80
        if(method=="GET"): 
            if((http1=="HTTP/1.1") or (http1=="HTTP/1.0")):
                proxy(method, a1, b1, http1, conn, clientaddr, port)
            else:
                print("Error1: 400 Bad Request.")
                conn.send((http1+" 400 Bad Request\n").encode("utf8"))     #Sends Error 400: Bad Request w.r.t HTTP Version
                conn.send(("Content-Type: text/html\n\n").encode("utf8"))
                e2=open("E400.html", "rb")
                resp3=e2.read()
                conn.send(resp3)
                e2.close()
                conn.close() 
        else:
            print("Error2: 400 Bad Request.")
            conn.send((http1+" 400 Bad Request\n").encode("utf8"))     #Sends Error 400: Bad Request w.r.t Method
            conn.send(("Content-Type: text/html\n\n").encode("utf8"))
            e2=open("E400.html", "rb")
            resp3=e2.read()
            conn.send(resp3)
            e2.close()
            conn.close()

if (len(sys.argv)==3):
    p=int(sys.argv[1])
    sec=int(sys.argv[2])
    classes={}
    classes1={}
    list1=[]
    
    if(p>=1024 and p<=65535):
        print("Success: Valid port entered.")
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", p))     
        print("Bind successful.")
    else:
        print("Error: Cannot bind as the port number is not in the valid range.")
        sys.exit()
        
    backlog=100
    s.listen(backlog)
    print("Socket now listening.")
    print("="*75)
        
    while True:
        s1=threading.Thread(target=mthread2)  #Keyboard Interrupt
        s1.start()
        conn, clientaddr=s.accept()
        #t=threading.Thread(target=mthread, args=(conn, clientaddr))
        mthread(conn, clientaddr)       #Main function
        #t.start()

else:
    print("Please enter 2 valid arguments- the .py file name(sys.argv[0]) and the valid port number(sys.argv[1]).")        