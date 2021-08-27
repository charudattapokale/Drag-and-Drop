# -*- coding: utf-8 -*-
"""

"""

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(2,720)
detector = HandDetector(detectionCon = 0.8)


class DragRec():
    def __init__(self,centerPos, size=[100,100],def_color=(255,0,0)):
        
        self.centerPos = centerPos
        self.size = size
        self.color = def_color
        self.def_color = def_color
        
    def update(self,indexFinger,color):
        
        centerX, centerY = self.centerPos
        W, H = self.size
        
        print("update")
        
        if centerX - W // 2 < indexFinger[0] < centerX + W // 2 and centerY - H // 2 < indexFinger[1] < centerY + H // 2:
            print(f"{centerX - W // 2} < {indexFinger[0]} < {centerX + W // 2} and {centerY - H // 2} < {indexFinger[1]} < {centerY + H // 2}")
            
            #change the rectangle position and color if conditions met
            self.centerPos = indexFinger
            self.color = color


#list for the rectangle objects
rectList = []
for i in range(5):
    #append the object to the list
    rectList.append(DragRec([i*100+100,i*20+100]))


while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img) 
    lmlist, _ = detector.findPosition(img)
    
    if lmlist: 
        l, _, _ =detector.findDistance(8, 12, img)
        
        #condition to select the retangle
        if l < 35:
            indexFinger = lmlist[8]
            print(f"indexFinger {indexFinger} ... distance {l}")
            #update the rectangle position 
            for rect in rectList:
                rect.update(indexFinger,(0,0,255))
        else:
            for rect in rectList:
                rect.color = rect.def_color
    
    """ Solid draw
    for rect in rectList:
        centerX, centerY =rect.centerPos
        W, H = rect.size
        colorR = rect.color
        print(centerX, centerY)
        cv2.rectangle(img, (centerX-W//2,centerY-H//2),
                      (centerX+W//2,centerY+H//2),colorR,cv2.FILLED)
        cvzone.cornerRect(img,(centerX-W//2,centerY-H//2,W, H),rt = 0)
    """
    
    #transparent draw
    imgNew = np.zeros_like(img, np.uint8)
    out = img.copy()
    for rect in rectList:
        centerX, centerY =rect.centerPos
        W, H = rect.size
        colorR = rect.color
        print(centerX, centerY)
        cv2.rectangle(imgNew, (centerX-W//2,centerY-H//2),
                      (centerX+W//2,centerY+H//2),colorR,cv2.FILLED)
        cvzone.cornerRect(imgNew,(centerX-W//2,centerY-H//2,W, H),rt = 0)
    
    alpha = 0.3
    mask = imgNew.astype(bool)
    print(mask)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    
    
    cv2.imshow("Image",out)
    cv2.waitKey(1)
    #cv2.destroyAllWindows()