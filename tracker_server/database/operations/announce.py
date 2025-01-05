from ..database import Database

def is_torrent_tracked(info_hash):
    """
    Check if a torrent with the given info_hash is being tracked.

    :param info_hash: The info_hash of the torrent to check.
    :return: True if the torrent is tracked, False otherwise.
    """
    conn = Database().connect()
    result = None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM torrents WHERE info_hash = ?", (info_hash,))

        result = cursor.fetchone()

    except Exception as e:
        print(f"Error checking if torrent is tracked: {e}")
        result = False

    finally:
        conn.close()

    return result if result else False



def track_torrent(info_hash):
    """
    Track a torrent by inserting its info_hash into the database.

    :param info_hash: The info_hash of the torrent to track.
    :return: True if the torrent was successfully tracked, False otherwise.
    """
    conn = Database().connect()
    result = None

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO torrents (info_hash, added_at, last_checked)
            VALUES (?, DATETIME('now'), DATETIME('now'))
            """,
            (info_hash,)
        )

        conn.commit()
        result = True

    except Exception as e:
        print(f"Error tracking {info_hash}: {e}")
        conn.rollback()
        result = False

    finally:
        conn.close()

    return result if result else False

def is_peer_tracked(info_hash, peer_id, ip, port):
    """
    Check if a peer with the given info_hash, peer_id, ip, and port is already being tracked.

    :param info_hash: The info_hash of the torrent the peer is associated with.
    :param peer_id: The unique identifier of the peer.
    :param ip: The IP address of the peer.
    :param port: The port of the peer.
    :return: True if the peer is tracked, False otherwise.
    """
    conn = Database().connect()
    result = None

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 1 FROM peers 
            WHERE info_hash = ? AND peer_id = ? AND ip = ? AND port = ?
            """,
            (info_hash, peer_id, ip, port)
        )

        result = cursor.fetchone()

    except Exception as e:
        print(f"Error checking if peer is tracked: {e}")
        result = False

    finally:
        conn.close()

    return result if result else False

def track_peer(info_hash, peer_id, ip, port, uploaded, downloaded, remaining, event=None, has_file=0):
    """
    Track a peer by inserting its information into the database.

    :param info_hash: The info_hash of the torrent the peer is associated with.
    :param peer_id: The unique identifier of the peer.
    :param ip: The IP address of the peer.
    :param port: The port of the peer.
    :param uploaded: Amount uploaded by the peer.
    :param downloaded: Amount downloaded by the peer.
    :param remaining: Amount remaining for the peer to download.
    :param event: Event (optional) like 'started', 'completed', or 'stopped'.
    :return: True if the peer was successfully tracked, False otherwise.
    """
    conn = Database().connect()
    result = None

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO peers (info_hash, peer_id, ip, port, uploaded, downloaded, remaining, event, has_file, last_announce)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, DATETIME('now'))
            """,
            (info_hash, peer_id, ip, port, uploaded, downloaded, remaining, event, has_file)
        )

        conn.commit()
        result = True

    except Exception as e:
        print(f"Error tracking peer {peer_id} for torrent {info_hash}: {e}")
        conn.rollback()
        result = False

    finally:
        conn.close()

    return result if result else False

def remove_old_peers(info_hash, time_limit='1 hour'):
    """
    Remove peers for a specific torrent (info_hash) who haven't announced in the last 'time_limit'.

    :param info_hash: The info_hash of the torrent to remove peers for.
    :param time_limit: The time window in which a peer must have announced to be considered active (default is 1 hour).
    :return: True if the old peers were successfully removed, False otherwise.
    """
    conn = Database().connect()
    result = None

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM peers
            WHERE info_hash = ? AND last_announce < DATETIME('now', ?)
            """,
            (info_hash, f"-{time_limit}")
        )

        conn.commit()
        result = True

    except Exception as e:
        print(f"Error removing old peers for torrent {info_hash}: {e}")
        conn.rollback()
        result = False

    finally:
        conn.close()

    return result if result else False

def get_peers_for_torrent(info_hash, exclude_peer_id=None, exclude_ip=None, exclude_port=None):
    """
    Get a list of peers associated with the given torrent (info_hash),
    excluding the peer making the request.

    :param info_hash: The info_hash of the torrent to get peers for.
    :param exclude_peer_id: The peer_id to exclude from the list.
    :param exclude_ip: The IP address to exclude from the list.
    :param exclude_port: The port to exclude from the list.
    :return: A list of peers (peer_id, ip, port) for the torrent, excluding the given peer OR None.
    """
    conn = Database().connect()
    peers = []

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT peer_id, ip, port, uploaded, downloaded, remaining, event, has_file, last_announce
            FROM peers
            WHERE info_hash = ?
            """,
            (info_hash,)
        )

        rows = cursor.fetchall()

        for row in rows:
            if (exclude_peer_id and row[0] == exclude_peer_id) and \
               (exclude_ip and row[1] == exclude_ip) and \
               (exclude_port and row[2] == exclude_port):
                continue

            peers.append({
                'peer_id': row[0],
                'ip': row[1],
                'port': row[2],
                'uploaded': row[3],
                'downloaded': row[4],
                'remaining': row[5],
                'event': row[6],
                'has_file': row[7],
                'last_announce': row[8]
            })

    except Exception as e:
        print(f"Error fetching peers for torrent {info_hash}: {e}")
        peers = None

    finally:
        conn.close()

    return peers












