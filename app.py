from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import logging

app = Flask(__name__)
CORS(app) # Allow frontend to communicate with backend

logging.basicConfig(level=logging.INFO)

@app.route('/api/resolve', methods=['POST'])
def resolve_video():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL diperlukan"}), 400

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return jsonify({
                "status": "success",
                "title": info.get('title', 'Video Tanpa Judul'),
                "thumbnail": info.get('thumbnail'),
                "video_url": info.get('url'), # The direct streaming URL
                "ext": info.get('ext')
            })

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Gagal mengambil video. Pastikan URL valid."}), 500

if __name__ == '__main__':
    # Run on port 5000
    app.run(debug=True, port=5000)
