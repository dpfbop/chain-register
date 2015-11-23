from Server import Server
from flask import request
import db

TIMEOUT = 5  # Create new block every TIMEOUT seconds
server = Server(TIMEOUT)

if __name__ == "__main__":
    app = server.create_app()


# API calls
@app.route("/register_purchase/")
def register_purchase():
    shop_id = request.args.get('shop_id', '')
    m_hash = request.args.get('hash', '')
    db.save_tx(shop_id, m_hash)
    return "OK"
