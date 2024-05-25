from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from pytube import YouTube
import os

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
#CORS(app)

# Serve the React app
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data['url']
    format = data['format']

    try:
        yt = YouTube(url)
        if format == '360p':
            stream = yt.streams.filter(res="360p", file_extension='mp4').first()
        elif format == '480p':
            stream = yt.streams.filter(res="480p", file_extension='mp4').first()
        elif format == '720p':
            stream = yt.streams.filter(res="720p", file_extension='mp4').first()
        else:
            return jsonify({"error": "Invalid format"}), 400

        if stream:
            file_path = 'video.mp4'
            stream.download(filename=file_path)
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "Stream not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render provides the PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
