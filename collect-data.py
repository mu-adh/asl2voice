import cv2
import numpy as np
import os

# Create the directory structure
if not os.path.exists("data"):
    os.makedirs("data")
    os.makedirs("data/train")
    os.makedirs("data/test")
    os.makedirs("data/train/hello")
    os.makedirs("data/train/ily")
    os.makedirs("data/train/ty")
    os.makedirs("data/test/hello")
    os.makedirs("data/test/ily")
    os.makedirs("data/test/ty")
    

# Train or test 
mode = 'test'
directory = 'data/'+mode+'/'

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    # Simulating mirror image
    frame = cv2.flip(frame, 1)
    
    # Getting count of existing images
    count = {'hello': len(os.listdir(directory+"/hello")),
             'ily': len(os.listdir(directory+"/ily")),
             'ty': len(os.listdir(directory+"/ty")),
             'null': len(os.listdir(directory+"/null"))}

    # Printing the count in each set to the screen
    cv2.putText(frame, "MODE : "+mode, (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    cv2.putText(frame, "IMAGE COUNT", (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    cv2.putText(frame, "HELLO : "+str(count['hello']), (10, 120), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    cv2.putText(frame, "I LOVE YOU : "+str(count['ily']), (10, 140), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    cv2.putText(frame, "THANK YOU : "+str(count['ty']), (10, 160), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
    #cv2.putText(frame, "NULL : "+str(count['null']), (10, 180), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)   
    # Coordinates of the ROI
    x1 = int(0.5*frame.shape[1])
    y1 = 10
    x2 = frame.shape[1]-10
    y2 = int(0.5*frame.shape[1])
    # Drawing the ROI
    # The increment/decrement by 1 is to compensate for the bounding box
    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)
    # Extracting the ROI
    roi = frame[y1:y2, x1:x2]
    roi = cv2.resize(roi, (64, 64)) 
 
    cv2.imshow("Frame", frame)
    
    #_, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
    #kernel = np.ones((1, 1), np.uint8)
    #img = cv2.dilate(mask, kernel, iterations=1)
    #img = cv2.erode(mask, kernel, iterations=1)
    # do the processing after capturing the image!
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, roi = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("ROI", roi)
    
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27: # esc key
        break
    if interrupt & 0xFF == ord('1'):
        cv2.imwrite(directory+'hello/'+str(count['hello'])+'.jpg', roi)
    if interrupt & 0xFF == ord('2'):
        cv2.imwrite(directory+'ily/'+str(count['ily'])+'.jpg', roi)
    if interrupt & 0xFF == ord('3'):
        cv2.imwrite(directory+'ty/'+str(count['ty'])+'.jpg', roi)
    if interrupt & 0xFF == ord('4'):
        cv2.imwrite(directory+'null/'+str(count['null'])+'.jpg', roi)
cap.release()
cv2.destroyAllWindows()
