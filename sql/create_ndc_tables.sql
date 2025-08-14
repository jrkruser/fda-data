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