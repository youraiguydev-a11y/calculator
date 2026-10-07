import os
import time

from flask import Flask, render_template, request, jsonify
from openai import OpenAI, RateLimitError

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def create_response_with_retry(**kwargs):
    """
    Temporary 429 rate-limit aaye to thora wait karke
    automatically retry karega.
    """

    delays = [1, 2, 4]

    for attempt in range(len(delays) + 1):
        try:
            return client.responses.create(**kwargs)

        except RateLimitError:
            if attempt == len(delays):
                raise

            time.sleep(delays[attempt])


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

        # Prevent unnecessarily huge prompts
        if len(question) > 1000:
            return jsonify({
                "error": "Please keep the question shorter."
            }), 400

        response = create_response_with_retry(
            model="gpt-6-luna",

            instructions=(
                "You are a concise assistant inside a calculator app. "
                "For maths questions, calculate carefully and give the final answer first. "
                "For current information such as exchange rates, weather, prices, "
                "or recent information, use web search when necessary. "
                "Keep the answer short and clear."
            ),

            tools=[
                {
                    "type": "web_search"
                }
            ],

            input=question,

            max_output_tokens=180
        )

        return jsonify({
            "answer": response.output_text
        })


    except RateLimitError:
        return jsonify({
            "error": "AI is busy right now. Please try again in a few seconds."
        }), 429

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

        # Suggestions only need a small expression
        if len(expression) > 150:
            return jsonify({
                "suggestion": ""
            })

        response = create_response_with_retry(
            model="gpt-6-luna",

            instructions=(
                "You are a smart calculator assistant. "
                "Look at the calculation the user is currently entering. "
                "Only suggest something when there is a clear mathematical mistake, "
                "confusing expression, or clearly better way to write it. "
                "Do not interrupt normal correct calculations. "
                "Never invent context. "
                "Give at most one short sentence. "
                "If no suggestion is useful, reply exactly NONE."
            ),

            input=f"Calculation: {expression}",

            max_output_tokens=60
        )

        suggestion = response.output_text.strip()

        if suggestion.upper() == "NONE":
            suggestion = ""

        return jsonify({
            "suggestion": suggestion
        })


    except RateLimitError:
        # Don't annoy user with an error while typing
        return jsonify({
            "suggestion": ""
        })

    except Exception as error:
        print("Suggestion error:", error)

        return jsonify({
            "suggestion": ""
        })


if __name__ == "__main__":
    app.run(debug=True)
