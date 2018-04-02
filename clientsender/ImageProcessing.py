import numpy as np
import cv2 as cv

Blue = []
Green = []
Red = []
count = 0

#Set Number of Frames between 50 - 350
NumberOfFrames = 5

#Getting mean of an image and later adding it to an array
def ArrayAppend(ColorFrame,ChannelName):
    l = ColorFrame.mean()
    ChannelName.append(l)
    return ChannelName
#Splitting image and using ArrayAppend to add mean value ro
def ImageSplit(roi):
    b, g, r = cv.split(roi)
    BlueArray = ArrayAppend(b, Blue)
    GreenArray = ArrayAppend(g, Green)
    RedArray = ArrayAppend(r, Red)
    return BlueArray, GreenArray, RedArray

def GetArrayMean(ColorArray):
    JustinCase = ColorArray
    MeanOfArray = np.mean(JustinCase)
    return MeanOfArray

def FFT(ChannelArray):
    return np.fft.fft(ChannelArray)
    #FFT dor all 3 channels
def ChannelFFT(BlueArray, GreenArray, RedArray):
    Tempb = BlueArray
    Tempg = GreenArray
    Tempr = RedArray
    BlueFFT = FFT(Tempb)
    GreenFFT = FFT(Tempg)
    RedFFT = FFT(Tempr)
    return BlueFFT ,GreenFFT, RedFFT
#Preparing data which are going to be sent
def DataToSend(BlueArray, GreenArray, RedArray):
    MeanOfBlue = GetArrayMean(BlueArray)
    MeanOfGreen = GetArrayMean(GreenArray)
    MeanOfRed = GetArrayMean(RedArray)
    temp = [MeanOfBlue, MeanOfGreen, MeanOfRed]
    Meanof3channels = GetArrayMean(temp)
    temp = [MeanOfBlue, MeanOfGreen, MeanOfRed, Meanof3channels]
    return temp

def ArrayClearing():
    return 0, 0, 0

#set number of frames

cap = cv.VideoCapture(0)
# take first frame of the video
ret, frame = cap.read()
# setup initial location of window
c, r, w, h = cv.selectROI('Image', frame)
track_window = (c, r, w, h)
# set up the ROI for getting info
roi = frame[r:r+h, c:c+w]

# Crop image
while(1):
    if count > NumberOfFrames:
        BlueFFT, GreenFFT, RedFFT = ChannelFFT(BlueArray, GreenArray, RedArray)
        Message = DataToSend(BlueArray, GreenArray, RedArray)
        #Clearing Arrays and counter
        BlueArray, GreenArray, RedArray = ArrayClearing()
        BlueFFT, GreenFFT, RedFFT = ArrayClearing()
        count = 0
        continue
    else:
        ret ,frame = cap.read()
        if ret == True:
            #Getting video from selected location
            x, y, w, h = track_window
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = frame[y:y + h, x:x + w]
            cv.imshow('dst', roi)
            # Spliting image and getting mean of a frame into arrays
            BlueArray, GreenArray, RedArray = ImageSplit(roi)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
        count += 1
cv.destroyAllWindows()
cap.release()

