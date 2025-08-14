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