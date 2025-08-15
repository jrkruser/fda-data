import psycopg2
from pathlib import Path
from drug_data_pipeline.utils.db import get_connection

def main():
    schema_path = Path(__file__).parent / "schema" / "v001__initial_schema.sql"
    print(f"Applying schema from {schema_path}...")

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found at {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(schema_sql)
    conn.commit()
    cur.close()
    conn.close()
    print("Schema applied successfully.")

if __name__ == "__main__":
    main()
