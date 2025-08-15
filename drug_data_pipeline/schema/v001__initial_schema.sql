-- FDA Drug Data Pipeline Schema
-- Version: v001
-- Run with: psql -U admin -d fda_data -f v001__initial_schema.sql

create schema if not exists fda_data;

-- NDC Tables
-- main NDC product table
create table if not exists fda_data.ndc_product (
    product_ndc text primary key,
    generic_name text,
    labeler_name text,
    brand_name text,
    brand_name_suffix text,
    finished boolean,
    listing_expiration_date date,
    marketing_category text,
    dosage_form text,
    product_type text,
    marketing_start_date date,
    application_number text,
    brand_name_base text
);

-- active ingredients table
create table if not exists fda_data.ndc_active_ingredient (
    id serial primary key,
    product_ndc text references fda_data.ndc_product(product_ndc) on delete cascade,
    ingredient_name text,
    strength text
);


-- Recall Tables
-- main recal table
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


-- Shortages Tables

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



-- Adverse Events Tables

-- Main table: one row per safety report
create table if not exists fda_data.drug_event (
    safetyreportid text primary key,
    safetyreportversion text,
    primarysourcecountry text,
    transmissiondate date,
    reporttype text,
    serious text,
    seriousnessdeath text,
    seriousnesslifethreatening text,
    seriousnesshospitalization text,
    seriousnessdisabling text,
    seriousnesscongenitalanomali text,
    seriousnessother text,
    receivedate date,
    receiptdate date,
    fulfillexpeditecriteria text,
    authoritynumb text,
    reportercountry text,
    reporterqualification text,
    sendertype text,
    senderorganization text,
    receivertype text,
    receiverorganization text,
    patientonsetage text,
    patientonsetageunit text,
    patientsex text,
    narrativeincludeclinical text
);

-- Child table: one row per drug in the report
create table if not exists fda_data.drug_event_drug (
    id serial primary key,
    safetyreportid text references fda_data.drug_event(safetyreportid) on delete cascade,
    drugcharacterization text,
    medicinalproduct text,
    drugbatchnumb text,
    drugstructuredosagenumb text,
    drugstructuredosageunit text,
    drugseparatedosagenumb text,
    drugintervaldosageunitnumb text,
    drugintervaldosagedefinition text,
    drugdosagetext text,
    drugadministrationroute text,
    activesubstancename text,
    application_number text,
    brand_name text,
    generic_name text,
    manufacturer_name text,
    product_ndc text,
    product_type text,
    route text,
    substance_name text,
    rxcui text,
    package_ndc text,
    nui text,
    pharm_class_epc text,
    pharm_class_moa text,
    unii text
);

-- Child table: one row per reaction in the report
create table if not exists fda_data.drug_event_reaction (
    id serial primary key,
    safetyreportid text references fda_data.drug_event(safetyreportid) on delete cascade,
    reactionmeddrapt text,
    reactionmeddraversionpt text
);