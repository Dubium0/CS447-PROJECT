from tracker_server.server.app import App
if __name__ == '__main__':
    app = App()
    app.init_database()
    app.run()