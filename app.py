from flask import Flask, request, jsonify, render_template
import asyncio
import os
import opengradient as og

app = Flask(__name__)

PRIVATE_KEY = os.environ.get("OG_PRIVATE_KEY")

llm = og.LLM(private_key=PRIVATE_KEY)


def run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    prompt = data.get("prompt")

    try:

        result = run_async(
            llm.chat(
                model="openai/gpt-4o",
                messages=[{"role":"user","content":prompt}]
            )
        )

        text = result["choices"][0]["message"]["content"]

        return jsonify({"response": text})

    except Exception as e:

        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run()
