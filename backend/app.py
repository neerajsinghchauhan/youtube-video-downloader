from flask import Flask, request, send_file, jsonify, make_response
from flask_cors import CORS
from pytube import YouTube
import logging
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG)

@app.route('/download', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def download_video():
    if request.method == 'POST':
        logging.debug('Received POST request')
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
                file_path = '/tmp/video.mp4'
                stream.download(filename=file_path)
                logging.debug('Download successful')
                return send_file(file_path, as_attachment=True, mimetype='video/mp4')
            else:
                logging.debug('Stream not found')
                return jsonify({"error": "Stream not found"}), 404
        except Exception as e:
            logging.error(f'Error: {e}')
            return jsonify({"error": str(e)}), 500

    elif request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response

    else:
        return jsonify({"message": f"Method {request.method} not supported"}), 405

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"error": "Endpoint not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
