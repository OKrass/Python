import socket

import time
import thread
# Put your IP and port here
TCP_IP = '127.0.0.1'
TCP_PORT = 3001
buffersize = 128
#Data which are going to be sent
data = 'some data\t'
#Function to get data later
def getData():
    data = 0
    return data
    # Send data via TCP
def sendData(data,t):
    gettime = t
    informationToSent = data
    while True:
        s.send(informationToSent)
        time.sleep(gettime)
        try:
            answer = s.recv(buffersize)
        except Exception:
            print('something went wrong')
        #Getting new information
        informationToSent = getData()


        if informationToSent:
            continue
        else:
            print 'no more data to %s\nclosing '%(TCP_IP)
            s.close()
            break

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #COnnecting to server using IP and Port
    s.connect((TCP_IP, TCP_PORT))
    print 'connecting to %s' % (TCP_IP)

    # Set amount of time between sending data in s
    thread.start_new_thread(sendData, (data, 5,))
except:
    print "Error: unable to start thread"

while 1:
   pass






