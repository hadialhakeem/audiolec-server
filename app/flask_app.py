from flask import Flask, request, jsonify
from flask_cors import CORS

from app.cloud import transcribe_file

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Hello World"


@app.route("/transcribe", methods=['POST'])
def transcribe():
    data = request.get_json(force=True)
    file = data['file']
    file_name = data['file_name']

    if ".wav" not in file_name:
        return "file type must be .wav", 400

    transcript = transcribe_file(file, file_name)

    response_dict = {
        'transcript': transcript
    }

    return jsonify(response_dict)


if __name__ == "__main__":
    app.run(debug=True)
