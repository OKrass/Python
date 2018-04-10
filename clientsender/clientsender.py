import socket
import sys
import time
import thread
import ImageProcessing
import Queue


# Put your IP and port here
q = Queue.Queue()
TCP_IP = '127.0.0.1'
TCP_PORT = 3001
buffersize = 8192
Data1 = []
NumberOfFrames = 300
# Set amount of time between sending data in s
timeBetweenTransmission = 0.01
# For 0.01 s program sends current values



    # Send data via TCP
def sendData(t, q, socket):
    gettime = t
    count = 0
    print('Started sending messages')
    while True:
        Data = []
        if q.empty is 1:
            time.sleep(5)
        else:
            while not len(Data) is 22:
                Data.append(q.get())
                Data.append(';\n ')

            datatosend = ''.join(str(x) for x in Data)
            socket.send(datatosend)
            try:
                answer = socket.recv(buffersize)
                if len(answer) >= 8192:
                    print ('Too many digits')
                    break
                else:
                # Checking if sent information is same as received
                    if (answer != datatosend):
                        print('messages do not match')
                        socket.close()
                        sys.exit('error')
                time.sleep(gettime)

            except Exception:
                print('something went wrong')
                socket.close()


            if Data:
                continue
            else:
                print 'no more data to %s\nclosing '%(TCP_IP)
                socket.close()
                sys.exit(0)
            break

try:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #COnnecting to server using IP and Port
    s.connect((TCP_IP, TCP_PORT))
    print 'connecting to %s' % (TCP_IP)

    a = thread.start_new_thread(sendData, (timeBetweenTransmission, q, s))
    b = thread.start_new_thread(ImageProcessing.RUN(NumberOfFrames, q))




except:
    print "Error: unable to start thread"
    sys.exit(1)
while 1:
   pass
