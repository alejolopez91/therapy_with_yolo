from typing import List, Optional
from models.exercise import Exercise
from db.database_manager import DatabaseManager

class ExerciseRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create(self, exercise: Exercise) -> Exercise:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO exercises (name, description)
                VALUES (?, ?)
                ''', (exercise.name, exercise.description))
            conn.commit()
            exercise.id = cursor.lastrowid
            return exercise

    def get(self, exercise_id: int) -> Optional[Exercise]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM exercises WHERE id = ?', (exercise_id,))
            row = cursor.fetchone()
            return Exercise(id=row[0], name=row[1], description=row[2]) if row else None

    def get_all(self) -> List[Exercise]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM exercises')
            return [Exercise(id=row[0], name=row[1], description=row[2]) 
                   for row in cursor.fetchall()]

    def update(self, exercise: Exercise) -> bool:
        if not exercise.id:
            return False
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE exercises 
                SET name = ?, description = ?
                WHERE id = ?
                ''', (exercise.name, exercise.description, exercise.id))
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, exercise_id: int) -> bool:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM exercises WHERE id = ?', (exercise_id,))
            conn.commit()
            return cursor.rowcount > 0