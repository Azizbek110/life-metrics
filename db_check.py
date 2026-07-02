import sqlite3
import pandas as pd

conn = sqlite3.connect(r"d:\life_metrics\data\metrics.db")
df = pd.read_sql("SELECT * FROM entries", conn)
print(df)

