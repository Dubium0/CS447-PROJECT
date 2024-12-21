from dataclasses import dataclass

@dataclass
class TorrentItem:
    name: str
    file_path: str
    download_speed: str
    upload_speed: str
    completion_percentage: str
    status: str