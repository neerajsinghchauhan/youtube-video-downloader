from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pytube import YouTube

app = Flask(__name__)
CORS(app)

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
handler = app
if __name__ == '__main__':
    app.run()