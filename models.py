from base import get_connection


def save_entry(date, sleep_hours, sleep_quality, mood, water_ml, screen_min, weight_kg, notes=""):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO entries (date, sleep_hours, sleep_quality, mood, water_ml, screen_min, weight_kg, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
                sleep_hours   = excluded.sleep_hours,
                sleep_quality = excluded.sleep_quality,
                mood          = excluded.mood,
                water_ml      = excluded.water_ml,
                screen_min    = excluded.screen_min,
                weight_kg     = excluded.weight_kg,
                notes         = excluded.notes
        """, (date, sleep_hours, sleep_quality, mood, water_ml, screen_min, weight_kg, notes))



def get_entry_by_date(date):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM entries WHERE date = ?", (date,)
        ).fetchone()
        return dict(row) if row else None


def get_all_entries():
    import pandas as pd
    with get_connection() as conn:
        return pd.read_sql("SELECT * FROM entries ORDER BY date DESC", conn)


def delete_entry(date):
    with get_connection() as conn:
        conn.execute("DELETE FROM entries WHERE date = ?", (date,))