from flask import Flask

from tracker_server.database.database import Database
from tracker_server.server.announce import announce_blueprint

class App:
    def __init__(self):
        self.app = Flask("tracker_server")

        self.app.register_blueprint(announce_blueprint)

    @staticmethod
    def init_database():
        db = Database()

    def run(self):
        self.app.run(host="0.0.0.0", port=6881)