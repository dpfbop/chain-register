from flask import Flask, request
from ChainRegister import ChainRegister
from pymongo import MongoClient

app = Flask(__name__)
register = ChainRegister()
mongoclient = MongoClient() 
db = mongoclient.chainregister_database
transactions = db.transactions
db.drop_collection(transactions)

@app.route("/")
def hello():
    return '<a href="/purchase/coffeemachine"> <button> Купить </button> </a>'

@app.route("/register_purchase/")
def register_purchase():
    id = request.args.get('id', '')
    amount = request.args.get('amount', '')
    price = request.args.get('price', '')
    tx_hash = register.register_purchase(id, amount, price)
    transactions.insert({'hash': tx_hash, 'salt': register.salt})
    return str(tx_hash)
    
@app.route("/get_transactions/<salt>")
def get_transactions(salt):
    num_salt = register.salt_to_num()
    txs = list(transactions.find({'salt': salt}))
    return str(register.get_page_with_transactions(txs))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
