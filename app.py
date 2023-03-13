#!/bin/python3

from flask import Flask, request, render_template
import openai
import subprocess
import os

app = Flask(__name__)

# Initialize the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

UPLOAD_FOLDER = "/home/al_termure/whisper_flask"

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
            transcribed_text = openai.Audio.transcribe("whisper-1", audio_file)

    return render_template("website.html", transcribed_text=transcribed_text)

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
            translated_text = openai.Audio.translate("whisper-1", audio_file)

    return render_template("translate.html", translated_text=translated_text)

@app.route("/faq")
def faq():
    return render_template("faq.html")


app.run(host="0.0.0.0", port=80)

