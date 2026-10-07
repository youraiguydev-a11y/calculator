import os
import time

from flask import Flask, render_template, request, jsonify
from openai import OpenAI, RateLimitError

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def call_with_retry(**kwargs):
    delays = [1, 2, 4]

    for attempt in range(len(delays) + 1):
        try:
            return client.responses.create(**kwargs)

        except RateLimitError as error:
            print("OPENAI RATE LIMIT ERROR:", error)

            if attempt == len(delays):
                raise

            time.sleep(delays[attempt])


def needs_web_search(question):
    q = question.lower()

    current_words = [
        "current",
        "latest",
        "today",
        "now",
        "weather",
        "exchange rate",
        "convert",
        "usd",
        "pkr",
        "eur",
        "gbp",
        "currency",
        "price",
        "bitcoin",
        "gold"
    ]

    return any(word in q for word in current_words)


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

        if len(question) > 800:
            return jsonify({
                "error": "Please keep the question shorter."
            }), 400


        if needs_web_search(question):

            response = call_with_retry(
                model="gpt-5-mini",
                instructions=(
                    "Give a short and accurate answer. "
                    "Use web search for current information such as "
                    "currency rates, weather, prices, or recent facts."
                ),
                tools=[
                    {
                        "type": "web_search"
                    }
                ],
                input=question,
                max_output_tokens=150
            )

        else:

            response = call_with_retry(
                model="gpt-5-mini",
                instructions=(
                    "You are a concise calculator assistant. "
                    "Solve maths accurately. "
                    "Give the final answer first, then a very short explanation."
                ),
                input=question,
                max_output_tokens=120
            )


        return jsonify({
            "answer": response.output_text
        })


    except RateLimitError as error:

        print("FINAL OPENAI RATE LIMIT ERROR:", error)

        return jsonify({
            "error": "AI is temporarily busy. Please try again shortly."
        }), 429


    except Exception as error:

        print("ASK AI GENERAL ERROR:", error)

        return jsonify({
            "error": "AI request failed."
        }), 500


@app.route("/suggest", methods=["POST"])
def suggest():
    try:
        data = request.get_json() or {}
        expression = data.get("expression", "").strip()

        if not expression or len(expression) > 120:
            return jsonify({
                "suggestion": ""
            })


        response = call_with_retry(
            model="gpt-5-mini",
            instructions=(
                "Check the user's calculator expression. "
                "Only give a suggestion if there is a clear mistake "
                "or a clearly better mathematical form. "
                "Do not comment on normal correct calculations. "
                "Use one very short sentence. "
                "If no suggestion is needed, answer exactly NONE."
            ),
            input=f"Expression: {expression}",
            max_output_tokens=40
        )


        suggestion = response.output_text.strip()

        if suggestion.upper() == "NONE":
            suggestion = ""


        return jsonify({
            "suggestion": suggestion
        })


    except RateLimitError as error:

        print("SUGGESTION RATE LIMIT ERROR:", error)

        return jsonify({
            "suggestion": ""
        })


    except Exception as error:

        print("SUGGESTION GENERAL ERROR:", error)

        return jsonify({
            "suggestion": ""
        })


if __name__ == "__main__":
    app.run(debug=True)
