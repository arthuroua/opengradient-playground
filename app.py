from flask import Flask, request, jsonify, render_template
import asyncio
import os
import opengradient as og

app = Flask(__name__)

PRIVATE_KEY = os.environ.get("OG_PRIVATE_KEY")

llm = og.LLM(private_key=PRIVATE_KEY)


async def run_llm(prompt):

    response = await llm.chat(
        model="meta/Meta-Llama-3-8B-Instruct",
        messages=[{"role":"user","content":prompt}]
    )

    return response["choices"][0]["message"]["content"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    prompt = data.get("prompt")

    try:

        result = asyncio.run(run_llm(prompt))

        return jsonify({"response": result})

    except Exception as e:

        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run()
