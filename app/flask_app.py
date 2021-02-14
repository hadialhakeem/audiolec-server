from flask import Flask, request, jsonify
from flask_cors import CORS
from app.quizhelper import create_questions

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/generate", methods=['POST'])
def generate():
    data = request.get_json(force=True)
    title = data['title']

    questions, updated_query = create_questions(title)
    response_dict = {'quiz': questions, 'updated_query': updated_query}
    return jsonify(response_dict)


if __name__ == "__main__":
    app.run(debug=True)
