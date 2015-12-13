#!/usr/bin/env python
from Server import Server
from flask import request
from Configs import Configs
import db
import re

server = Server(Configs.timeout)

if __name__ == "__main__":
    app = server.create_app()


# API calls
@app.route("/register_purchase/")
def register_purchase():
    shop_id = request.args.get('shop_id', '')
    m_hash = request.args.get('hash', '')
    valid = re.compile("^[A-F0-9]{16}$|^[A-F0-9]{32}$|^[A-F0-9]{64}$")
    if valid.match(m_hash) is not None:
        db.save_tx(shop_id, m_hash)
        return "OK"
    else:
        return ""


@app.route("/get_block/")
def get_block():
    hash = request.args.get('hash', '')
    block = db.get_block_by_tx_hash(hash)
    if block is None:
        return "No block"
    return str(block)
