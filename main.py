import os
import json
import speech_recognition as sr
import pyttsx3
from groq import Groq
from PIL import ImageGrab, Image

import cv2
import pytesseract


from datasets import load_dataset
import torch


import time

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from deepgram import DeepgramClient, SpeakOptions
from dotenv import load_dotenv
import io
import soundfile as sf
import sounddevice as sd
from flask import Response

import re
import requests
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import webbrowser
import time
import keyboard
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from threading import Thread

# Initialize global variable for play/pause state

load_dotenv()

GroqApiKey = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GroqApiKey)

processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

# Load xvector from dataset
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

def synthesize(text):
    inputs = processor(text=text, return_tensors="pt")
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
    speech_numpy = speech.numpy()
    buf = io.BytesIO()
    sf.write(buf, speech_numpy, samplerate=16000, format='WAV', subtype='PCM_16')
    buf.seek(0)
    data, samplerate = sf.read(buf)
    sd.play(data, samplerate)
    sd.wait()

def Can_you_fix_error(chat_box):
    try:
        screenshot = ImageGrab.grab()
        cwd = os.getcwd()
        file_path = os.path.join(cwd, "screenshot.png")
        screenshot.save(file_path)
        Text = extract_text_from_image(file_path)
        Query = "Can you solve this problem and you only have to provide the code nothing else just the corrected code"
        response = ask_question_about_text(Text, Query)
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"Bot: {response}\n")
        chat_box.config(state=tk.DISABLED)
        return "Check Your Chat"
    except Exception as e:
        return f"An error occurred while taking the screenshot: {e}"

def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    return text.strip() if text else "No text detected."

def ask_question_about_text(extracted_text, question):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Please provide a solution to any error found in the extracted text."
        },
        {
            "role": "user",
            "content": f"The following is the extracted text from an image:\n\n{extracted_text}\n\nNow answer the following question based on the above text:\n\n{question}"
        }
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192"
    )

    response = chat_completion.choices[0].message.content
    return response.strip()

def get_youtube_video_url(query):
    query_string = urllib.parse.urlencode({"search_query": query})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    if not search_results:
        return None
    video_url = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    return video_url

def play_music_from_youtube(query):
    video_url = get_youtube_video_url(query)
    if not video_url:
        return "No results found"
    webbrowser.open(video_url)
    time.sleep(2)
    return f"Playing: {query}"

def play_pause_media():
    keyboard.send('play/pause media')
    return "Toggled play/pause"

function_calling_template = """
system

You are a virtual assistant AI model you have to call function depending upon user request also there may be noramal conversation request if the function for specific problem is not provide do not use toolcall in conversation. You are provided with function signatures within <tools></tools> XML tags. You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug into functions. For each function call return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:
<tool_call>
{"name": <function-name>,"arguments": <args-dict>}
</tool_call>

Here are the available tools:
<tools> {
    "name": "Can_you_fix_error",
    "description": "Fix the Error",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
    "name": "play_pause_media",
    "description": "play or puase the current music",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },

    "name": "play_music_from_youtube",
    "description": "Play music from YouTube based on a search query",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to find the music on YouTube"
            }
        },
        "required": ["query"],
    }
} </tools>
"""

def listen_for_trigger_word(trigger_word="hello"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio).lower()
                if trigger_word in text:
                    return
            except sr.UnknownValueError:
                pass

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def process_command(command, chat_box):
    messages = [
        {
            "role": "system",
            "content": function_calling_template
        },
        {
            "role": "user",
            "content": command
        }
    ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
    )
    response = chat_completion.choices[0].message.content

    if "<tool_call>" in response:
        function_call = response.split("<tool_call>")[1].split("</tool_call>")[0]
        function_call_json = json.loads(function_call)
        function_name = function_call_json['name']
        if function_name == "Can_you_fix_error":
            return Can_you_fix_error(chat_box)
        elif function_name == "play_music_from_youtube":
            query = function_call_json['arguments']['query']
            return play_music_from_youtube(query)
        elif function_name == "play_pause_media":
            return play_pause_media()

    return response

def start_bot(chat_box):
    trigger_word = "hello"
    
    while True:
        listen_for_trigger_word(trigger_word)
        st = "Hey, how can I help you?"
        synthesize(st)
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, "Bot: Hey, how can I help you?\n")
        chat_box.config(state=tk.DISABLED)

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, "Listening for command...\n")
            chat_box.config(state=tk.DISABLED)
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio).lower()
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, f"You: {command}\n")
                chat_box.config(state=tk.DISABLED)
                response = process_command(command, chat_box)
                chat_box.insert(tk.END, f"Bot: {response}\n")
                chat_box.config(state=tk.DISABLED)
                if "```" in response:
                    # Split and format code blocks
                    parts = response.split("```")
                    for i, part in enumerate(parts):
                        if i % 2 == 0:
                            chat_box.insert(tk.END, part)
                        else:
                            chat_box.insert(tk.END, part, "code")
                else:
                    chat_box.insert(tk.END, f"Bot: {response}\n")
                if len(response) > 600:
                    speak(response)
                else:
                    synthesize(response)
                chat_box.config(state=tk.NORMAL)
            except sr.UnknownValueError:
                synthesize("Sorry, I didn't catch that.")
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, "Bot: Sorry, I didn't catch that.\n")
                chat_box.config(state=tk.DISABLED)
            except Exception as e:
                synthesize("An unexpected error occurred. Please try again.")
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, f"Bot: An unexpected error occurred. Please try again. Error: {e}\n")
                chat_box.config(state=tk.DISABLED)
                break


def on_start_button_click(chat_box):
    bot_thread = Thread(target=start_bot, args=(chat_box,))
    bot_thread.start()

def create_gui():
    root = tk.Tk()
    root.title("Voice Assistant")

    chat_box = ScrolledText(root, wrap=tk.WORD, state='disabled')
    chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    start_button = tk.Button(root, text="Start Bot", command=lambda: on_start_button_click(chat_box))
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
