import json
import psycopg2
import sys
from datetime import datetime

"""
Loader uploads current snapshot for the sake of testing the db table design. No historical backlog needed, this for ensuring proper table structure.
Logic will be tweeked slightly for future script for daily update.
"""

# --- CONFIG ---
DB_NAME = "fda_data"
DB_USER = "admin"
DB_PASS = "admin"
DB_HOST = "localhost"
DB_PORT = "5434"

# --- ARGUMENT CHECK ---
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_shortages_json>")
    sys.exit(1)

input_file = sys.argv[1]

# --- DATE PARSER ---
def parse_date(val):
    try:
        if val and len(val) == 10:  # format like YYYY-MM-DD
            return datetime.strptime(val, "%Y-%m-%d").date()
        elif val and len(val) == 8:  # format like YYYYMMDD
            return datetime.strptime(val, "%Y%m%d").date()
    except Exception:
        pass
    return None

# --- CONNECT ---
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# --- LOAD JSON ---
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

records = data.get("results", [])

for r in records:
    # Insert into main shortages table
    cur.execute("""
        INSERT INTO fda_data.drug_shortage (
            update_type, initial_posting_date, discontinued_date, change_date,
            proprietary_name, package_ndc, generic_name, contact_info,
            availability, related_info, resolved_note, update_date,
            dosage_form, presentation, company_name, status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        r.get("update_type"),
        parse_date(r.get("initial_posting_date")),
        parse_date(r.get("discontinued_date")),
        parse_date(r.get("change_date")),
        r.get("proprietary_name"),
        r.get("package_ndc"),
        r.get("generic_name"),
        r.get("contact_info"),
        r.get("availability"),
        r.get("related_info"),
        r.get("resolved_note"),
        parse_date(r.get("update_date")),
        r.get("dosage_form"),
        r.get("presentation"),
        r.get("company_name"),
        r.get("status")
    ))

    shortage_id = cur.fetchone()[0]

    # Strength list
    for s in r.get("strength", []):
        cur.execute("""
            INSERT INTO fda_data.drug_shortage_strength (shortage_id, strength)
            VALUES (%s, %s)
        """, (shortage_id, s))

    # Therapeutic category list
    for cat in r.get("therapeutic_category", []):
        cur.execute("""
            INSERT INTO fda_data.drug_shortage_therapeutic_category (shortage_id, category)
            VALUES (%s, %s)
        """, (shortage_id, cat))

    # OpenFDA data
    openfda = r.get("openfda", {})
    cur.execute("""
        INSERT INTO fda_data.drug_shortage_openfda (
            shortage_id, application_number, brand_name, generic_name,
            manufacturer_name, product_ndc, product_type, route,
            substance_name, rxcui, spl_id, spl_set_id, package_ndc, unii
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """, (
        shortage_id,
        ", ".join(openfda.get("application_number", [])),
        ", ".join(openfda.get("brand_name", [])),
        ", ".join(openfda.get("generic_name", [])),
        ", ".join(openfda.get("manufacturer_name", [])),
        ", ".join(openfda.get("product_ndc", [])),
        ", ".join(openfda.get("product_type", [])),
        ", ".join(openfda.get("route", [])),
        ", ".join(openfda.get("substance_name", [])),
        ", ".join(openfda.get("rxcui", [])),
        ", ".join(openfda.get("spl_id", [])),
        ", ".join(openfda.get("spl_set_id", [])),
        ", ".join(openfda.get("package_ndc", [])),
        ", ".join(openfda.get("unii", []))
    ))

# --- COMMIT & CLOSE ---
conn.commit()
cur.close()
conn.close()

print(f"Loaded {len(records)} drug shortage records successfully.")


