import numpy as np
import cv2 as cv
import socket
import sys
import time
import Queue

Blue = []
Green = []
Red = []
queue = Queue.Queue()
# set IP and Port
TCP_IP = '127.0.0.1'
TCP_PORT = 3001
buffersize = 1024
Data1 = []

# Set amount of time between sending data in s
timeBetweenTransmission = 2
# Set Number of Frames between 50 - 350
NumberOfFrames = 20

# Getting mean of an image and later adding it to an List




    # Send data via TCP


def sendData(t, Data, q, socket):
    gettime = t
  #  print('Started sending messages')

    Data = []
    if q.empty is 1:
        time.sleep(5)
    else:
        while not q.empty():
            Data.append(q.get())
            Data.append(';\n ')

    if len(Data) is 22:
        datatosend = ''.join(str(x) for x in Data)
        socket.send(datatosend)

        try:
            answer = socket.recv(buffersize)
            time.sleep(gettime)
            # Checking if sent information is same as received
            '''
            if (answer != datatosend):

                print('messages do not match')
                socket.close()
                sys.exit('error')
'''
        except Exception:
            print('something went wrong')
            socket.close()



            
def ListAppend(ColorFrame, ChannelName):
    l = ColorFrame.mean()
    ChannelName.append(l)
    return ChannelName


# Splitting image and using ListAppend to add mean value ro


def ImageSplit(ROI):
    b, g, r = cv.split(ROI)
    BlueListtemp = ListAppend(b, Blue)
    GreenListtemp = ListAppend(g, Green)
    RedListtemp = ListAppend(r, Red)
    return BlueListtemp, GreenListtemp, RedListtemp


def GetListMean(ColorList):
    JustinCase = ColorList
    MeanOfList = np.mean(JustinCase)
    return MeanOfList


def FFT(ChannelList):
    return np.fft.fft(ChannelList)

    # FFT dor all 3 channels
def ChannelFFT(BlueList, GreenList, RedList):
    Tempb = BlueList
    Tempg = GreenList
    Tempr = RedList
    blueFFT = FFT(Tempb)
    greenFFT = FFT(Tempg)
    redFFT = FFT(Tempr)
    return blueFFT, greenFFT, redFFT


# Preparing data which are going to be sent
def DataToSend(BlueList, GreenList, RedList, i):
    counter = i
    check = counter % 10
    MeanOfBlue = GetListMean(BlueList)
    MeanOfGreen = GetListMean(GreenList)
    MeanOfRed = GetListMean(RedList)
    # For i = 9 we are sending all information ( mean of 3 channels(r,g,b), mean of mean of (r,g,b), FFT of 3 channels )
    if check == 9:
        BlueFFT, GreenFFT, RedFFT = ChannelFFT(BlueList, GreenList, RedList)
        temp1 = [MeanOfBlue, MeanOfGreen, MeanOfRed, Meanof3channels(MeanOfBlue, MeanOfGreen, MeanOfRed)]
        return temp1, 1, BlueFFT, GreenFFT, RedFFT
    else:
        BlueFFT, GreenFFT, RedFFT = ChannelFFT([0],[0],[0])
        temp = []
        return temp, 0, BlueFFT, GreenFFT, RedFFT


def Meanof3channels(MeanOfblue, MeanOfgreen, MeanOfred):
    temp = [MeanOfblue, MeanOfgreen, MeanOfred]
    Meanof3channels = GetListMean(temp)
    return Meanof3channels


def PutAllDataInQueue(Queue,Color, New, Mean, BFFT, GFFT, RFFT):

    Queue.put(Color[0])
    Queue.put(Color[1])
    Queue.put(Color[2])
    Queue.put(New)
    if not Mean:
        Queue.put(0)
        Queue.put(0)
        Queue.put(0)
        Queue.put(0)
    else:
        Queue.put(Mean[0])
        Queue.put(Mean[1])
        Queue.put(Mean[2])
        Queue.put(Mean[3])
    Queue.put(BFFT)
    Queue.put(GFFT)
    Queue.put(RFFT)

def ListClearing():
    return 0, 0, 0

def RUN(NumberofFrames,q,IP,Port,timebtwtrans):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # COnnecting to server using IP and Port
    s.connect((IP, Port))
    print 'connecting to %s' % (TCP_IP)
    count = 0
    cap = cv.VideoCapture(0)
    while 1:
        reg, video = cap.read()
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(video, 'Press q when ready to choose area', (30, 40), font, 1, (255, 255, 0), 2, cv.LINE_AA)
        cv.imshow('Video', video)

        # Press q if ready to continue
        if cv.waitKey(1) & 0xFF == ord('q'):
            # closing useless window
            cv.destroyAllWindows()
            break
    # take first frame of the video
    ret, frame = cap.read()
    # setup initial location of window
    c, r, w, h = cv.selectROI('Image', frame, 0)
    track_window = (c, r, w, h)
    # set up the ROI for getting info
    roi = frame[r:r+h, c:c+w]
    # closing useless window
    cv.destroyAllWindows()
    # Crop image
    while 1:
        if count > NumberofFrames:

            # Clearing Lists and counter
            del BlueList[:], GreenList[:], RedList[:], Blue[:], Red[:], Green[:]
            BlueFFT, GreenFFT, RedFFT = ListClearing()
            count = 0
            continue
        else:
            ret, frame = cap.read()
            if ret is True:
                # Getting video from selected location
                x, y, w, h = track_window
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi = frame[y:y + h, x:x + w]

                cv.imshow('dst', roi)
                # Splitting image and getting mean of a frame into Lists
                BlueList, GreenList, RedList = ImageSplit(roi)
                BGR = [BlueList[count], GreenList[count], RedList[count]]
                # getting all needed information
                mean, isnew, msgBlueFFT, msgGreenFFT, msgRedFFT = DataToSend(BlueList, GreenList, RedList, count)
                # Putting all data in queue
                PutAllDataInQueue(q, BGR, isnew, mean, msgBlueFFT, msgGreenFFT, msgRedFFT)
                # Data format: mean of 1 image (b,g,r) ; isNew ; Mean of n images (b,g,r) ; BFFT ; GFFT ; RFFT ;
                sendData(timebtwtrans, Data1, q, s)
                BGR = []
                count += 1
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

    cv.destroyAllWindows()
    cap.release()


RUN(NumberOfFrames,queue,TCP_IP,TCP_PORT,timeBetweenTransmission)