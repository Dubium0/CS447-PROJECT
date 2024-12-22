from flask import Flask, request, jsonify
import random
import time

app = Flask(__name__)

# Store peers in memory (for demo purposes, use a database in production)
peers = {}

@app.route('/announce', methods=['GET'])
def announce():
    # Parse the incoming parameters
    info_hash = request.args.get('info_hash')  # Hash of the torrent file
    peer_id = request.args.get('peer_id')  # Unique peer ID
    ip = request.args.get('ip')  # Peer IP address
    port = request.args.get('port')  # Peer port
    event = request.args.get('event')  # Event like 'started', 'completed', 'stopped'
    uploaded = request.args.get('uploaded')  # Amount uploaded
    downloaded = request.args.get('downloaded')  # Amount downloaded

    if info_hash not in peers:
        peers[info_hash] = []

    # Store or update peer information (you may wish to add more features, like banning or timeouts)
    peer_data = {
        'peer_id': peer_id,
        'ip': ip,
        'port': port,
        'last_announce': time.time()
    }

    # Add the peer to the list of peers for this torrent
    peers[info_hash].append(peer_data)

    # Optionally, remove peers that have not announced in a while to avoid memory bloat
    # for key in list(peers.keys()):
    #     peers[key] = [p for p in peers[key] if time.time() - p['last_announce'] < 60]

    # Generate a list of peers to respond with (you can limit the number of peers here)
    peer_list = []
    for peer in peers[info_hash]:
        peer_list.append(f"{peer['ip']}:{peer['port']}")

    # Prepare the response in the BitTorrent format (using the 'bencode' style)
    response = {
        'interval': 1800,  # Time in seconds before the client should announce again
        'peers': peer_list  # List of peers in "IP:port" format
    }

    return jsonify(response)


if __name__ == '__main__':
    # Run the server
    app.run(host='0.0.0.0', port=6881)  # Use port 6969 (default for trackers)
