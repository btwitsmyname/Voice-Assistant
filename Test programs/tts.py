#import all libaries
import pyttsx3
#state the engine being used
engine = pyttsx3.init()
#text variable
text="This is a test for the speach to text"
#say text variable
engine.say(text)
#perform action and wait
engine.runAndWait()
