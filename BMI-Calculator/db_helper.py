import sqlite3


def init_db():
    conn = sqlite3.connect('bmi_calculator.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create bmi_records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()


def insert_bmi_record(user_id, weight, height, bmi, category, timestamp):
    print(f"Debug: Inserting - user_id: {user_id}, weight: {weight}, height: {height}, bmi: {bmi}, category: {category}, timestamp: {timestamp}")
    conn = sqlite3.connect('bmi_calculator.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO bmi_records (user_id, weight, height, bmi, category, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
        (user_id, weight, height, bmi, category, timestamp))
    conn.commit()
    conn.close()


def get_bmi_records(user_id):
    conn = sqlite3.connect('bmi_calculator.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bmi_records WHERE user_id = ?', (user_id,))
    records = cursor.fetchall()
    conn.close()

    # Debug: Print retrieved records
    print(f"Debug: Retrieved records for user_id {user_id}:")
    for record in records:
        print(record)

    return records
