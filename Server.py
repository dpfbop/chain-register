from flask import Flask
from ChainRegister import ChainRegister
from threading import Lock, Thread
from time import sleep
import db


class Server(object):
    def __init__(self, timeout):
        self.timeout = timeout
        self._app = Flask(__name__)
        self.register = ChainRegister()

    def create_app(self):
        def run_register():
            # Thread with register
            while True:
                sleep(self.timeout)
                with Lock():
                    new_block_id, txs_hashes = db.get_txs_for_new_block()
                    # print(txs_hashes)
                    self.register.register_block(new_block_id, txs_hashes)

        def run_flask():
            # Thread with Flask
            self._app.debug = False  # Flask can't work in thread in debug mode
            self._app.run(host='0.0.0.0')

        register_thread = Thread(target=run_register)
        flask_thread = Thread(target=run_flask)
        register_thread.start()
        flask_thread.start()
        return self._app
