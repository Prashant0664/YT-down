from flask import Flask, request
from pytube import YouTube
from flask_cors import CORS

app = Flask(__name__)

# Allow CORS from localhost:5000
CORS(app, origins=["https://www.youtube.com"])

def download(link):
    youtubeObject = YouTube(link)
    yt = youtubeObject.streams.get_highest_resolution()
    try:
        yt.download('Downloads')
    except Exception as e:
        print(f"An error has occurred: {e}")
    print(f"{link} Download is completed successfully")

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    download(url)
    return "summary", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
