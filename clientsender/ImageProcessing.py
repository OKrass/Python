import numpy as np
import cv2 as cv
import Queue
import threading
Blue = []
Green = []
Red = []

# Set Number of Frames between 50 - 350
NumberOfFrames = 20

# Getting mean of an image and later adding it to an array


def ArrayAppend(ColorFrame, ChannelName):
    l = ColorFrame.mean()
    ChannelName.append(l)
    return ChannelName


# Splitting image and using ArrayAppend to add mean value ro


def ImageSplit(ROI):
    b, g, r = cv.split(ROI)
    BlueArraytemp = ArrayAppend(b, Blue)
    GreenArraytemp = ArrayAppend(g, Green)
    RedArraytemp = ArrayAppend(r, Red)
    return BlueArraytemp, GreenArraytemp, RedArraytemp


def GetArrayMean(ColorArray):
    JustinCase = ColorArray
    MeanOfArray = np.mean(JustinCase)
    return MeanOfArray


def FFT(ChannelArray):
    a = np.fft.fft(ChannelArray)
    b = np.absolute(a)
    temp = []
    for i in range(0, len(b)):
        a = b[i]
        k = '{:.2f}'.format(a)
        z = float(k)
        temp.append(z)
    return temp

    # FFT dor all 3 channels
def ChannelFFT(BlueArray, GreenArray, RedArray):
    Tempb = BlueArray
    Tempg = GreenArray
    Tempr = RedArray
    blueFFT = FFT(Tempb)
    greenFFT = FFT(Tempg)
    redFFT = FFT(Tempr)
    return blueFFT, greenFFT, redFFT


# Preparing data which are going to be sent
def DataToSend(BlueArray, GreenArray, RedArray, i):
    counter = i
    check = counter % 10
    MeanOfBlue = GetArrayMean(BlueArray)
    MeanOfGreen = GetArrayMean(GreenArray)
    MeanOfRed = GetArrayMean(RedArray)

    if check == 9:
        BlueFFT, GreenFFT, RedFFT = ChannelFFT(BlueArray, GreenArray, RedArray)
        temp1 = [MeanOfBlue, MeanOfGreen, MeanOfRed, Meanof3channels(MeanOfBlue, MeanOfGreen, MeanOfRed)]
        return temp1, 1, BlueFFT, GreenFFT, RedFFT
    else:
        BlueFFT, GreenFFT, RedFFT = ChannelFFT([0],[0],[0])
        temp = []
        return temp, 0, BlueFFT, GreenFFT, RedFFT


def Meanof3channels(MeanOfblue, MeanOfgreen, MeanOfred):
    temp = [MeanOfblue, MeanOfgreen, MeanOfred]
    Meanof3channels = GetArrayMean(temp)
    return Meanof3channels


def PutAllDataInQueue(Queue,Color, New, Mean, BFFT, GFFT, RFFT):

    Queue.put("{:.5f}".format(Color[0]))
    Queue.put("{:.5f}".format(Color[1]))
    Queue.put("{:.5f}".format(Color[2]))
    Queue.put(New)
    if not Mean:
        Queue.put(0)
        Queue.put(0)
        Queue.put(0)
        Queue.put(0)
    else:
        Queue.put("{:.5f}".format(Mean[0]))
        Queue.put("{:.5f}".format(Mean[1]))
        Queue.put("{:.5f}".format(Mean[2]))
        Queue.put("{:.5f}".format(Mean[3]))
    Queue.put(BFFT)
    Queue.put(GFFT)
    Queue.put(RFFT)


def ArrayClearing():
    return 0, 0, 0

def RUN(NumberOfFrames,q):

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
        if count > NumberOfFrames:

            # Clearing Arrays and counter
            del BlueArray[:], GreenArray[:], RedArray[:], Blue[:], Red[:], Green[:]
            BlueFFT, GreenFFT, RedFFT = ArrayClearing()
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
                # Splitting image and getting mean of a frame into arrays
                BlueArray, GreenArray, RedArray = ImageSplit(roi)
                BGR = [BlueArray[count], GreenArray[count], RedArray[count]]
                # getting all needed information
                mean, isnew, msgBlueFFT, msgGreenFFT, msgRedFFT = DataToSend(BlueArray, GreenArray, RedArray, count)
                # Putting all data in queue
                PutAllDataInQueue(q, BGR, isnew, mean, msgBlueFFT, msgGreenFFT, msgRedFFT)

                BGR = []
                count += 1
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

    cv.destroyAllWindows()
    cap.release()
