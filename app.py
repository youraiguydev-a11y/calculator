import os

from flask import Flask, jsonify
from google import genai

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

@app.route("/")
def home():
    return "Gemini checker is live"

@app.route("/models")
def models():
    try:
        result = []

        for model in client.models.list():
            result.append(model.name)

        return jsonify(result)

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
