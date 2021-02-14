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
    file_name = data['file']

    transcript = transcribe_file(file_name)

    response_dict = {
        'transcript': transcript
    }

    return jsonify(response_dict)


@app.route('/uploadfile', methods=['GET', 'POST', 'PUT'])
def uploadfile():
    if request.method == 'PUT':
        f = request.files['file']
        filePath = "./somedir/"+secure_filename(f.filename)
        f.save(filePath)
        return "success"


if __name__ == "__main__":
    app.run(debug=True)
