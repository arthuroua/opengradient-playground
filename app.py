from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)


LLM_ENDPOINT = "http://3.15.214.21/v1/chat/completions"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    prompt = data.get("prompt")

    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:

        r = requests.post(
            LLM_ENDPOINT,
            json=payload
        )

        result = r.json()

        text = result["choices"][0]["message"]["content"]

        return jsonify({"response": text})

    except Exception as e:

        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run()
