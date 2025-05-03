
import struct
import time
from playsound import playsound
import eel
import pvporcupine
from .intents import *
from .ttss import *
import os
import pywhatkit as kit
import sqlite3
import webbrowser
from .helper import *
import pyaudio
import requests
from .ollamaa import *

ASSISTANT_NAME='A L E X A'




con = sqlite3.connect("application.db")
cursor = con.cursor()

@eel.expose #connecting backend with frontend
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")




def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("i")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



selected_model = "llama3"  # default

@eel.expose
def setModel(model_name):
    global selected_model
    # Map UI label to actual model ID used in Ollama
    model_map = {
        "llama": "llama3",
        "gemma": "gemma:2b",
        "qwen": "qwen"
    }
    selected_model = model_map.get(model_name.lower(), "llama3")
    print(f"✅ Python backend model set to: {selected_model}")

#chat application
def chatBot(query):
    global selected_model
    # rest of the function
    print(f"🔁 Using model: {selected_model}")
    response = query_ollama(query, selected_model)
    return response

    