import os

from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json() or {}
        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "error": "Please enter a question."
            }), 400

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                "You are a concise calculator and math assistant. "
                "Answer accurately. Give the final answer first, "
                "then a short and simple explanation.\n\n"
                f"Question: {question}"
            )
        )

        answer = response.text

        if not answer:
            return jsonify({
                "error": "AI returned no answer."
            }), 500

        return jsonify({
            "answer": answer
        })

    except Exception as error:
        print("GEMINI ERROR:", error)

        return jsonify({
            "error": "AI request failed."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
