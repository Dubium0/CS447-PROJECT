from client.controller.torrent_controller import TorrentController

if __name__ == '__main__':
    controller = TorrentController()
    controller.load_torrents_from_database()
    controller.run()