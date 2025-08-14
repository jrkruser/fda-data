CREATE TABLE IF NOT EXISTS fda_data.drug_shortage (
    id SERIAL PRIMARY KEY,
    update_type TEXT,
    initial_posting_date DATE,
    discontinued_date DATE,
    change_date DATE,
    proprietary_name TEXT,
    package_ndc TEXT,
    generic_name TEXT,
    contact_info TEXT,
    availability TEXT,
    related_info TEXT,
    resolved_note TEXT,
    update_date DATE,
    dosage_form TEXT,
    presentation TEXT,
    company_name TEXT,
    status TEXT
);


CREATE TABLE IF NOT EXISTS fda_data.drug_shortage_strength (
    id SERIAL PRIMARY KEY,
    shortage_id INT REFERENCES fda_data.drug_shortage(id) ON DELETE CASCADE,
    strength TEXT
);


CREATE TABLE IF NOT EXISTS fda_data.drug_shortage_therapeutic_category (
    id SERIAL PRIMARY KEY,
    shortage_id INT REFERENCES fda_data.drug_shortage(id) ON DELETE CASCADE,
    category TEXT
);


CREATE TABLE IF NOT EXISTS fda_data.drug_shortage_openfda (
    id SERIAL PRIMARY KEY,
    shortage_id INT REFERENCES fda_data.drug_shortage(id) ON DELETE CASCADE,
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
    unii TEXT
);