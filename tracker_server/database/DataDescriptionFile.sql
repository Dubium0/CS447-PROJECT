CREATE TABLE IF NOT EXISTS torrents (
    info_hash BLOB PRIMARY KEY,
    name TEXT NOT NULL,
    size INTEGER,
    seeders INTEGER DEFAULT 0,
    leechers INTEGER DEFAULT 0,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_checked TIMESTAMP
);

CREATE TABLE IF NOT EXISTS peers (
    info_hash BLOB NOT NULL,
    peer_id TEXT NOT NULL,
    ip TEXT NOT NULL,
    port INTEGER NOT NULL,
    uploaded INTEGER NOT NULL,
    downloaded INTEGER NOT NULL,
    remaining INTEGER NOT NULL,
    event TEXT,
    last_announce TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (info_hash, peer_id, ip, port),
    FOREIGN KEY (info_hash) REFERENCES torrents(info_hash) ON DELETE CASCADE
);
