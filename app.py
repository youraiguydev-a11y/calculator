import os

from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

selected_model = None


def get_working_model():
    global selected_model

    if selected_model:
        return selected_model

    supported_models = []

    for model in client.models.list():
        actions = model.supported_actions or []

        if "generateContent" in actions:
            supported_models.append(model.name)

    # Prefer newer Flash models first
    preferred_models = [
        "models/gemini-3.8-flash",
        "models/gemini-3.5-flash-lite",
        "models/gemini-2.5-flash-lite",
        "models/gemini-2.5-flash"
    ]

    for model_name in preferred_models:
        if model_name in supported_models:
            selected_model = model_name
            return selected_model

    # If preferred models aren't available,
    # use any Gemini model that supports generateContent
    for model_name in supported_models:
        if "gemini" in model_name.lower():
            selected_model = model_name
            return selected_model

    raise RuntimeError(
        "No Gemini model with generateContent support was found."
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

        model_name = get_working_model()

        response = client.models.generate_content(
            model=model_name,
            contents=(
                "You are a concise calculator and math assistant. "
                "Solve the question accurately. "
                "Give the final answer first, then a short explanation.\n\n"
                f"Question: {question}"
            )
        )

        if not response.text:
            return jsonify({
                "error": "AI returned no answer."
            }), 500

        return jsonify({
            "answer": response.text
        })

    except Exception as error:
        print("GEMINI ERROR:", repr(error))

        return jsonify({
            "error": "AI request failed."
        }), 500


@app.route("/model-check")
def model_check():
    try:
        model_name = get_working_model()

        return jsonify({
            "selected_model": model_name,
            "status": "ready"
        })

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
