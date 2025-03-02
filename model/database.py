import sqlite3

class Database:
    def __init__(self, db_name='medical_records.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fio TEXT,
                address TEXT,
                birth_date TEXT,
                appointment_date TEXT,
                doctor_fio TEXT,
                conclusion TEXT
            )
        ''')
        self.conn.commit()

    def add_record(self, record):
        self.cursor.execute('''
            INSERT INTO records (fio, address, birth_date, appointment_date, doctor_fio, conclusion)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (record['fio'], record['address'], record['birth_date'], record['appointment_date'], record['doctor_fio'], record['conclusion']))
        self.conn.commit()

    def search_records(self, conditions):
        query = 'SELECT * FROM records WHERE '
        query += ' AND '.join([f"{key} = ?" for key in conditions.keys()])
        self.cursor.execute(query, list(conditions.values()))
        return self.cursor.fetchall()

    def delete_records(self, conditions):
        query = 'DELETE FROM records WHERE '
        query += ' AND '.join([f"{key} = ?" for key in conditions.keys()])
        self.cursor.execute(query, list(conditions.values()))
        self.conn.commit()
        return self.cursor.rowcount

    def get_all_records(self):
        self.cursor.execute('SELECT * FROM records')
        return self.cursor.fetchall()