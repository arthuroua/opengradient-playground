from flask import Flask, request, jsonify, render_template
import opengradient as og
import os

app = Flask(__name__)

PRIVATE_KEY = os.environ.get("OG_PRIVATE_KEY")

llm = og.LLM(private_key=PRIVATE_KEY)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    prompt = request.json.get("prompt")

    try:

        response = llm.chat(
            model="Meta-Llama-3-8B-Instruct",
            messages=[{"role":"user","content":prompt}]
        )

        return jsonify({
            "response": str(response)
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
