from flask import Flask, request, send_file, jsonify
from pytube import YouTube
from flask_cors import CORS
import os

app = Flask(__name__)

# Allow CORS from localhost:5000
CORS(app, origins=["https://www.youtube.com"])

DOWNLOAD_FOLDER = 'Downloads'

def download(link):
    youtubeObject = YouTube(link)
    yt = youtubeObject.streams.get_highest_resolution()
    try:
        # Download the video to the Downloads folder
        print("start video in downloadded;;;;;;;")
        video_path = yt.download(DOWNLOAD_FOLDER)
        print("video in downloadded;;;;;;;")
        return video_path  # Return the path of the downloaded video
    except Exception as e:
        print(f"custom2 An error has occurred;;;;;;;: {e}")
        return None

@app.get('/summary')
def download_video():
    url = request.args.get('url', '')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    print("downloaded initialted;;;;;;;")
    video_path = download(url)
    print("video_path downloaded;;;;;;;", video_path)
    if not video_path:
        return jsonify({"error": "Failed to download video"}), 500

    try:
        # Send the downloaded file to the client
        print("video sending...")
        return send_file(video_path, as_attachment=True)
    except Exception as e:
        print(f"An custom1 error occurred while sending the file;;;;;;;: {e}")
        return jsonify({"error": "Error sending file"}), 500

if __name__ == '__main__':
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    app.run(host='0.0.0.0', port=3000)
