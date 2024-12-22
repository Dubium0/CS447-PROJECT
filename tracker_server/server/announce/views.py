from flask import request, jsonify
import time
from . import announce_blueprint

peers = {}

@announce_blueprint.route('', methods=['GET'])
def announce():
    # Parse the incoming parameters
    info_hash = request.args.get('info_hash')  # Hash of the torrent file
    peer_id = request.args.get('peer_id')  # Unique peer ID
    ip = request.args.get('ip')  # Peer IP address
    port = request.args.get('port')  # Peer port
    event = request.args.get('event')  # Event like 'started', 'completed', 'stopped'
    uploaded = request.args.get('uploaded')  # Amount uploaded
    downloaded = request.args.get('downloaded')  # Amount downloaded
    left = request.args.get('left')  # Amount left (number of bytes remaining)

    # Ensure the necessary parameters are present
    if not all([info_hash, peer_id, ip, port]):
        return jsonify({'error': 'Missing required parameters'}), 400

    # Initialize peer list if not already present for this torrent (info_hash)
    if info_hash not in peers:
        peers[info_hash] = []

    # Store or update peer information
    peer_data = {
        'peer_id': peer_id,
        'ip': ip,
        'port': port,
        'last_announce': time.time(),
        'uploaded': uploaded,
        'downloaded': downloaded,
        'left': left
    }

    # Add the peer to the list of peers for this torrent
    peers[info_hash].append(peer_data)

    # Optionally, remove peers that have not announced in a while to avoid memory bloat
    # For example, remove peers that have not announced in the last 5 minutes
    for key in list(peers.keys()):
        peers[key] = [p for p in peers[key] if time.time() - p['last_announce'] < 300]

    # Generate a list of peers to respond with (you can limit the number of peers here)
    peer_list = []
    for peer in peers[info_hash]:
        peer_list.append(f"{peer['ip']}:{peer['port']}")

    # Prepare the response in the BitTorrent format
    response = {
        'interval': 1800,  # Time in seconds before the client should announce again
        'peers': peer_list  # List of peers in "IP:port" format
    }

    # Return the response as JSON
    return jsonify(response)