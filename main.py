#! /usr/bin/env/Python3
#import all libaries
import pyttsx3
import vosk
import pyaudio
import json
import ollama
import time
import tkinter as tk
#custom supporting files
import general
import calculation
#start the stt engine
engine = pyttsx3.init()
#set path to language model
model = vosk.Model("vosk-model-small-en-us-0.15")
#set recorder and standard samplerate for audio files
rec = vosk.KaldiRecognizer(model,16000)
#set up mic
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                    channels = 1,
                    rate = 16000,
                    input = True,
                    frames_per_buffer = 8192)
#start speech output
with open("speak.txt", "w") as output_file:
    text="Listening"
    print (text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)
    #start audio stream
    while True:
        data = stream.read(1000)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            speak = result['text']
            #write what the system interpuripts
            output_file.write(speak + "\n")
            print (speak)
            #add termiination keyword
            if "stop program" in speak.lower():
                text ="Ending program"
                print (text)
                engine.say(text)
                engine.runAndWait()
                time.sleep(1)
                break
            #add generation keyword for model
            if "i have a question" in speak.lower():
                text="Starting General response model"
                engine.say(text)
                engine.runAndWait()
                time.sleep(0.5)
                general.question()
            #add math model
            if "perform calculation" in speak.lower():
                text="Starting calculator"
                engine.say(text)
                engine.runAndWait()
                time.sleep(0.5)
                calculation.math()
stream.stop_stream()
stream.close()
p.terminate()
engine=pyttsx3.init()
