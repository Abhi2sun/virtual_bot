import torch
from TTS.api import TTS
import sounddevice as sd
import eel

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the TTS model once
tts_model = TTS(model_name="tts_models/en/ljspeech/fast_pitch", progress_bar=True)
tts_model.to(device)


def speak(text):
    """
    Convert text to speech and play it in real time (no saving).

    """
    text=str(text)
    if not text:
        return

    audio = tts_model.tts(text)
    eel.DisplayMessage(text)
    sd.play(audio, samplerate=tts_model.synthesizer.output_sample_rate)
    eel.receiverText(text)
    sd.wait()

