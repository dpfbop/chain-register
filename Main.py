#!/usr/bin/env python
from flask import Flask, request, jsonify
import db
import re
import json

app = Flask(__name__)


# API calls
@app.route("/register_purchase/")
def register_purchase():
    shop_id = request.args.get('shop_id', '')
    m_hash = request.args.get('hash', '')
    valid_hash = re.compile("^[a-fA-F0-9]{16}$|^[a-fA-F0-9]{32}$|^[a-fA-F0-9]{64}$")
    if valid_hash.match(m_hash) is not None:
        try:
            if int(shop_id) <= 0:
                raise ValueError
        except ValueError:
            return json.dumps({"status": "FAIL", "message": "shop_id should be a positive number"})
        db.save_tx(shop_id, m_hash)
        return json.dumps({"status": "OK", "message": ""})
    else:
        return json.dumps({"status": "FAIL", "message": "hash should have 16, 32 or 64 symbols"})


@app.route("/get_block/")
def get_block():
    m_hash = request.args.get('hash', '')
    valid_hash = re.compile("^[a-fA-F0-9]{16}$|^[a-fA-F0-9]{32}$|^[a-fA-F0-9]{64}$")
    if valid_hash.match(m_hash) is not None:
        blocks = db.get_block_by_tx_hash(m_hash)
        if blocks is None or len(blocks) == 0:
            return jsonify({"status": "OK", "block": None, "date": None, "message": "hash not found"})
        return jsonify({"status": "OK", "blocks": list([{"block": block[0], "date": block[1]} for block in blocks]), "message": ""})
    else:
        return jsonify({"status": "FAIL", "message": "hash should have 16, 32 or 64 symbols"})


@app.route("/check")
def check():
    return app.send_static_file("checker.html")
#
#
# @app.route("/sha256.js")
# def sha256():
#     return app.send_static_file("sha256.js")
#
#
# @app.route("/styles.css")
# def styles():
#     return app.send_static_file("styles.css")

if __name__ == "__main__":
    app.run()
