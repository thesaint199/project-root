from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/postgres")

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        );
    """)
    cursor.execute("""
        INSERT INTO messages (content) VALUES ('Hello, World!') ON CONFLICT DO NOTHING;
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def get_message():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM messages LIMIT 1;")
    message = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({"message": message[0] if message else "No message found!"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
