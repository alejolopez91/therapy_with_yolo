import sqlite3

def initialize_database():
    conn = sqlite3.connect('yolo_pose_estimation.db')
    cursor = conn.cursor()

    # Create exercises table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    ''')

    # Create sessions table 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        reps INTEGER,
        FOREIGN KEY (exercise_id) REFERENCES exercises (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS joints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        points TEXT NOT NULL  -- Store array as JSON string
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()