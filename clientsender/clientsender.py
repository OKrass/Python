import socket
import sys
import time
# Put your IP and port here
TCP_IP = '127.0.0.1'
TCP_PORT = 3001
#Data which are going to be sent
data = 'some data\t'
#function to fill later
def getData():
    data = 0
    return data
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #COnnecting to server using IP and Port
    s.connect((TCP_IP, TCP_PORT))
    print >> sys.stderr, 'connection from', TCP_IP
        # Send data via TCP
    while True:
        s.send(data)
        data = getData()
        #Set amount of time between sending data in s
        time.sleep(5)
        if data:
            continue
        else:
            print >> sys.stderr, 'no more data to', TCP_IP
            break



finally:
     # Clean up the connection
    s.close()



