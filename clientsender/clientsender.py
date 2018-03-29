import socket
import sys
import time
import thread
# Put your IP and port here
TCP_IP = '127.0.0.1'
TCP_PORT = 3001
buffersize = 256
# Set amount of time between sending data in s
timeBetweenTransmission = 2
#Data which are going to be sent
data = 'SOME RATA'
#Function to get data later
def getData():
    data = 0
    return data
    # Send data via TCP
def sendData(data,t):
    gettime = t
    informationToSent = data
    print('Started sending messages')
    while True:

        s.send(informationToSent)

        time.sleep(gettime)
        try:
            answer = s.recv(buffersize)
            #Checking if sent information is same as recieved
            if (answer != informationToSent):
                print('messages do not match')
                s.close()
                sys.exit(0)



        except Exception:
            print('something went wrong')
            s.close()
        #Getting new information
        #informationToSent = getData()


        if informationToSent:
            continue
        else:
            print 'no more data to %s\nclosing '%(TCP_IP)
            s.close()
            sys.exit(0)
        break

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #COnnecting to server using IP and Port
    s.connect((TCP_IP, TCP_PORT))
    print 'connecting to %s' % (TCP_IP)
    thread.start_new_thread(sendData, (data, timeBetweenTransmission,))
except:
    print "Error: unable to start thread"
    sys.exit(1)
while 1:
   pass






