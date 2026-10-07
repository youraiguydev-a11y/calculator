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
        data = request.get_json() or {}
        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "error": "Please enter a question."
            }), 400

        response = client.responses.create(
            model="gpt-6-luna",
            instructions=(
                "You are a helpful assistant inside a calculator app. "
                "For maths questions, calculate carefully and give the final answer first. "
                "For questions that need current information, such as exchange rates, "
                "weather, prices, or recent information, use web search when needed. "
                "Keep answers short, clear, and easy to understand."
            ),
            tools=[
                {
                    "type": "web_search"
                }
            ],
            input=question
        )

        return jsonify({
            "answer": response.output_text
        })

    except Exception as error:
        print("Ask AI error:", error)

        return jsonify({
            "error": "AI request failed."
        }), 500


@app.route("/suggest", methods=["POST"])
def suggest():
    try:
        data = request.get_json() or {}
        expression = data.get("expression", "").strip()

        if not expression:
            return jsonify({
                "suggestion": ""
            })

        response = client.responses.create(
            model="gpt-6-luna",
            instructions=(
                "You are a smart calculator assistant watching the user's calculation "
                "while they are typing. "
                "Only give a suggestion if the calculation appears incorrect, confusing, "
                "incomplete, or there is a clearly better mathematical way to write it. "
                "Do not interrupt correct simple calculations. "
                "Do not guess what the user means unless the likely mistake is clear. "
                "Keep the suggestion to one short sentence. "
                "If no useful suggestion is needed, reply with exactly NONE."
            ),
            input=f"Current calculation: {expression}"
        )

        suggestion = response.output_text.strip()

        if suggestion.upper() == "NONE":
            suggestion = ""

        return jsonify({
            "suggestion": suggestion
        })

    except Exception as error:
        print("Suggestion error:", error)

        return jsonify({
            "suggestion": ""
        })


if __name__ == "__main__":
    app.run(debug=True)
