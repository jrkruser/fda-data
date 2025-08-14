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
    print(f"Usage: python {sys.argv[0]} <path_to_recalls_json>")
    sys.exit(1)

input_file = sys.argv[1]

# --- DATE PARSER ---
def parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, "%Y%m%d").date()
    except ValueError:
        return None

# --- DB CONNECTION ---
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
    data = json.load(f)

# --- INSERT DATA ---
for record in data.get("results", []):
    event_id = record.get("event_id")

    # Insert into main table
    cur.execute("""
        INSERT INTO fda_data.drug_enforcement (
            event_id, status, city, state, country, classification,
            product_type, recalling_firm, address_1, address_2,
            postal_code, voluntary_mandated, initial_firm_notification,
            distribution_pattern, recall_number, product_description,
            product_quantity, reason_for_recall, recall_initiation_date,
            center_classification_date, termination_date, report_date,
            code_info, more_code_info
        ) VALUES (
            %(event_id)s, %(status)s, %(city)s, %(state)s, %(country)s, %(classification)s,
            %(product_type)s, %(recalling_firm)s, %(address_1)s, %(address_2)s,
            %(postal_code)s, %(voluntary_mandated)s, %(initial_firm_notification)s,
            %(distribution_pattern)s, %(recall_number)s, %(product_description)s,
            %(product_quantity)s, %(reason_for_recall)s, %(recall_initiation_date)s,
            %(center_classification_date)s, %(termination_date)s, %(report_date)s,
            %(code_info)s, %(more_code_info)s
        )
        ON CONFLICT (event_id) DO NOTHING;
    """, {
        "event_id": event_id,
        "status": record.get("status"),
        "city": record.get("city"),
        "state": record.get("state"),
        "country": record.get("country"),
        "classification": record.get("classification"),
        "product_type": record.get("product_type"),
        "recalling_firm": record.get("recalling_firm"),
        "address_1": record.get("address_1"),
        "address_2": record.get("address_2"),
        "postal_code": record.get("postal_code"),
        "voluntary_mandated": record.get("voluntary_mandated"),
        "initial_firm_notification": record.get("initial_firm_notification"),
        "distribution_pattern": record.get("distribution_pattern"),
        "recall_number": record.get("recall_number"),
        "product_description": record.get("product_description"),
        "product_quantity": record.get("product_quantity"),
        "reason_for_recall": record.get("reason_for_recall"),
        "recall_initiation_date": parse_date(record.get("recall_initiation_date")),
        "center_classification_date": parse_date(record.get("center_classification_date")),
        "termination_date": parse_date(record.get("termination_date")),
        "report_date": parse_date(record.get("report_date")),
        "code_info": record.get("code_info"),
        "more_code_info": record.get("more_code_info")
    })

    # Insert into openfda sub-table if exists
    openfda_list = record.get("openfda", [])
    if isinstance(openfda_list, dict):
        openfda_list = [openfda_list]

    for openfda in openfda_list:
        cur.execute("""
            INSERT INTO fda_data.drug_enforcement_openfda (
                event_id, application_number, brand_name, generic_name,
                manufacturer_name, product_ndc, product_type, route,
                substance_name, rxcui, spl_id, spl_set_id, package_ndc,
                is_original_packager, upc, unii
            ) VALUES (
                %(event_id)s, %(application_number)s, %(brand_name)s, %(generic_name)s,
                %(manufacturer_name)s, %(product_ndc)s, %(product_type)s, %(route)s,
                %(substance_name)s, %(rxcui)s, %(spl_id)s, %(spl_set_id)s, %(package_ndc)s,
                %(is_original_packager)s, %(upc)s, %(unii)s
            );
        """, {
            "event_id": event_id,
            "application_number": ",".join(openfda.get("application_number", [])),
            "brand_name": ",".join(openfda.get("brand_name", [])),
            "generic_name": ",".join(openfda.get("generic_name", [])),
            "manufacturer_name": ",".join(openfda.get("manufacturer_name", [])),
            "product_ndc": ",".join(openfda.get("product_ndc", [])),
            "product_type": ",".join(openfda.get("product_type", [])),
            "route": ",".join(openfda.get("route", [])),
            "substance_name": ",".join(openfda.get("substance_name", [])),
            "rxcui": ",".join(openfda.get("rxcui", [])),
            "spl_id": ",".join(openfda.get("spl_id", [])),
            "spl_set_id": ",".join(openfda.get("spl_set_id", [])),
            "package_ndc": ",".join(openfda.get("package_ndc", [])),
            "is_original_packager": openfda.get("is_original_packager", [None])[0] if openfda.get("is_original_packager") else None,
            "upc": ",".join(openfda.get("upc", [])),
            "unii": ",".join(openfda.get("unii", []))
        })

conn.commit()
cur.close()
conn.close()
