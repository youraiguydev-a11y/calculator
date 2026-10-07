import os

from flask import Flask, jsonify
from google import genai

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


@app.route("/")
def home():
    return "Gemini model checker is running."


@app.route("/models")
def models():
    try:
        available_models = []

        for model in client.models.list():
            if "generateContent" in model.supported_actions:
                available_models.append(model.name)

        return jsonify({
            "models": available_models
        })

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
