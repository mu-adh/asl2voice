from ctypes import alignment
from email.mime import image
import filecmp
import tkinter as tk
from tkinter import filedialog, Text
from tkinter import *
import os
from turtle import down, pos, position
import speech_recognition as sr
import threading
import numpy as np
from keras.models import model_from_json
import operator
import cv2
import sys, os
from time import *
from gtts import gTTS
from playsound import playsound


root=tk.Tk()
root.geometry("3000x3000")
canvas=tk.Canvas(root,height=1000,width=1000,bg="#2a4d69")
canvas.pack()

frame1=Frame(canvas,bg="#e7eff6")
frame1.place(relheight=0.4,relwidth=0.8,rely=0.1,relx=0.1,)
frame2=Frame(canvas,bg="#e7eff6")
frame2.place(relheight=0.4,relwidth=0.8,rely=0.5,relx=0.1,)

def btn1a_hover(e):
    btn1a["image"]=img1b

def btn1a_exit(d):
    btn1a["image"]=img1a

def btn2a_hover(e):
    btn2a["image"]=img2b

def btn2a_exit(d):
    btn2a["image"]=img2a

def recognise():
    frame3=Frame(canvas,bg="#e7eff6")
    frame3.place(relheight=0.8,relwidth=0.8,rely=0.1,relx=0.1,)
    btn4=Button(frame3,borderwidth=0,pady=500,padx=500,bg="#e7eff6",command=v2a)
    btn4.pack(pady=120) 
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if(text=="hello"):
                btn4["image"]=hlo
            elif(text=="thank you"):
                btn4["image"]=ty
            elif(text=="I love you"):
                btn4["image"]=ilov
            else:
                btn4["image"]=sry
        
            

        except:
            btn4["image"]=sry
        frame3.bind('<q>',key_pressed)
global mytimer
mytimer=2
def predi():
    import predict
    def countdown():
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


    json_file = open("model-bw.json", "r")
    model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(model_json)
    
    loaded_model.load_weights("model-bw.h5")
    print("Loaded model from disk")

    cap = cv2.VideoCapture(0)

    
    categories = {1: 'hello', 2: 'ily', 3: 'ty',4: 'null'}

    while True:
        _, frame = cap.read()
        
        frame = cv2.flip(frame, 1)
        
        x1 = int(0.5*frame.shape[1])
        y1 = 50
        x2 = frame.shape[1]-10
        y2 = int(0.5*frame.shape[1])
        cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)
        
        roi = frame[y1:y2, x1:x2]
        
        
        roi = cv2.resize(roi, (64, 64)) 
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, test_image = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
        cv2.imshow("test", test_image)
        
        result = loaded_model.predict(test_image.reshape(1, 64, 64, 1))
        prediction = {'Hello': result[0][0], 
                    'I love you': result[0][1], 
                    'null': result[0][2],
                    'Null': result[0][3]}
        
        prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        
        
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
        

def v2a():
    frame3=Frame(canvas,bg="#e7eff6")
    frame3.place(relheight=0.8,relwidth=0.8,rely=0.1,relx=0.1,)
    
    btn3=Button(frame3,image=micro,borderwidth=0,pady=1500,padx=500,bg="#e7eff6",command=threading.Thread(target=recognise).start)
    btn3.pack(pady=120)
    root.bind('<q>',key_pressed)
    root.bind('<Left>',leftkey)

def a2v():
    #from predict import pred
    frame3=Frame(canvas,bg="#e7eff6")
    frame3.place(relheight=0.8,relwidth=0.8,rely=0.1,relx=0.1,)
    btn3=Button(frame3,borderwidth=0,pady=1500,padx=500,bg="#e7eff6",command=predi)
    btn3.pack(pady=120)
    #root.bind('<q>',key_pressed)

img1a=PhotoImage(file='btn1a.png')
img1b=PhotoImage(file='btn1b.png')
img2a=PhotoImage(file='btn2a.png')
img2b=PhotoImage(file='btn2b.png')
micro=PhotoImage(file='mic.png')
hlo=PhotoImage(file='hello.png')
ilov=PhotoImage(file='ily.png')
ty=PhotoImage(file='ty.png')
sry=PhotoImage(file='sorry.png')
btn1a=Button(frame1,image=img1a,borderwidth=0,bg="#e7eff6",command=a2v)
#btn1a.place(x=500,y=500)
btn1a.pack(padx=50,pady=50)
btn2a=Button(frame2,image=img2a,borderwidth=0,pady=500,padx=500,bg="#e7eff6",command=v2a)
btn2a.place(x=500,y=500)
btn2a.pack()
btn1a.bind("<Enter>",btn1a_hover)
btn1a.bind("<Leave>",btn1a_exit)
btn2a.bind("<Enter>",btn2a_hover)
btn2a.bind("<Leave>",btn2a_exit)


def leftkey(u):
    #frame1=Frame(canvas,bg="#e7eff6")
    frame1.place(relheight=0.4,relwidth=0.8,rely=0.1,relx=0.1,)
    btn1a.pack(padx=50,pady=50)
    #frame2.place(relheight=0.4,relwidth=0.8,rely=0.5,relx=0.1,)  

def key_pressed(event):
    if event.char=='q':
        root.quit()

root.bind('<q>',key_pressed)
root.bind('<w>',leftkey)
root.mainloop()
