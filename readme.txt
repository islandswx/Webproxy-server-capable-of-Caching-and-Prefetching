Author: Pranit Yadav
Python version: 3.5.2
Third Socket Programming Assignment

Functionality:
1)Python 3.0-3.5 has been used for this code.
2)The functionality of this code is to serve as a proxy. Basically its a proxy server. The requests from the web-browser(client) would reach the server via this proxy.
3)On the command prompt we have to enter the following to run the code- python  <filename.py>  <1024<=port number<=65535 >  <timeout for caching purposes>.
4)On entering the above command, the browser gets connected to the proxy server. Any requests that the browser makes are forwarded to the proxy which in turn forwards to the server which serves it accordingly.
5)In this code, only those sites are served which are connected to port 80, i.e., only HTTP requests are served.
6)Once the server serves the requests, all those requests are stored in the cache for the time that you mention in point 3. <timeout for caching purposes>
7)Within the timeout, even if the Internet is turned OFF or ON, all the responses stored in the cache would be served if they are requested. Once timeout value exceeds, all the requests are served from the server and not cache. 
8)Dictionary(hashes) is used for caching purposes. Here the dictionary named classes is used. The request (the first line, for eg:- GET http://google.com HTTP/1.0) from the web-browser is converted to a hash value by using the sha256 function. It serves as the key whereas its response from the server acts as the value. On making the same request within the timeout, same hash would be generated and so its response(value) would be served from the cache. A different request would generate a different hash and so it would be served from the server and then this new request-response(key-value pair) would be added to the exisiting dictionary.
9)Also, prefetching has been done in this code. The hyperlinks are fetched from the existing page using BeautifulSoup. Once the first request is made by the browser(this is the time when the code runs completely for 1 time), a thread is invoked which fetches all the hyperlinks, sends requests from all those hyperlinks to browser and receives its responses. These requests-reponses(key-values) are again added to the existing dictionary(classes).
10)For timeout purposes, a different dictionary is used namely classes1. A time is recorded using time.time() function when a new request is made. Again when the same request is made, the new time is noted. If the difference between new and old time is within the timeout(point 3), respones are served from cache, else from the server.
11)This proxy server fucntions properly for HTTP/1.0 as well as HTTP/1.1 version. The HTTP version can be changed in Firefox using about:config. Also, it serves only GET requests. For other requests and for other HTTP versions besides HTTP/1.0 and HTTP/1.1, a 400 BAD REQUEST error is reported.
12)Keyboard interrupt has been handled too(Ctrl+C).

Note:- webproxy.py serves purely for HTTP/1.0 versions. webproxy1.py serves HTTP/1.0 and HTTP/1.1 version. (HTTP/1.1 requires the header HOST to be included in it)