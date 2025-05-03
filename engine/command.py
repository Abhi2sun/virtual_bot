
from .ttss import speak
import sounddevice as sd
import numpy as np
import time
import eel
from .stt import transcribe_audio
from engine.intent_router import IntentRouter 
from .features import *




def takecommand():
    """
    Record microphone input and use STT to get the text.
    """
    samplerate = 16000  # Whisper expects 16kHz
    duration = 5  # You can change this to how long you want to listen

    
    eel.DisplayMessage('listening...')

    # Record microphone
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()

    audio = np.squeeze(recording)

    try:
        
        eel.DisplayMessage('recognizing...')
        query = transcribe_audio(audio)  # Call the imported stt function
        eel.DisplayMessage(query)
        time.sleep(1)
        
        

    except Exception as e:
        print(f"Error during recognition: {e}")
        return ""

    return query.lower()

router=IntentRouter()

@eel.expose
def allCommands(message=1):
    try:
        if message == 1:
            query = takecommand()
        else:
            query = message

        print("📥 Query received:", query)
        eel.senderText(query)

        if query:
            # Try routing via intent router
            success = router.route(query)

            # If routing fails (e.g., no matching intent), fall back to chatbot
            if not success:
                chatBot(query)
                #response = chatBot(query)
                #eel.receiverText(response)
                #speak(response)
    except Exception as e:
        print("❌ Error in allCommands:", e)

    eel.ShowHood()



