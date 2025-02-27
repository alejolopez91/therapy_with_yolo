from typing import List, Optional
import json
from models.joint import Joint
from db.database_manager import DatabaseManager

class JointRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create(self, joint: Joint) -> Joint:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            points_json = json.dumps(joint.points)  # Convert array to JSON string
            cursor.execute('''
                INSERT INTO joints (name, points)
                VALUES (?, ?)
                ''', (joint.name, points_json))
            conn.commit()
            joint.id = cursor.lastrowid
            return joint

    def get(self, joint_id: int) -> Optional[Joint]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM joints WHERE id = ?', (joint_id,))
            row = cursor.fetchone()
            if row:
                points = json.loads(row[2])  # Convert JSON string back to array
                return Joint(id=row[0], name=row[1], points=points)
            return None

    def get_all(self) -> List[Joint]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM joints')
            return [Joint(
                id=row[0],
                name=row[1],
                points=json.loads(row[2])
            ) for row in cursor.fetchall()]

    def update(self, joint: Joint) -> bool:
        if not joint.id:
            return False
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            points_json = json.dumps(joint.points)
            cursor.execute('''
                UPDATE joints 
                SET name = ?, points = ?
                WHERE id = ?
                ''', (joint.name, points_json, joint.id))
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, joint_id: int) -> bool:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM joints WHERE id = ?', (joint_id,))
            conn.commit()
            return cursor.rowcount > 0