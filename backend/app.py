from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from pytube import YouTube
import logging
import os
import tempfile

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

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
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                stream.download(filename=tmp_file.name)
                tmp_file_path = tmp_file.name
                logging.debug('Download successful')
                response = send_file(tmp_file_path, as_attachment=True, mimetype='video/mp4')
                response.headers['x-title'] = yt.title
                return response
        else:
            logging.debug('Stream not found')
            return jsonify({"error": "Stream not found"}), 404
    except Exception as e:
        logging.error(f'Error: {e}')
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
