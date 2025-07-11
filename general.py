#! /usr/bin/env/Python3
#import all libaries
import pyttsx3
import vosk
import pyaudio
import json
import ollama
import time
engine = pyttsx3.init()
def question():
    #set path to language model
    model = vosk.Model("vosk-model-en-us-0.42-gigaspeech")
    #set recorder and standard sample rate for audio files
    rec = vosk.KaldiRecognizer(model,16000)
    #set up mic
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,channels = 1, rate = 16000,
                    input = True, frames_per_buffer = 8192)
    #set output path
    with open("prompt.txt", "w") as output_file:
        text = "What is your question"
        print (text)
        engine.say(text)
        time.sleep(0.5)
        engine.runAndWait()
        #start audio stream
        while True:
            data = stream.read(1000)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                prompt = result['text']
                #write what the system interpuripts
                output_file.write(prompt + "\n")
                print (prompt)
                if "cancel" in prompt.lower():
                    text = "action canceled"
                    break
                #push prompt to ollama model
                else:
                    print ("Generating response")
                    engine.say("Generating response")
                    engine.runAndWait()
                    #make a file for the response
                    file = open("response.txt","a")
                    #generate the ollama response
                    response =generation = ollama.chat(model='llama3.2',messages=[{'role':'user','content':prompt,},])
                    #variable for the response
                    text = (response['message']['content'])
                    #text = ollama.generate(model='llama3.2',prompt=prompt)
                    print (text)
                    engine.say(text)
                    engine.runAndWait()
                    time.sleep(30)
    stream.stop_stream()
    stream.close()
    p.terminate()
engine=pyttsx3.init()
