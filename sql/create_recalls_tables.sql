CREATE TABLE IF NOT EXISTS fda_data.drug_enforcement (
    event_id TEXT PRIMARY KEY,
    status TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    classification TEXT,
    product_type TEXT,
    recalling_firm TEXT,
    address_1 TEXT,
    address_2 TEXT,
    postal_code TEXT,
    voluntary_mandated TEXT,
    initial_firm_notification TEXT,
    distribution_pattern TEXT,
    recall_number TEXT,
    product_description TEXT,
    product_quantity TEXT,
    reason_for_recall TEXT,
    recall_initiation_date DATE,
    center_classification_date DATE,
    termination_date DATE,
    report_date DATE,
    code_info TEXT,
    more_code_info TEXT
);


CREATE TABLE IF NOT EXISTS fda_data.drug_enforcement_openfda (
    id SERIAL PRIMARY KEY,
    event_id TEXT REFERENCES fda_data.drug_enforcement(event_id) ON DELETE CASCADE,
    application_number TEXT,
    brand_name TEXT,
    generic_name TEXT,
    manufacturer_name TEXT,
    product_ndc TEXT,
    product_type TEXT,
    route TEXT,
    substance_name TEXT,
    rxcui TEXT,
    spl_id TEXT,
    spl_set_id TEXT,
    package_ndc TEXT,
    is_original_packager BOOLEAN,
    upc TEXT,
    unii TEXT
);

