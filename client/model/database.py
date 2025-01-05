import sqlite3, os, sys

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'database_path'):
            base_path = os.path.dirname(os.path.abspath(__file__))
            self.database_path = os.path.join(base_path, 'data.db')

            init_conn = sqlite3.connect(self.database_path)
            init_cursor = init_conn.cursor()

            data_description_file_path = os.path.join(base_path, 'TorrentDatabaseDescriptionFile.sql')

            try:
                with open(data_description_file_path, 'r') as data_file:
                    sql_script = data_file.read()

                init_cursor.executescript(sql_script)
                init_conn.commit()

                print("Database initialized successfully")
            except Exception as e:
                print(f"Database initialization failed: {e}")
                init_conn.rollback()
                init_cursor.close()
                init_conn.close()
                sys.exit(1)
            finally:
                init_cursor.close()
                init_conn.close()

    def connect(self):
        return sqlite3.connect(self.database_path)