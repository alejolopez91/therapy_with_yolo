import sqlite3
from typing import List, Optional
from contextlib import contextmanager
from models.exercise import Exercise, Session

class DatabaseManager:
    def __init__(self, db_path: str = 'yolo_pose_estimation.db'):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def dict_factory(self, cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}