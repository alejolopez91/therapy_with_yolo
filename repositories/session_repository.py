from typing import List, Optional
from models.exercise import Session
from db.database_manager import DatabaseManager

class SessionRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create(self, session: Session) -> Session:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sessions (exercise_id, reps, timestamp)
                VALUES (?, ?, ?)
                ''', (session.exercise_id, session.reps, session.timestamp))
            conn.commit()
            session.id = cursor.lastrowid
            return session

    def get(self, session_id: int) -> Optional[Session]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sessions WHERE id = ?', (session_id,))
            row = cursor.fetchone()
            return Session(
                id=row[0],
                exercise_id=row[1],
                reps=row[3],
                timestamp=row[2]
            ) if row else None

    def get_by_exercise(self, exercise_id: int) -> List[Session]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sessions WHERE exercise_id = ?', (exercise_id,))
            return [Session(
                id=row[0],
                exercise_id=row[1],
                reps=row[3],
                timestamp=row[2]
            ) for row in cursor.fetchall()]