# engine/intent_router.py

from engine.features import openCommand, PlayYoutube
from engine.intents import extract_apps
from .ttss import speak  

class IntentRouter:
    def __init__(self):
        # Mapping: intent → app → function
        self.intent_map = {
            "open": {
                "chrome": openCommand,
                "notepad": openCommand,
                "windows": openCommand,
                "whatsapp": openCommand
            },
            "play": {
                "youtube": PlayYoutube,
                "spotify": openCommand
            }
        }

    def detect_intent(self, query):
        query = query.lower()
        if any(word in query for word in ["open", "start", "launch"]):
            return "open"
        if "on youtube" in query or "play" in query:
            return "play"
        if "send message" in query or "whatsapp" in query:
            return "message"
        return None

    def route(self, query):
        intent = self.detect_intent(query)
        apps = extract_apps(query)

        if not intent or not apps:
            #speak("Sorry, I didn't understand that.")
            return False
        handled=False

        for app in apps:
            app = app.strip().lower()
            action = self.intent_map.get(intent, {}).get(app)
            if not action and intent == "open":
                action = openCommand  # fallback to universal handler
            if action:
                try:
                    if intent == "play" and app == "youtube":
                        action(query)  # play c tutorials on youtube
                        
                    else:
                        action(f"{intent} {app}")
                    handled=True
                except Exception as e:
                    speak(f"Something went wrong trying to open {app}.")
                    print(f"[IntentRouter] Error executing {action.__name__}: {e}")
            
                #speak(f"Sorry, I can't handle {app} with intent {intent}.")
                return handled
