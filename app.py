import os

from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received."
            }), 400

        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "error": "Please enter a math question."
            }), 400

        response = client.responses.create(
            model="gpt-6-luna",
            instructions=(
                "You are a helpful math assistant. "
                "Solve the user's math question accurately. "
                "Give the final answer first, followed by a short and simple explanation. "
                "Keep the response concise."
            ),
            input=question
        )

        return jsonify({
            "answer": response.output_text
        })

    except Exception as error:
        print("OpenAI error:", error)

        return jsonify({
            "error": "AI request failed."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
