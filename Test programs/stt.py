#import all libaries
import vosk
import pyaudio
import json
#set path to language model
model = vosk.Model("vosk-model-small-en-us-0.15")
#set recorder
rec = vosk.KaldiRecognizer(model,16000)
#sample rate of 16000hz is average for audio file sizes
#set up mic
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels = 1,
                rate = 16000,
                input = True,
                frames_per_buffer = 8192)
#set output file path
output_file_path = "speak.txt"
with open(output_file_path, "w") as output_file:
    print ("Listening...")
    #start audio stream
    while True:
        data = stream.read(4096)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            speak = result['text']
            #write the text
            output_file.write(speak + "\n")
            print (speak)
            #add termination keyword
            if "stop program" in speak.lower():
                print ("Ending program")
                break
stream.stop_stream()
stream.close()
p.terminate()
