import cv2
import numpy as np
import math
import serial
import time

ser=serial.Serial("/dev/ttyAMA0",9600)
ser.baudrate(9600)
from matplotlib import pyplot as plt

def nothing(x):
    pass;
cap=cv2.VideoCapture(0)

window1="Original"
window2="Threshold"
cv2.namedWindow(window1,cv2.WINDOW_NORMAL)
#cv2.namedWindow("Smooth",cv2.WINDOW_NORMAL)
#cv2.namedWindow(window2,cv2.WINDOW_NORMAL)
#cv2.namedWindow("Thres2",cv2.WINDOW_NORMAL)
#cv2.createTrackbar("Kernel",window2,0,17,nothing)
l=352
w=640
def check():
    orient=1;drift=0
    global x_c_up,y_c_up,x_c_low,y_c_low,l,w
    x_mean=x_c_up+x_c_low
    drift_error=x_mean-w/2
    
    orient_error=x_c_up-x_c_low
    error=orient*orient_error+drift*drift_error
    if error>0:
        print 'left'
        ser.write('0')
    else:
        print 'right'
        ser.write('1')
    

    

out = cv2.VideoWriter('/home/kunal/Videos/outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (w,l))
while (1):
    ret,frame =cap.read()

    if(ret==False):
        break;
    out.write(frame)
    r,g,b = cv2.split(frame);                                                    # Splitting of colour channels
    #kernel=cv2.getTrackbarPos("Kernel",window2)
    
    #if not(kernel%2):
    #    kernel=kernel+1;
    #kernel=max(3,kernel); 
    
    kernel=17
    smoothed = cv2.GaussianBlur(r,(kernel,kernel),0);                             # Smoothing the r channel of the video to reduce noise
    ret1,th1 = cv2.threshold(r,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)           # Using OTSU Thresholding method to get binary image 
    #ret2,th2 = cv2.threshold(smoothed,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    M_low=cv2.moments(th1[l/2:l,0:w])                                             # Calculating moments for finding blobs , we have used two blobs 
    if M_low['m00']!=0:
        x_c_low=int(M_low['m10']/M_low['m00'])
        y_c_low=int(M_low['m01']/M_low['m00'])+l/2
    else:
        x_c_low=0;y_c_low=0
    M_up=cv2.moments(th1[0:l/2,0:w])
    if M_up['m00']!=0:
        x_c_up=int(M_up['m10']/M_up['m00'])
        y_c_up=int(M_up['m01']/M_up['m00'])
    else:
        x_c_up=0;y_c_up=0

    cv2.circle(frame, (x_c_low,y_c_low), 10, (0,0,255),5) 
    cv2.circle(frame, (x_c_up,y_c_up), 10, (255,0,0),5)
    check();
    
    cv2.imshow("Original",frame)
    #cv2.imshow("Smooth",smoothed)
    #cv2.imshow("Threshold",th1)
    #cv2.imshow("Thres2",th2)
    print frame.shape
    if(cv2.waitKey(10)==27):
        break;
out.release()
cap.release()
cv2.destroyAllWindows()

