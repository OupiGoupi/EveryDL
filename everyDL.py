import os
import subprocess
import sys
from flask import Flask, render_template, request, jsonify
import webbrowser
import socket

app = Flask(__name__)

DOWNLOAD_DIR = r"D:\sets"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

PYTHON_EXECUTABLE = sys.executable

def run_command(command, shell=True):
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=shell
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            return False, stderr or stdout or "Erreur inconnue"
        return True, stdout
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_soundcloud', methods=['POST'])
def download_soundcloud():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL manquante'})

    os.chdir(DOWNLOAD_DIR)
    command = [
        PYTHON_EXECUTABLE,
        "-m",
        "yt_dlp",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "0",
        url
    ]
    success, output = run_command(command, shell=False)

    if success:
        return jsonify({'message': 'Téléchargement SoundCloud terminé'})
    else:
        return jsonify({'error': output})

@app.route('/download_spotify', methods=['POST'])
def download_spotify():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL vide'}), 400
    
    try:
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        os.chdir(DOWNLOAD_DIR)
        command = [sys.executable, "-m", "spotdl", url, "--bitrate", "320k", "--format", "mp3"]
        subprocess.Popen(command)  
        return jsonify({'message': 'Téléchargement Spotify démarré'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_youtube_music', methods=['POST'])
def download_youtube_music():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL manquante'})

    os.chdir(DOWNLOAD_DIR)
    command = [
        PYTHON_EXECUTABLE,
        "-m",
        "yt_dlp",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "0",
        "--yes-playlist",  
        url
    ]
    success, output = run_command(command, shell=False)

    if success:
        return jsonify({'message': 'Téléchargement YouTube Music terminé'})
    else:
        return jsonify({'error': output})

if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 5000))
        sock.close()
        webbrowser.open('http://127.0.0.1:5000')
    except socket.error:
        pass
    
    app.run(debug=True, use_reloader=False)