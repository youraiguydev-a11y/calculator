import os

from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

PRIMARY_MODEL = "gemini-3.5-flash-lite"
BACKUP_MODEL = "gemini-3.8-flash"


def ask_model(model_name, prompt):
    return client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=250,
            temperature=0.2
        )
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json() or {}

        question = data.get(
            "question",
            ""
        ).strip()

        if not question:
            return jsonify({
                "error": "Please enter a question."
            }), 400

        # Increased because conversation memory
        # sends previous messages too.
        if len(question) > 12000:
            return jsonify({
                "error": "Conversation is too long. Please start a new chat."
            }), 400

        prompt = (
            "Answer the user's latest message naturally and accurately. "
            "Use earlier conversation only as helpful context. "
            "Always prioritize the latest user message. "
            "Understand normal abbreviations, spelling mistakes, shorthand, "
            "and informal conversational wording using common sense. "
            "If the latest question changes the topic, follow the new topic. "
            "For maths, give the final answer first. "
            "Keep normal answers concise unless more explanation is needed.\n\n"
            f"{question}"
        )

        try:
            response = ask_model(
                PRIMARY_MODEL,
                prompt
            )

        except Exception as primary_error:

            print(
                "PRIMARY MODEL ERROR:",
                repr(primary_error)
            )

            response = ask_model(
                BACKUP_MODEL,
                prompt
            )

        if not response.text:
            return jsonify({
                "error": "AI returned no answer."
            }), 500

        return jsonify({
            "answer":
                response.text.strip()
        })

    except Exception as error:

        print(
            "FINAL GEMINI ERROR:",
            repr(error)
        )

        return jsonify({
            "error":
                "AI is temporarily unavailable. Please try again."
        }), 503


@app.route("/model-check")
def model_check():
    return jsonify({
        "primary": PRIMARY_MODEL,
        "backup": BACKUP_MODEL,
        "status": "ready"
    })


if __name__ == "__main__":
    app.run(debug=True)
