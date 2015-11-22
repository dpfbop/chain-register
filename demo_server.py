from flask import Flask, request
from ChainRegister import ChainRegister
from pymongo import MongoClient
import json

app = Flask(__name__)
register = ChainRegister("hack4people")
mongoclient = MongoClient() 
db = mongoclient.chainregister_database
transactions = db.transactions
db.drop_collection(transactions)

@app.route("/")
def hello():
    return '''<form name="form1" action ="/register_purchase/" onsubmit="return required()">
  Product Id:<br>
  <input type="number" name="product_id">
  <br>
  Amount:<br>
  <input type="number" name="amount">
  <br>Price:<br>
  <input type="number" name="price">
  <br><br>
<input type="submit" value="Buy" />
</form>
<script>
function required()
{
var empt1 = document.forms["form1"]["product_id"].value;
var empt2 = document.forms["form1"]["amount"].value;
var empt3 = document.forms["form1"]["price"].value;
if (empt1 == "" || empt2 == "" || empt3 == "")
{
alert("Please input a Value");
return false;
} else {
return true;
}
}
</script>'''

@app.route("/register_purchase/")
def register_purchase():
    id = request.args.get('product_id', '')
    amount = request.args.get('amount', '')
    price = request.args.get('price', '')
    tx_hash = register.register_purchase(id, amount, price)
    transactions.insert({'hash': tx_hash, 'salt': register.salt})
    return json.dumps({'payment': {'product_id': id, 'amount': amount,
                                   'price': price}, 'transaction': {'tx_hash': tx_hash}})
    
@app.route("/get_transactions/")
def get_transactions():
    salt = request.args.get('salt', '')
    num_salt = register.salt_to_num()
    txs = list(transactions.find({'salt': salt}))
    return json.dumps(register.get_page_with_transactions(txs))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
