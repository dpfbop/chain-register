from flask import Flask, request
from ChainRegister import ChainRegister
from pymongo import MongoClient
from datetime import datetime
import json


app = Flask(__name__)
register = ChainRegister("hack4people")
mongo = MongoClient()
db = mongo.chainregister_database
transactions = db.transactions
blocks = db.blocks


@app.route("/register_purchase/")
def register_purchase():
    id = request.args.get('shop_id', '')
    hash = request.args.get('hash', '')
    now = datetime.utcnow()
    transactions.insert({'shop_id': id, 'hash': hash, "block": -1,
                              "date": now})
    return json.dumps({'transaction': {'shop_id': id, 'hash': hash,
                                       'block': -1, 'date': now.isoformat()}})


@app.route("/get_undelivered/")
def get_undelivered_txs():
    result = []
    for tx in transactions.find({"block": -1}):
        tx["date"] = tx['date'].isoformat()
        del tx["_id"]
        result.append(tx)
    return json.dumps(result)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

