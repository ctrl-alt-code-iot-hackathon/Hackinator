import cv2
import numpy as np

img = cv2.imread('fence3.jpeg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
edges = cv2.GaussianBlur(edges,(5,5),0)

k_square = np.ones((5,5),np.uint8)
k_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
thresh = cv2.dilate(edges,k_ellipse,iterations=1)
thresh = cv2.erode(thresh,k_square,iterations=2)
minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(thresh,1,np.pi/180,100,minLineLength,maxLineGap)
s=0
if lines is not None:
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
           
cv2.imshow('houghlin',img)

cv2.waitKey(0)
cv2.destroyAllWindows()
