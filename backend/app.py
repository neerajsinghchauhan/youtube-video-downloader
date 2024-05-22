from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pytube import YouTube
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Auth-Token, Origin, Authorization'
    return response

@app.route('/download', methods=['POST'])
def download_video():
    logging.debug('Received request')
    data = request.json
    logging.debug(f'Request data: {data}')
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
            logging.debug('Download successful')
            return send_file(file_path, as_attachment=True, mimetype='video/mp4')
        else:
            logging.debug('Stream not found')
            return jsonify({"error": "Stream not found"}), 404
    except Exception as e:
        logging.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
