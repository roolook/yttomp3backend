from flask import Flask, request, jsonify
from deepgram import Deepgram
import asyncio
import os

app = Flask(__name__)
dg = Deepgram("071fc58248a998ed6a6f2f17c585bf86336cfee4")

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    source = {'buffer': file.read(), 'mimetype': file.mimetype}

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        response = loop.run_until_complete(dg.transcription.prerecorded(source, {'punctuate': True}))
        transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
        return jsonify({'transcript': transcript})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)