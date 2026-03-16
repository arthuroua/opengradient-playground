from flask import Flask, request, jsonify, render_template
import asyncio
import os

import opengradient as og
from eth_account import Account
from web3 import Web3

app = Flask(__name__)

PRIVATE_KEY = os.environ.get("OG_PRIVATE_KEY")

llm = og.LLM(private_key=PRIVATE_KEY)

# RPC Base Sepolia
RPC = "https://sepolia.base.org"
w3 = Web3(Web3.HTTPProvider(RPC))

OPG_TOKEN = Web3.to_checksum_address("0x240b09731D96979f50B2C649C9CE10FcF9C7987F")

PERMIT2 = Web3.to_checksum_address(
    "0x000000000022D473030F116dDEE9F6B43aC78BA3"
)

wallet = Account.from_key(PRIVATE_KEY)


# ERC20 approve ABI
ERC20_ABI = [{
 "name":"approve",
 "type":"function",
 "stateMutability":"nonpayable",
 "inputs":[
  {"name":"spender","type":"address"},
  {"name":"amount","type":"uint256"}
 ],
 "outputs":[{"name":"","type":"bool"}]
}]


def ensure_approval():

    contract = w3.eth.contract(address=OPG_TOKEN, abi=ERC20_ABI)

    nonce = w3.eth.get_transaction_count(wallet.address)

    tx = contract.functions.approve(
        PERMIT2,
        10**30
    ).build_transaction({
        "from": wallet.address,
        "nonce": nonce,
        "gas": 100000,
        "gasPrice": w3.eth.gas_price
    })

    signed = wallet.sign_transaction(tx)

    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    print("Approve TX:", tx_hash.hex())


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

        ensure_approval()

        result = asyncio.run(run_llm(prompt))

        return jsonify({"response": result})

    except Exception as e:

        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run()
