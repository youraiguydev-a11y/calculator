from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question"}), 400

    try:
        response = client.responses.create(
            model="gpt-6-luna",
            instructions=(
                "You are a concise math assistant. "
                "Solve the user's math question accurately. "
                "Give the final answer first, then a very short explanation."
            ),
            input=question
        )

        return jsonify({
            "answer": response.output_text
        })

    except Exception as error:
        return jsonify({
            "error": "AI request failed"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
