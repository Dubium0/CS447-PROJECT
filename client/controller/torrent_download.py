import threading
import queue

from . import p2p
class DownloadJobAssigner(threading.Thread):
    def __init__(self,torrent_name :str , peers,controller):
        super().__init__()
        self.job_queue = queue.Queue()  # Queue to hold jobs
        self.stop_event = threading.Event()  # Event to signal stopping
        self.daemon = True  # Daemonize the thread (will exit when the main program exits)
        self.controller = controller
        self.torrent_name = torrent_name
        self.peers  = peers

   

    def run(self):
        """
        Main loop of the thread. Continuously processes jobs from the queue.
        """
        metaInfo,downloadInfo   = self.controller.get_torrent_and_download_info_by_name(self.torrent_name)

        remainingPieces = downloadInfo.remaining_pieces_bytes
        downloadedPieces = downloadInfo.downloaded_pieces_bytes
        while(len(remainingPieces) > 0):

            if len(remainingPieces) > len(self.peers):
                index = 0
                for peerIP_PORT in self.peers:
                    peer_ip, peer_port  = peerIP_PORT.split(':')
                    p2p.download_piece_by_piece( peer_ip,
                                        peer_port,
                                        downloadInfo.file_path,
                                        remainingPieces[index][0],
                                        downloadInfo.piece_length,
                                        remainingPieces[index][1])
                    downloadedPieces.append(remainingPieces[index])
                    index +=1
                remainingPieces = remainingPieces[index:]
            else:
                pindex = 0
                for piece in remainingPieces:
                    peerIP_PORT = self.peers[pindex]
                    peer_ip, peer_port  = peerIP_PORT.split(':')
                    p2p.download_piece_by_piece( 
                                        peer_ip,
                                        peer_port,
                                        downloadInfo.file_path,
                                        piece[0],
                                        downloadInfo.piece_length,
                                        piece[1])
                    downloadedPieces.append(piece)
                    pindex +=1
                remainingPieces = []

            downloadInfo.remaining_pieces_bytes = remainingPieces
            downloadInfo.downloaded_pieces_bytes = downloadedPieces
            self.controller.update_torrent_download_info_by_name(self.torrent_name,downloadInfo)

    def stop(self):
        """
        Stop the thread gracefully.
        """
        self.stop_event.set()
        self.join()  # Wait for the thread to finish