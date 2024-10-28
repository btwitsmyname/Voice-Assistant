#import all libaries
import pyttsx3
import vosk
import pyaudio
import json
import ollama
import time
engine = pyttsx3.init()
#a function to start general model with stt and passthrough
def start_general():
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
    #set output path
    output_file_path = "prompt.txt"
    with open(output_file_path, "w") as output_file:
        text = "What is your question"
        print (text)
        engine.say(text)
        time.sleep(0.5)
        engine.runAndWait()
        #start audio stream
        while True:
            data = stream.read(4096)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                prompt = result['text']
                #write what the system interpuripts
                output_file.write(prompt + "\n")
                print (prompt)
                if "cancel" in prompt.lower():
                    text = "action canceled"
                #push prompt to ollama model
                else: 
                    text = ollama.generate(model='llama3.2',prompt=prompt)
                print (text)
                engine.say(text)
                time.sleep(0.5)
                engine.runAndWait()
                break
def start_math():
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
    #set output path
    output_file_path = "prompt.txt"
    with open(output_file_path, "w") as output_file:
        text = "What is your equation"
        print (text)
        engine.say(text)
        time.sleep(0.5)
        engine.runAndWait()
        #start audio stream
        while True:
            data = stream.read(4096)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                prompt = result['text']
                #write what the system interpuripts
                output_file.write(prompt + "\n")
                print (prompt)
                if "cancel" in prompt.lower():
                    text = "action canceled"
                #push prompt to ollama model
                else:
                    text = ollama.generate(model='qwen2-math',prompt=prompt)
                print (text)
                engine.say(text)
                time.sleep(0.5)
                engine.runAndWait()
                break
#a function to call and use the stt function
def start_stt():
    #set path to language model
    model = vosk.Model("vosk-model-en-us-0.42-gigaspeech")
    #set recorder and standard samplerate for audio files
    rec = vosk.KaldiRecognizer(model,16000)
    #set up mic
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels = 1,
                    rate = 16000,
                    input = True,
                    frames_per_buffer = 8192)
    #set output path
    output_file_path = "speak.txt"
    with open(output_file_path, "w") as output_file:
        text = "Listening"
        engine.say(text)
        engine.runAndWait()
        time.sleep(0.5)
        print (text + "...")
        #start audio stream
        while True:
            data = stream.read(4096)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                speak = result['text']
                #write what the system interpuripts
                output_file.write(speak + "\n")
                print (speak)
                #add termiination keyword
                if "stop program" in speak.lower():
                    test="Ending session"
                    print (test)
                    engine.say(text)
                    time.sleep(0.5)
                    engine.runAndWait()
                    break
                #add generation keyword for model
                if "i have a question" in speak.lower():
                    text="Starting General response model"
                    engine.say(text)
                    engine.runAndWait()
                    time.sleep(0.5)
                    start_general()
                #add math model
                if "perform calculation" in speak.lower():
                    text="Starting calculator"
                    engine.say(text)
                    engine.runAndWait()
                    time.sleep(0.5)
                    start_math()
    stream.stop_stream()
    stream.close()
    p.terminate()
engine=pyttsx3.init()
#keep the initation in the loop
start_stt()
