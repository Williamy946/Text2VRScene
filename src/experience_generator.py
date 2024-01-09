'''
Author: William Zhizhuo Yin
Data: 07/04/2023
'''

import os
import webbrowser

# Credit to Max Shvedov at https://stackoverflow.com/questions/51189628/simple-http-server-in-python-how-to-get-files-from-dir-path
# Forgot where else I picked up code

import http.server
import socketserver
from os import path

my_host_name = 'localhost'
my_port = 8888
html_folder = 'tmp_file/myheartwillgoon'
webfile = ""

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', path.getsize(self.getPath()))
        self.end_headers()

    def getPath(self):
        if self.path == '/':
            content_path = path.join(
                html_folder, webfile)
        else:
            content_path = path.join(html_folder, str(self.path).split('?')[0][1:])
        return content_path

    def getContent(self, content_path):
        with open(content_path, mode='rb') as f:
            content = f.read()
        return content

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self.getContent(self.getPath()))

def experience_generator(code, literature, is_test):

    if not os.path.exists("tmp_file/"+str(literature)):
        os.makedirs("tmp_file/"+str(literature))

    if os.path.exists("tmp_file/"+str(literature)+"/experience.html"):
        os.remove("tmp_file/"+str(literature)+"/experience.html")
    cur_html = "tmp_file/"+str(literature)+"/experience.html"

    # Store the code into the html file
    file = open(cur_html, 'w')
    file.write(code)
    file.close()
    global html_folder
    global webfile
    html_folder = "tmp_file/" + str(literature) + "/"
    if not is_test:
        webfile = "experience.html"
    else:
        webfile = "experience.html"
    my_handler = MyHttpRequestHandler
    #if is_test == False:
    with socketserver.TCPServer(("", my_port), my_handler) as httpd:
        print("Http Server Serving at port", my_port)
        webbrowser.open("http://localhost:8888")
        httpd.serve_forever()

if __name__ == "__main__":
    webfile = "experience.html"
    html_folder = 'samples/myheartwillgoon'
    my_handler = MyHttpRequestHandler
    with socketserver.TCPServer(("", my_port), my_handler) as httpd:
        print("Http Server Serving at port", my_port)
        webbrowser.open("http://localhost:8888")
        httpd.serve_forever()


