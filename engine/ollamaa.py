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


def query_ollama(query, model="llama3"):
    """
    Chat with a local Ollama model.

    Args:
        query (str): User's message
        model (str): Model name selected from UI (e.g. 'llama3', 'qwen', 'gemma')

    Returns:
        str: Model's response
    """
    url = "http://localhost:11434/api/chat"

    # Initial system prompt (optional, customize as needed)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ]

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "top_k": 40,
        "top_p": 0.9,
        "repeat_penalty": 1.1,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        if response.ok:
            answer = response.json()["message"]["content"]
            print("💬", answer)
            # Optional: convert to speech
            speak(answer)
            return answer
        else:
            raise RuntimeError(f"❌ Error {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        return "⚠️ Ollama server is not running. Please start it using: `ollama run <model>`"