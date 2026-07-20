import sqlite3

DB_NAME = "resume_screening.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS screening_results(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate TEXT,

            semantic_score REAL,

            skill_score REAL,

            final_score REAL,

            recommendation TEXT

        )
    """)

    conn.commit()
    conn.close()
def save_results(results):

    conn = get_connection()

    cursor = conn.cursor()

    for candidate in results:

        cursor.execute("""
            INSERT INTO screening_results
            (
                candidate,
                semantic_score,
                skill_score,
                final_score,
                recommendation
            )

            VALUES (?,?,?,?,?)
        """,

        (
            candidate["candidate"],
            candidate["semantic_score"],
            candidate["skill_score"],
            candidate["final_score"],
            candidate["recommendation"]
        ))

    conn.commit()
    conn.close()
import pandas as pd

def load_history():

    conn = get_connection()

    df = pd.read_sql_query(

        "SELECT * FROM screening_results",

        conn

    )

    conn.close()

    return df