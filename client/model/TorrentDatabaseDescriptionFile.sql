CREATE TABLE IF NOT EXISTS download_info_locations (
    path TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS has_file (
    info_hash TEXT PRIMARY KEY,
    has INTEGER NOT NULL DEFAULT 0
);