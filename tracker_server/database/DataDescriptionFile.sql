CREATE TABLE IF NOT EXISTS torrents (
    info_hash TEXT PRIMARY KEY,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_checked TIMESTAMP
);

CREATE TABLE IF NOT EXISTS peers (
    info_hash TEXT NOT NULL,
    peer_id TEXT NOT NULL,
    ip TEXT NOT NULL,
    port INTEGER NOT NULL,
    uploaded INTEGER,
    downloaded INTEGER,
    remaining INTEGER,
    event TEXT,
    has_file INTEGER NOT NULL DEFAULT 0,
    last_announce TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (info_hash, peer_id, ip, port),
    FOREIGN KEY (info_hash) REFERENCES torrents(info_hash) ON DELETE CASCADE
);
