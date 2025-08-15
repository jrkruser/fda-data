import json
import sys
import os
from drug_data_pipeline.utils.db import get_connection, parse_date


def load_ndc(input_file: str):
    input_file = os.path.abspath(input_file)

    conn = get_connection()
    cur = conn.cursor()

    with open(input_file, "r") as f:
        data = json.load(f)["results"]

    for product in data:
        product_row = (
            product.get("product_ndc"),
            product.get("generic_name"),
            product.get("labeler_name"),
            product.get("brand_name"),
            product.get("brand_name_suffix"),
            product.get("finished"),
            parse_date(product.get("listing_expiration_date")),
            product.get("marketing_category"),
            product.get("dosage_form"),
            product.get("product_type"),
            parse_date(product.get("marketing_start_date")),
            product.get("application_number"),
            product.get("brand_name_base")
        )

        cur.execute("""
            INSERT INTO fda_data.ndc_product
            (product_ndc, generic_name, labeler_name, brand_name, brand_name_suffix, finished,
             listing_expiration_date, marketing_category, dosage_form, product_type,
             marketing_start_date, application_number, brand_name_base)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (product_ndc) DO NOTHING
        """, product_row)

        for ai in product.get("active_ingredients", []):
            cur.execute("""
                INSERT INTO fda_data.ndc_active_ingredient
                (product_ndc, ingredient_name, strength)
                VALUES (%s, %s, %s)
            """, (
                product.get("product_ndc"),
                ai.get("name"),
                ai.get("strength")
            ))

    conn.commit()
    cur.close()
    conn.close()

    print(f"Loaded {len(data)} NDC product records successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python -m drug_data_pipeline.loaders.load_ndc <path_to_json>")
        sys.exit(1)
    load_ndc(sys.argv[1])
