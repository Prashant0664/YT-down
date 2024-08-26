from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from pytube import YouTube
app = Flask(__name__)

@app.get('/summary')
def summary_api():
    print(1111)
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    # summary = get_summary(get_transcript(video_id))
    return "summary", 200

def get_transcript(video_id):
    print(video_id)
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def get_summary(transcript):
    print(1111345425)
    summariser = pipeline('summarization')
    summary = ''
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)