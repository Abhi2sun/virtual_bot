import torch
from faster_whisper import WhisperModel

# Initialize the model globally once
model_size = "small"  # or "tiny", "base", "medium", "large"
device = "cuda" if torch.cuda.is_available() else "cpu"

whisper_model = WhisperModel(
    model_size,
    device=device,
    compute_type="int8" if device == "cuda" else "float32",
)

def transcribe_audio(audio):
    """
    Given raw audio data (numpy array), transcribes it using Faster-Whisper.
    Returns the recognized text.
    """
    segments, info = whisper_model.transcribe(audio, beam_size=5)
    text = ""
    for segment in segments:
        text += segment.text
    return text.strip()

