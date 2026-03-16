from flask import Flask, request, jsonify
import opengradient as og
import asyncio
import os

app = Flask(__name__)

PRIVATE_KEY = os.getenv("OG_PRIVATE_KEY")

llm = og.LLM(private_key=PRIVATE_KEY)


async def run_llm(prompt):

    response = await llm.chat(
        model="Meta-Llama-3-8B-Instruct",
        messages=[{"role":"user","content":prompt}]
    )

    return response


@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        prompt = data.get("prompt","")

        result = asyncio.run(run_llm(prompt))

        return jsonify({
            "response": str(result)
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/")
def home():
    return open("index.html").read()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
