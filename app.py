from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

API_BLOCKS_URL = "https://blockstream.info/api/blocks/"
API_BLOCK_DETAILS_URL = "https://blockstream.info/api/block/"
API_MEMPOOL_URL = "https://blockstream.info/api/mempool/recent"

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/blocks")
def blocks_page():
    return render_template("blocks.html")

@app.route('/block-details', methods=['GET'])
def block_details_page():
    block_id = request.args.get('id')
    if not block_id:
        return "Errore: ID del blocco non fornito", 400
    return render_template('block-details.html', block_id=block_id)

@app.route("/api/blocks", methods=["GET"])
def get_blocks():
    last_block_height = request.args.get("lastBlockHeight")
    url = f"{API_BLOCKS_URL}{last_block_height}" if last_block_height else API_BLOCKS_URL
    try:
        response = requests.get(url)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/mempool")
def mempool_page():
    return render_template("mempool.html")

@app.route("/transaction-details")
def transaction_details_page():
    tx_id = request.args.get("id")
    if not tx_id:
        return "Errore: ID della transazione non fornito", 400
    return render_template("transaction-details.html", tx_id=tx_id)

@app.route("/api/mempool", methods=["GET"])
def get_mempool_transactions():
    try:
        response = requests.get(API_MEMPOOL_URL)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False)