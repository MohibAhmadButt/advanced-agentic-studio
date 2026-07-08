import sqlite3
import os
import pandas as pd
from config import DB_FILE, OUTPUT_DIR

def init_db():
    """Initializes the relational schema ledger with image analytics support."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                core_concept TEXT,
                art_style TEXT,
                lighting TEXT,
                framing TEXT,
                modifier TEXT,
                agent_logic TEXT,
                expanded_prompt TEXT,
                image_path TEXT,
                dominant_color TEXT,
                contrast_score REAL,
                human_reward INTEGER DEFAULT -1
            )
        """)

def insert_generation(timestamp, concept, style, lighting, framing, modifier, logic, expanded, path, dominant_color, contrast_score):
    """Inserts a new generation record alongside its pixel analytics arrays."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO portfolio (timestamp, core_concept, art_style, lighting, framing, modifier, agent_logic, expanded_prompt, image_path, dominant_color, contrast_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, concept, style, lighting, framing, modifier, logic, expanded, path, dominant_color, contrast_score))
        return cursor.lastrowid

def update_reward(record_id, score):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("UPDATE portfolio SET human_reward = ? WHERE id = ?", (score, record_id))

def get_all_records():
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT id, image_path, core_concept, art_style FROM portfolio ORDER BY id DESC", conn)
    if df.empty:
        return []
    return [(row['image_path'], f"#{row['id']} | {row['core_concept']} ({row['art_style']})") for _, row in df.iterrows()]

def get_single_record(record_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM portfolio WHERE id = ?", (record_id,))
        return cursor.fetchone()

def export_vault_to_csv():
    """Compiles the SQLite log ledger cleanly into a downloadable dataset file."""
    export_path = "studio_vault_export.csv"
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT * FROM portfolio ORDER BY id DESC", conn)
    df.to_csv(export_path, index=False)
    return export_path