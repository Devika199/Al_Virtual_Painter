
import cv2
import numpy as np
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
cap.set(3,1280)#3- width,4-height
cap.set(4,720)


detector =htm.handDetector()
drawingColor=(0,0,255)
imgCanvas=np.zeros((720,1280,3),np.uint8)
erasersize=50
brushsize=20



while True:
#1.import image  
#preprocessing screen
    success,image = cap.read()
    image=cv2.resize(image,(1280,720))
    image=cv2.flip(image,1)


    cv2.rectangle(image,(0,0),(1280,110),(0,0,0),cv2.FILLED) 

    cv2.circle(image,(90,60),50,(0,0,255),cv2.FILLED) #red
    cv2.circle(image,(210,60),50,(0,255,0),cv2.FILLED) #green
    cv2.circle(image,(330,60),50,(255,0,0),cv2.FILLED) #blue
    cv2.circle(image,(450,60),50,(0,255,255),cv2.FILLED) #yellow
    cv2.circle(image,(570,60),50,(255,0,255),cv2.FILLED)
    cv2.circle(image,(690,60),50,(255,255,0),cv2.FILLED)
    #cv2.circle(image,(810,60),50,(0,0,0),cv2.FILLED)
    #cv2.rectangle(image,(530,50),50,(255,255,255),cv2.FILLED) #eraser
    cv2.rectangle(image,(810,10),(1270,105),(255,255,255),cv2.FILLED) #eraser
    cv2.putText(image,'Eraser',(1080,65),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)


    #find hand landmarks
    image=detector.findHands(image)
    lmlist=detector.findPosition(image)

    #print(lmlist)
    if len(lmlist)!=0:
        x1,y1=lmlist[8][1:]# index finger
        x2,y2=lmlist[12][1:]# middle finger

        #print(x2,y2)
   
   #3.check which finger is up
    fingers=detector.fingersUp()# checks which finger is up
    #print(fingers)

    #4.selection mode - two finger up condition
    if fingers[1] and fingers[2]:#  if 2 fingers is up yes aneki

        xp,yp=0,0 # staring pt,ending pt
        #print('selection mode')
        if y1<100:# height of clr
            if 60<x1<90:
                drawingColor=(0,0,255)
                #print(x1,y1)
                print('red selected')
            elif 110<x1<210:
                drawingColor=(0,255,0)
                #print('green selected')
            elif 230<x1<330:
                drawingColor=(255,0,0)
                #print('blue selected')
            elif 370<x2<470:
                drawingColor=(0,255,255)
                #print('yellow selected')
            elif 490<x2<570:
               drawingColor=(255,0,255)# pink
            elif 590<x2<810:
                drawingColor=(255,255,0)
                
                
                
            elif 830<x1<1270:
                drawingColor=(0,0,0)
                #print('eraser')

        cv2.rectangle(image,(x1,y1),(x2,y2),drawingColor,cv2.FILLED)
            

            #5.drawing mode - one finger up condition
    if (fingers[1] and not fingers[2]):
        cv2.circle(image,(x1,y1),15,drawingColor,thickness=1)
        #print('drawing mode')
        if xp==0 and yp==0:
               xp=x1
               yp=y1
        if drawingColor==(0,0,0):
            cv2.line(image,(xp,yp),(x1,y1),drawingColor,erasersize)
            cv2.line(imgCanvas,(xp,yp),(x1,y1),drawingColor,erasersize)

        else:
            cv2.line(image,(xp,yp),(x1,y1),drawingColor,brushsize)
            cv2.line(imgCanvas,(xp,yp),(x1,y1),drawingColor,brushsize)
        xp,yp=x1,y1
        # to merge canvas and image
    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgINV=cv2.threshold(imgGray,20,255,cv2.THRESH_BINARY_INV)
    imgINV=cv2.cvtColor(imgINV,cv2.COLOR_GRAY2BGR)

    image=cv2.bitwise_and(image,imgINV)
        
    image=cv2.bitwise_or(image,imgCanvas)


    image=cv2.addWeighted(image,1,imgCanvas,0.5,0)# add both
            

            


    
    cv2.imshow("image",image)
    cv2.waitKey(1)

