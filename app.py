#!/bin/python3

from flask import Flask, request, render_template
import openai
import subprocess
import os

app = Flask(__name__)

# Initialize the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Insert path to where the audio files should be uploaded
UPLOAD_FOLDER = "YOUR_PATH_HERE"

# Transcribe function
@app.route("/", methods=["GET", "POST"])
def index():
    transcribed_text = None
    if request.method == "POST":
        # Get the audio file from the uploaded file
        file = request.files["file"]
        if file:
            # Save the uploaded file to the UPLOAD_FOLDER
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            
            #Pass the audio file to the OpenAI Whisper model
            audio_file = open(file.filename, "rb")
            transcribed_text = openai.Audio.transcribe("whisper-1", audio_file, response_format= "text")

    return render_template("website.html", transcribed_text=transcribed_text)

# Translate function
@app.route("/translate", methods=["GET", "POST"])
def translate():
    translated_text = None
    if request.method == "POST":
        # Get the audio file from the uploaded file
        file = request.files["file"]
        if file:
            # Save the uploaded file to the UPLOAD_FOLDER
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            
            #Pass the audio file to the OpenAI Whisper model
            audio_file = open(file.filename, "rb")
            translated_text = openai.Audio.translate("whisper-1", audio_file, response_format= "text")

    return render_template("translate.html", translated_text=translated_text)

# Transcribe to ChatGPT function
@app.route("/askgpt", methods=["GET", "POST"])
def askgpt():
    #global messages
    gpt_text = None
    if request.method == "POST":
        # Get the audio file from the uploaded file
        file = request.files["file"]
        if file:
            # Save the uploaded file to the UPLOAD_FOLDER
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            
            #Pass the audio file to the OpenAI Whisper model
            audio_file = open(file.filename, "rb")
            gpt_text = openai.Audio.transcribe("whisper-1", audio_file, response_format= "text")

            #messages.append({"role": "user", "content": gpt_text["text"]})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
              #{"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": f"{gpt_text}"},
            ]
        )
    answer = response['choices'][0]['message']['content']


    return render_template("askgpt.html", gpt_text=answer)

# Function to call the "What is whisper?" page
@app.route("/faq")
def faq():
    return render_template("faq.html")


app.run(host="0.0.0.0", port=80)

