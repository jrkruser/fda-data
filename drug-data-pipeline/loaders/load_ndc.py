import json
import psycopg2
import sys
from datetime import datetime

# --- CONFIG ---
DB_NAME = "fda_data"
DB_USER = "admin"
DB_PASS = "admin"
DB_HOST = "localhost"
DB_PORT = "5434"

# --- ARGUMENT CHECK ---
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_ndc_json>")
    sys.exit(1)

input_file = sys.argv[1]

# --- DB CONNECT ---
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# --- LOAD JSON ---
with open(input_file, "r") as f:
    data = json.load(f)["results"]

for product in data:
    # extract only needed fields
    product_row = (
        product.get("product_ndc"),
        product.get("generic_name"),
        product.get("labeler_name"),
        product.get("brand_name"),
        product.get("brand_name_suffix"),
        product.get("finished"),
        datetime.strptime(product.get("listing_expiration_date"), "%Y%m%d").date()
            if product.get("listing_expiration_date") else None,
        product.get("marketing_category"),
        product.get("dosage_form"),
        product.get("product_type"),
        datetime.strptime(product.get("marketing_start_date"), "%Y%m%d").date()
            if product.get("marketing_start_date") else None,
        product.get("application_number"),
        product.get("brand_name_base")
    )

    # insert product
    cur.execute("""
        INSERT INTO fda_data.ndc_product
        (product_ndc, generic_name, labeler_name, brand_name, brand_name_suffix, finished,
         listing_expiration_date, marketing_category, dosage_form, product_type,
         marketing_start_date, application_number, brand_name_base)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (product_ndc) DO NOTHING
    """, product_row)

    # insert active ingredients
    for ai in product.get("active_ingredients", []):
        cur.execute("""
            INSERT INTO fda_data.ndc_active_ingredient
            (product_ndc, ingredient_name, strength)
            VALUES (%s, %s, %s)
        """, (product.get("product_ndc"), ai.get("name"), ai.get("strength")))

conn.commit()
cur.close()
conn.close()
