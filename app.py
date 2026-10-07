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
                "error": "Please enter a question."
            }), 400

        response = client.responses.create(
            model="gpt-6-luna",

            instructions=(
                "You are a helpful assistant inside a calculator app. "
                "For maths questions, calculate accurately and give the final answer first. "
                "For questions that need current information such as currency exchange rates, "
                "prices, weather, current events, or other changing information, use web search. "
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
        print("OpenAI error:", error)

        return jsonify({
            "error": "AI request failed."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
