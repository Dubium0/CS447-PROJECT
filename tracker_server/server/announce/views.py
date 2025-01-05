from flask import request, jsonify
from . import announce_blueprint
from ...database.operations.announce import *

@announce_blueprint.route('', methods=['GET'])
def announce():
    info_hash = request.args.get('info_hash')
    peer_id = request.args.get('peer_id')
    ip = request.args.get('ip')
    port = request.args.get('port')
    event = request.args.get('event')
    uploaded = request.args.get('uploaded')
    downloaded = request.args.get('downloaded')
    left = request.args.get('left')

    if not all([info_hash, peer_id, ip, port]):
        return jsonify({'error': 'Missing required parameters'}), 400

    if not is_torrent_tracked(info_hash):
        res = track_torrent(info_hash)

        if not res:
            return jsonify({'error': 'Internal server error'}), 500

    if not is_peer_tracked(info_hash, peer_id, ip, port):
        res = track_peer(info_hash, peer_id, ip, port, uploaded, downloaded, left, event)

        if not res:
            return jsonify({'error': 'Internal server error'}), 500

    remove_old_peers(info_hash)

    peers = get_peers_for_torrent(info_hash, peer_id, ip, port)
    if not peers:
        return jsonify({'error': 'Internal server error'}), 500

    # Prepare the response in the BitTorrent format
    response = {
        'interval': 1800,  # Time in seconds before the client should announce again
        'peers': [f"{peer['ip']}:{peer['port']}" for peer in peers],
        'peers_with_file': [f"{peer['ip']}:{peer['port']}" for peer in peers if peer['has_file'] == 1]
    }

    return jsonify(response)