from flask import Flask, request, jsonify
from pytube import YouTube
from flask_cors import CORS
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import dotenv

# Load environment variables
dotenv.load_dotenv()

app = Flask(__name__)

# Allow CORS from frontend (localhost:3001 in this case)
CORS(app, origins=["http://localhost:3001"])

DOWNLOAD_PATH = 'Downloads'  # Local folder to save the videos

# Configure Cloudinary using your credentials
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)
print("cloudinary configured;;;;;;;")

# Ensure the Downloads folder exists
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

def download_video(link):
    """
    Downloads the YouTube video and returns the local file path.
    """
    youtube_object = YouTube(link)
    yt = youtube_object.streams.get_highest_resolution()
    try:
        file_path = yt.download(DOWNLOAD_PATH)  # Returns the file path
        return file_path  # Return the local path of the downloaded file
    except Exception as e:
        print(f"An error occurred while downloading: {e}")
        return None

def upload_to_cloudinary(file_path):
    """
    Uploads the file to Cloudinary and returns the Cloudinary URL.
    """
    try:
        print("uploading started")
        response = cloudinary.uploader.upload(file_path, resource_type="video")
        cloudinary_url = response.get('secure_url')
        print("uploaded finished", cloudinary_url)
        return cloudinary_url
    except Exception as e:
        print(f"An error occurred while uploading to Cloudinary: {e}")
        return None

@app.get('/summary')
def summary_api():
    print("API HITTED")
    # return jsonify({"cloudinary_url": "HIIII"}), 200
    url = request.args.get('url', '')
    
    if not url:
        return jsonify({"error": "No URL provided."}), 400

    # Download video from YouTube
    file_path = download_video(url)
    print("downloaded")
    if not file_path:
        return jsonify({"error": "Failed to download video."}), 500

    # Upload to Cloudinary
    cloudinary_url = upload_to_cloudinary(file_path)

    if not cloudinary_url:
        return jsonify({"error": "Failed to upload video to Cloudinary."}), 500

    # Optionally, you can delete the local file after uploading
    os.remove(file_path)

    return jsonify({"cloudinary_url": cloudinary_url}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
