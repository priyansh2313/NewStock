import sqlite3
import hashlib
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('stockapp.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            subscription_status TEXT DEFAULT 'free'
        )
        ''')

        # Subscriptions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plan_type TEXT,
            active BOOLEAN,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        self.conn.commit()

    def add_user(self, email, password):
        cursor = self.conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute(
                'INSERT INTO users (email, password) VALUES (?, ?)',
                (email, hashed_password)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, email, password):
        cursor = self.conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(
            'SELECT id, email FROM users WHERE email = ? AND password = ?',
            (email, hashed_password)
        )
        user = cursor.fetchone()
        return user if user else None

    def get_subscription_status(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT subscription_status FROM users WHERE id = ?',
            (user_id,)
        )
        return cursor.fetchone()[0]

    def update_subscription(self, user_id, plan_type):
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE users SET subscription_status = ? WHERE id = ?',
            (plan_type, user_id)
        )
        self.conn.commit()
