import os
import asyncio
from flask import Flask, request, jsonify, render_template
import opengradient as og

app = Flask(__name__)

PRIVATE_KEY = os.environ.get("OG_PRIVATE_KEY")


@app.route("/")
def index():
    return render_template("index.html")


async def run_model(prompt):

    # створюємо новий client кожен раз
    llm = og.LLM(private_key=PRIVATE_KEY)

    llm.ensure_opg_approval(opg_amount=100)

    messages = [
        {"role": "user", "content": prompt}
    ]

    result = await llm.chat(
        model=og.TEE_LLM.GEMINI_2_5_FLASH,
        messages=messages,
        max_tokens=200,
        x402_settlement_mode=og.x402SettlementMode.PRIVATE
    )

    return result.chat_output["content"]


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    prompt = data.get("prompt")

    try:

        response = asyncio.run(run_model(prompt))

        return jsonify({
            "response": response
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
