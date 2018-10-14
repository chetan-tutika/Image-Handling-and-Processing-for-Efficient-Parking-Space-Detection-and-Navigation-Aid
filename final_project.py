import sys
import dropbox

from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

import numpy as np
import argparse
import cv2
import mahotas
import d_up1 
import d_up2


ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="Path to the image")
args=vars(ap.parse_args())

image=cv2.imread(args["image"])
ims = cv2.resize(image, (960, 540))
imss11=ims.copy()
cv2.imshow("Image",ims)
l = []
image=cv2.cvtColor(ims,cv2.COLOR_BGR2GRAY)
#blurred=cv2.GaussianBlur(image,(5,5),0)
#cv2.imshow("blur",blurred)


blurred=cv2.GaussianBlur(image,(3,3),0)
cv2.imshow("blur",blurred)
(T,thresht)=cv2.threshold(blurred,120,255,cv2.THRESH_TRUNC)
#cv2.imshow("threshtru",thresht)

canny=cv2.Canny(thresht,130,160)
kernel = np.ones((1,2),np.uint8)

thresh = cv2.erode(canny, kernel, iterations=1)
thresh = cv2.dilate(thresh, None, iterations=2)
#opening = cv2.morphologyEx(canny, cv2.MORPH_OPEN, kernel)
#cv2.imshow("CAnny",thresh)

(_,cnts,_)=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
print("I count {} in this image".format(len(cnts)))
cars=thresh.copy()
j=1
cv2.imshow("cars",cars)
for (i,c) in enumerate(cnts):
    A=cv2.contourArea(c)
    (x,y,w,h)=cv2.boundingRect(c)
    if A<70 :
        #mask=np.ones(ims.shape[:2],dtype="uint8")
        thresh[y:y+h,x:x+w]=0
    if y>270:
        #mask=np.ones(ims.shape[:2],dtype="uint8")
        thresh[y:y+h,x:x+w]=0
        
#cv2.imshow("thresh",thresh)

(_,cnts,_)=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
print("I count {} in this image".format(len(cnts)))
for (i,c) in enumerate(cnts):
    (a,b),(MA,ma),angle = cv2.fitEllipse(c)
    #print(MA)
    print(angle)
    if angle>80 and angle <100:
        (x,y,w,h)=cv2.boundingRect(c)
        if y<120:
            mask=np.ones(ims.shape[:2],dtype="uint8")
            thresh[y:y+h,x:x+w]=0
cv2.imshow("hresh",thresh)

(_,cnts,_)=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
##print("yyyyyyyyyyyyyyyyyyyyyyy")
##for (i,c) in enumerate(cnts):
##    (a,b),(MA,ma),angle = cv2.fitEllipse(c)
##    #print(MA)
##    print(angle)
##    if angle>65 and angle <82:
##        (x,y,w,h)=cv2.boundingRect(c)
##        mask=np.ones(ims.shape[:2],dtype="uint8")
##        thresh[y:y+h,x:x+w]=0
        
cv2.imshow("hresh1",thresh)
print("cntsss",len(cnts))
if len(cnts)>5:
    xa=[]
    ya=[]
    xa1=[]
    ya1=[]
    for (i,c) in enumerate(cnts) :
        (x,y,w,h)=cv2.boundingRect(c)
        xa.append(x)
        ya.append(y)
##        epsilon = 0.1*cv2.arcLength(c,True)
##        approx = cv2.approxPolyDP(c,epsilon,True)
##        cv2.drawContours(ims,[approx],-1,(0,255,0),3)


    S=sorted(ya,reverse=True)[0]
    S1=sorted(ya)[0]
    S2=sorted(xa,reverse=True)[0]
    S3=sorted(xa)[0]
    print("S",S)
    print("s3",S3)
    #(_,cnts,_)=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    if S>=173 and S<=300:
        Ab=1
        for (i,c) in enumerate(cnts) :
            (x,y,w,h)=cv2.boundingRect(c)
            if S1>30:
                S1=50
            if y==S:
                (x1,y1,w1,h1)=cv2.boundingRect(c)
        thresh=thresh[S1:S+h1,:]
        imss=ims.copy()
        imss=imss[S1:S+2*h1,:]
        print("S1",S1)
    else:
        S1=72
        S=270
        h1=31
        thresh=thresh[S1-h1:S+h1,:]
        imss=ims.copy()
        imss=imss[S1-int(1.5*h1):S+int(1.5*h1),:]
        cv2.imshow("imss",thresh)
    
    (_,cnts,_)=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    xa=[]
    ya=[]
    xa1=[]
    ya1=[]
    for (i,c) in enumerate(cnts) :
        (x,y,w,h)=cv2.boundingRect(c)
        xa.append(x)
        ya.append(y)
##        epsilon = 0.1*cv2.arcLength(c,True)
##        approx = cv2.approxPolyDP(c,epsilon,True)
##        cv2.drawContours(ims,[approx],-1,(0,255,0),3)


    S=sorted(ya,reverse=True)[0]
    S1=sorted(ya)[0]
    S2=sorted(xa,reverse=True)[0]
    S3=sorted(xa)[0]
    for (i,c) in enumerate(cnts) :
        (x,y,w,h)=cv2.boundingRect(c)
        if x==S3:
            (x1,y1,w1,h1)=cv2.boundingRect(c)
    print("x1",x1)
    x2=x1
    if x1<=132 and x1>30:
        z=1
        
        theta=80
        while (x1<960):
            if x1>70:
                x1=x1-int(x2/1.6)
            if S1-h1>0:
                ims1=thresh[S1-h1:S+h1,x1:x1+150]
                H=S+h1-S1+h1
            else:
                ims1=thresh[S1:S+h1,x1:x1+150]
                H=S-S1+h1
                
            (_,cnts,_)=cv2.findContours(ims1.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            print("cnts",len(cnts))
            cX=((x1+x1+150)*0.5)+15
            cY=(S1+h1+S)*0.5+23
            W=(x1+170)-(x1-int(0.05*w1))
            if len(cnts)>=1:
                
                rect=((cX,cY),(H,W),theta)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(imss,[box],0,(0,0,255),2)
                cv2.drawContours(imss11,[box],0,(0,0,255),2)
                c="1"
                l.append(c)
        #cv2.rectangle(imss,(x1-int(0.05*w1),S1-h1),(x1+140,S),(0,0,255),3)
            else:
                rect=((cX,cY),(H,W),theta)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(imss,[box],0,(0,255,0),2)
                cv2.drawContours(imss11,[box],0,(0,255,0),2)
                c="0"
                l.append(c)
            x1=x1+270+j*3
            j=j+1
            theta=theta-3.5
    else:
        theta=80
        j=1
        if S<=185 and S>=300:
            S=270
        S1=72
        #S=270
        h1=55
        x1=60
        w1=106
        while (x1<960):
            
            ims1=thresh[S1-h1:S+h1,x1:x1+150]    
            (_,cnts,_)=cv2.findContours(ims1.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cX=((x1+x1+160)*0.5)
            cY=(S1-h1+S)*0.5
            H=S+h1-S1+h1
            W=(x1+170)-(x1-int(0.05*w1))
            if len(cnts)>3:
                
                rect=((cX,cY),(H,W),theta)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(imss,[box],0,(0,0,255),2)
                cv2.drawContours(imss11,[box],0,(0,0,255),2)
                c="1"
                l.append(c)
        #cv2.rectangle(imss,(x1-int(0.05*w1),S1-h1),(x1+140,S),(0,0,255),3)
            else:
                rect=((cX,cY),(H,W),theta)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(imss,[box],0,(0,255,0),2)
                cv2.drawContours(imss11,[box],0,(0,255,0),2)
                c="0"
                l.append(c)
            x1=x1+190+j*7
            j=j+1
            theta=theta-3.5
    #cv2.rectangle(imss,(x1-int(0.05*w1),S1-h1),(x1+140,S),(0,255,0),3)
else:
    theta=80
    S1=72
    S=270
    h1=31
    thresh=thresh[S1-h1:S+h1,:]
    imss=ims.copy()
    imss=imss[S1-h1:S+2*h1,:]
    h1=43
    x1=30
    w1=106
    while (x1<960):
        ims1=thresh[S1-h1:S+h1,x1:x1+150]    
        (_,cnts,_)=cv2.findContours(ims1.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cX=((x1+x1+180)*0.5)+50
        cY=((S1-h1+S)*0.5)+12
        H=(S+h1-S1+h1)/1.5
        W=(x1+170)-(x1-int(0.05*w1))
        if len(cnts)>3:
            rect=((cX,cY),(H,W),theta)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(imss,[box],0,(0,0,255),2)
            cv2.drawContours(imss11,[box],0,(0,0,255),2)
            c="1"
            l.append(c)
        #cv2.rectangle(imss,(x1-int(0.05*w1),S1-h1),(x1+140,S),(0,0,255),3)
        else:
            rect=((cX,cY),(H,W),theta)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(imss,[box],0,(0,255,0),2)
            cv2.drawContours(imss11,[box],0,(0,255,0),2)
            c="0"
            l.append(c)
        x1=x1+190+j*7
        j=j+1
        theta=theta-3.5
    #cv2.rectangle(imss,(x1-int(0.05*w1),S1-h1),(x1+140,S),(0,255,0),3)
   

if  len(l)<5:
    kl="0"
    l.append(kl)
##    
if len(l)>5:
    listx = list(l) 
    del listx[-1] 
    tuplex = tuple(listx)
cv2.imwrite('imss.jpg',imss11)
    
##    
with open("Output.txt", "w") as text_file:
    text_file.write("Output: {0}".format(l))

d_up1.uploadtxt()
d_up2.uploadim()
##access_token = 'xf_Of6jJbyAAAAAAAAAAjh6S4JogA59B6ZpMjylQAIA209XXWh_QP3TUuxke8IZ1'
##file_from = 'imss.jpg'  
##file_to = '/home/chetan/index.jpg'      
##def upload_file1(file_from, file_to):
##    dbx = dropbox.Dropbox(access_token)
##    f = open(file_from, 'rb')
##    dbx.files_upload(f.read(), file_to)
##upload_file1(file_from,file_to)
##
##file_from1 = 'Output.txt'  
##file_to1 = '/home/chetan/output.txt'      
##def upload_file(file_from, file_to):
##    dbx = dropbox.Dropbox(access_token)
##    f = open(file_from, 'rb')
##    dbx.files_upload(f.read(), file_to)
##upload_file(file_from1,file_to1)


#cv2.imshow("crop",thresh)
cv2.imshow("final",imss)
cv2.imshow("final12",imss11)
cv2.imshow("thresh" ,thresh)
(height, width) = thresh.shape
print(len(cnts))
print(width)
print(S)
print(S1)
cv2.waitKey(0)
print(len(l))       
        


