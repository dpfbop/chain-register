from flask import Flask
from ChainRegister import ChainRegister

app = Flask(__name__)

@app.route("/")
def hello():
    return '<a href="/purchase/coffeemachine"> <button> Купить </button> </a>'

@app.route("/purchase/<item>")
def successful_purchase(item):
    register = ChainRegister()
    tx_hash = register.register_purchase(item)
    return str(tx_hash)

    
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
