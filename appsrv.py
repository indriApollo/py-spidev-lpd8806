#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process, Value, Array
from ledEffects import ledEffects

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8000

class processHandler:

    def __init__(self):
        self.flag = Value("i", 1)
        self.shared = Array("i",[0,0,0,0])
        self.le = ledEffects(32)
        self.p = 0

    def killProc(self):
        if self.p and self.p.is_alive():
            self.flag.value = 0
            self.p.join()
            self.p = 0
            self.flag.value = 1
            print("killed previous process")
        else:
            print("no process to kill")

    def spawnProc(self,pname,params):
        if pname == "unicorn":
            self.killProc()
            alt = params["alt"]
            self.p = Process(target=self.le.unicorn, name=pname, args=(self.flag,alt))
            self.p.start()
            print("spawned process %s with alt %i" % (pname,alt))

        elif pname == "custom":

            r = params["r"]
            g = params["g"]
            b = params["b"]
            alt = params["alt"]

            self.shared[0] = r
            self.shared[1] = g
            self.shared[2] = b
            self.shared[3] = alt

            if self.p and self.p.name == "custom":
                #tell process to load new values
                self.flag.value = 1
                print("reload process %s with %i,%i,%i alt %i" % (pname,r,g,b,alt))
            else:
                self.killProc()
                self.p = Process(target=self.le.custom, name=pname, args=(self.flag,self.shared))
                self.p.start()
                print("spawned process %s with %i,%i,%i alt %i" % (pname,r,g,b,alt))

        elif pname == "reset":
            self.killProc()
            self.le.reset()
            print("reset")
        

class httpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        split = self.path.split("/")
        cmd = split[1]

        if cmd == "unicorn":
            alt = int(split[2])
            proc.spawnProc("unicorn",{"alt":alt})
        elif cmd == "custom":
            r = int(split[2])
            g = int(split[3])
            b = int(split[4])
            alt = int(split[5])
            proc.spawnProc("custom",{"r":r,"g":g,"b":b,"alt":alt})
        elif cmd == "reset":
            proc.spawnProc("reset",{})
        
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write( bytes('{"path":"%s"}' % (self.path), "utf8") )
        

if __name__ == '__main__':

    proc = processHandler()
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), httpHandler)
    print("Server started at %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
