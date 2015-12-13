from Server import Server
from flask import request
from Configs import Configs
import db

server = Server(Configs.timeout)
app = server.create_app()


# API calls
@app.route("/register_purchase/")
def register_purchase():
    shop_id = request.args.get('shop_id', '')
    m_hash = request.args.get('hash', '')
    db.save_tx(shop_id, m_hash)
    return "OK"


@app.route("/get_block/")
def get_block():
    hash = request.args.get('hash', '')
    block = db.get_block_by_tx_hash(hash)
    if block is None:
        return "No block"
    return str(block)
