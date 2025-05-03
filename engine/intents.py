

#using lightweight llm to extract intents from the sentence 
from ctransformers import AutoModelForCausalLM
import re

# ---- Model Configuration ----
# Choose your local model path and file
MODEL_FOLDER = "C:\\Users\\HP PC\\Desktop\\va\\"
MODEL_FILE = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"            
MODEL_TYPE = "tinyllama"                           

# Load the model ONCE globally
llm = AutoModelForCausalLM.from_pretrained(
    MODEL_FOLDER,
    model_file=MODEL_FILE,
    model_type=MODEL_TYPE,
    max_new_tokens=100,
    temperature=0.1,       # Keep generation deterministic
    repetition_penalty=1.1 # Avoid repeating words
)



KNOWN_APPS = ["whatsapp", "windows", "youtube", "chrome", "instagram","notepad",'spotify','sql','vlc']


def extract_apps(query: str):
    query = query.lower()
    apps = [app for app in KNOWN_APPS if app in query]
    
    if apps:
        return apps
    else:
        prompt = f"""
You are a helpful assistant.

Task: Extract ONLY the application names mentioned in the user input text.
Ignore verbs like open, start, launch, play, go to, etc.
Return ONLY a pure Python list of application names, in lowercase.

Example 1:
Input: "open youtube and chrome"
Output: ["youtube", "chrome"]

Example 2:
Input: "start whatsapp and windows"
Output: ["whatsapp", "windows"]

Now process the following:

Input: "{query}"
Output:
"""
    try:
        response = llm(prompt, max_new_tokens=150)  # Updated max tokens
        #print(f"LLM Response: {response}")

        # Safe extraction
        match = re.search(r"\[.*?\]", response, re.DOTALL)
        if match:
            apps = eval(match.group())
            if isinstance(apps, list):
                return [app.strip().lower() for app in apps]
        return []

    except Exception as e:
        #print(f"Error in LLM extraction: {e}")
        return []

