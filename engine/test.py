import os
import onnxruntime
import numpy as np
from transformers import AutoTokenizer
from huggingface_hub import snapshot_download
import shutil

# Local ONNX cache root
CACHE_DIR = "./onnx_models"

# Model registry
MODELS = {
    "llama": "onnx-community/Llama-3.2-3B-Instruct-ONNX",
    "gemma": "onnx-community/Gemma-2B-Instruct-ONNX",
    "qwen": "onnx-community/Qwen2-1_5B-Instruct-onnx"
}

class ONNXModelManager:
    def __init__(self):
        self.sessions = {}
        self.tokenizers = {}

    def download_once(self, key):
        model_id = MODELS.get(key)
        if not model_id:
            raise ValueError(f"[ERROR] Unsupported model key: {key}")

        local_path = os.path.join(CACHE_DIR, key)
        if not os.path.exists(local_path):
            print(f"[INFO] Downloading {key} ONNX model from Hugging Face...")
            tmp = snapshot_download(repo_id=model_id, local_dir=local_path, local_dir_use_symlinks=False, resume_download=True )
        return local_path

    def load(self, key):
        if key in self.sessions:
            return self.sessions[key], self.tokenizers[key]

        local_path = self.download_once(key)

        # Load ONNX model session (assume decoder_model.onnx)
        onnx_file = os.path.join(local_path, "decoder_model.onnx")
        session = onnxruntime.InferenceSession(onnx_file, providers=["CPUExecutionProvider"])

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(local_path)

        self.sessions[key] = session
        self.tokenizers[key] = tokenizer
        return session, tokenizer

    def generate(self, key, prompt, max_tokens=100):
        session, tokenizer = self.load(key)

        inputs = tokenizer(prompt, return_tensors="np")
        ort_inputs = {
            "input_ids": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"]
        }

        outputs = session.run(None, ort_inputs)
        logits = outputs[0]
        predicted_ids = np.argmax(logits, axis=-1)
        return tokenizer.decode(predicted_ids[0], skip_special_tokens=True)
manager = ONNXModelManager()
print(manager.generate("llama", "Tell me a joke."))