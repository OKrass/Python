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

NumberOfFrames = 50
Lock = thread.allocate_lock()
# Set amount of time between sending data in s
timeBetweenTransmission = 2
Data = []

def getData(queue):
        temp = []
        temp.append(queue.get)
        queue.task_done()
        return temp


    # Send data via TCP
def sendData(t, data):
    gettime = t
    print('Started sending messages')
    while True:
        if q.empty is 1:
            time.sleep(5)
        else:
            while not q.empty():
                Data = getData(q)
        if len(data) is 11:
            s.send(Data)
            time.sleep(gettime)
            try:
                answer = s.recv(buffersize)
                # Checking if sent information is same as received
                if (answer != Data):
                    print('messages do not match')
                    s.close()
                    sys.exit('error')

            except Exception:
                print('something went wrong')
                s.close()
            #Getting new information
            #informationToSent = getData()


            if Data:
                continue
            else:
                print 'no more data to %s\nclosing '%(TCP_IP)
                s.close()
                sys.exit(0)
            break

        else:
            continue
try:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #COnnecting to server using IP and Port
    s.connect((TCP_IP, TCP_PORT))
    print 'connecting to %s' % (TCP_IP)

    thread.start_new_thread(sendData, (timeBetweenTransmission, Data))
    thread.start_new_thread(ImageProcessing.RUN(NumberOfFrames, q))



except:
    print "Error: unable to start thread"
    sys.exit(1)
while 1:
   pass
