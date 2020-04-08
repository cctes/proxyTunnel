import socket
import requests
import re
import threading
import json

#testpx
#
timeout = 300
nodatatime = 5

def getPX():
    p = requests.get("http://127.0.0.1:5010/get/").json().get("proxy")
    p = str(p)
    ip = str(p.split(":")[0])
    port = int(p.split(":")[1])
    print("new ip is:" + ip + ":" + str(port))
    return ip,port


def targetToClient(conn,toPX):
    global timeout
    global nodatatime
    i = 0
    j = 0
    while i < timeout:
        try:
            data = toPX.recv(1024)
            if not data:
                if j > nodatatime:
                    conn.close()
                    toPX.close()
                    return
                j += 1
        except:
            if j > nodatatime:
                conn.close()
                toPX.close()
                return
            j += 1
            #print("get data from px error")
        try:
            conn.sendall(data)
        except:
            #print("send data to client error")
            pass

def clientToTarget(conn,toPX):
    global timeout
    global nodatatime
    j = 0
    i = 0
    while i < timeout:
        try:
            data = conn.recv(1024)
            if not data:
                if j > nodatatime:
                    conn.close()
                    toPX.close()
                    return
                j += 1
        except:
            if j > nodatatime:
                conn.close()
                toPX.close()
                print("close")
                return
            j += 1
            print("get data from client error")
        try:
            toPX.sendall(data)
        except:
            print("send data to px error")
        i += 1


def AConnectFromClient(conn,addr):
    print("new connect from client")
    #pxip = "218.75.158.153"
    #pxport = 3128

    pxip,pxport = getPX()
    try:
        toPX = socket.socket()
        toPX.connect((pxip,pxport))
    except:
        print("connect px error")
    threading.Thread(target=clientToTarget,args=(conn,toPX)).start()
    threading.Thread(target=targetToClient,args=(conn,toPX)).start()



if __name__ == "__main__":
    sever = socket.socket()
    host = "127.0.0.1"
    port = 3080
    sever.bind((host,port))

    sever.listen(20)
    print("sever is ok!!")
    while True:
        try:
            conn,addr = sever.accept()
            threading.Thread(target=AConnectFromClient,args=(conn,addr)).start()
        except:
            print("connect from client error")
