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
buffersize = 256
Data1 = []
NumberOfFrames = 50
# Set amount of time between sending data in s
timeBetweenTransmission = 2


def getData(queue):
        temp = []
        temp.append(queue.get)
        queue.task_done()
        return temp


    # Send data via TCP
def sendData(t, data, q, socket):
    gettime = t
    print('Started sending messages')
    while True:
        '''
        if q.empty is 1:
            time.sleep(5)
        else:
            while not q.empty():
                Data = getData(q)
                '''
        Data = [1,2,3,4,5,6,7,8,9,10,11]
        if len(Data) is 11:
            datatosend = ''.join(str(x) for x in Data)
            socket.send(datatosend)
            time.sleep(gettime)
            try:
                answer = socket.recv(buffersize)
                # Checking if sent information is same as received
                if (answer != datatosend):
                    print('messages do not match')
                    socket.close()
                    sys.exit('error')

            except Exception:
                print('something went wrong')
                socket.close()
            #Getting new information
            #informationToSent = getData()


            if Data:
                continue
            else:
                print 'no more data to %s\nclosing '%(TCP_IP)
                socket.close()
                sys.exit(0)
            break

        else:
            continue
try:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #COnnecting to server using IP and Port
    s.connect((TCP_IP, TCP_PORT))
    print 'connecting to %s' % (TCP_IP)

    a = thread.start_new_thread(sendData, (timeBetweenTransmission, Data1, q, s))
    b = thread.start_new_thread(ImageProcessing.RUN(NumberOfFrames, q))




except:
    print "Error: unable to start thread"
    sys.exit(1)
while 1:
   pass
