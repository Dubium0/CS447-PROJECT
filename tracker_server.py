from tracker_server.database.database import Database
from tracker_server.server.app import App
if __name__ == '__main__':
    app = App()
    app.run()