from flask import Flask, request
from pytube import YouTube
app = Flask(__name__)

def download(link):
    youtubeObject = YouTube(link)
    yt = youtubeObject.streams.get_highest_resolution()
    try:
        yt.download('Downloads')
    except:
        print("An error has occurred")
    print(link + " Download is completed successfully")

@app.get('/summary')
# @cross_origin()
def summary_api():
    print(1111)
    url = request.args.get('url', '')
    download(url)
    return "summary", 200
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
