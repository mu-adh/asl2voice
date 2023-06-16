import numpy as np
from keras.models import model_from_json
import operator
import cv2
import sys, os
from time import *
import threading
from gtts import gTTS
from playsound import playsound

def countdown():
    global mytimer
    mytimer=2
    for x in range(2):
        mytimer=mytimer-1
        sleep(1)
    if(mytimer==0):
        speech=gTTS(text=txt)
        speech.save('sound.mp3')
        playsound('sound.mp3')
        os.remove('sound.mp3')
        mytimer=2
    else:
        mytimer=2
        os.remove('sound.mp3')

# Loading the model
json_file = open("model-bw.json", "r")
model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(model_json)
# load weights into new model
loaded_model.load_weights("model-bw.h5")
print("Loaded model from disk")

cap = cv2.VideoCapture(0)

# Category dictionary
categories = {1: 'hello', 2: 'ily', 3: 'ty',4: 'null'}

while True:
    _, frame = cap.read()
    # Simulating mirror image
    frame = cv2.flip(frame, 1)
    
    # Got this from collect-data.py
    # Coordinates of the ROI
    x1 = int(0.5*frame.shape[1])
    y1 = 50
    x2 = frame.shape[1]-10
    y2 = int(0.5*frame.shape[1])
    # Drawing the ROI
    # The increment/decrement by 1 is to compensate for the bounding box
    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)
    # Extracting the ROI
    roi = frame[y1:y2, x1:x2]
    
    # Resizing the ROI so it can be fed to the model for prediction
    roi = cv2.resize(roi, (64, 64)) 
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, test_image = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("test", test_image)
    # Batch of 1
    result = loaded_model.predict(test_image.reshape(1, 64, 64, 1))
    prediction = {'Hello': result[0][0], 
                  'I love you': result[0][1], 
                  'null': result[0][2],
                  'Null': result[0][3]}
    # Sorting based on top prediction
    prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
    
    # Displaying the predictions
    txt=prediction[0][0]
    cv2.putText(frame, txt, (420,360), cv2.FONT_HERSHEY_DUPLEX, 1, (255,191,0), 1)    
    
    if (txt=='Hello'):
        cdthread=threading.Thread(target=countdown)
        cdthread.start()
    if (txt=='I love you'):
        cdthread=threading.Thread(target=countdown)
        cdthread.start()        
    cv2.imshow("Frame", frame)

    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27: # esc key
        break
        
 
cap.release()
cv2.destroyAllWindows()
