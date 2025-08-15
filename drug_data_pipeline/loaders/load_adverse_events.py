import json
import sys
import os
from drug_data_pipeline.utils.db import get_connection, parse_date


def load_adverse_events(input_file: str):
    input_file = os.path.abspath(input_file)

    conn = get_connection()
    cur = conn.cursor()

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    reports = data.get("results", [])

    for r in reports:
        safetyreportid = r.get("safetyreportid")

        cur.execute("""
            INSERT INTO fda_data.drug_event (
                safetyreportid, safetyreportversion, primarysourcecountry,
                transmissiondate, reporttype, serious,
                seriousnessdeath, seriousnesslifethreatening, seriousnesshospitalization,
                seriousnessdisabling, seriousnesscongenitalanomali, seriousnessother,
                receivedate, receiptdate, fulfillexpeditecriteria, authoritynumb,
                reportercountry, reporterqualification, sendertype, senderorganization,
                receivertype, receiverorganization, patientonsetage, patientonsetageunit,
                patientsex, narrativeincludeclinical
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (safetyreportid) DO NOTHING
        """, (
            safetyreportid,
            r.get("safetyreportversion"),
            r.get("primarysourcecountry"),
            parse_date(r.get("transmissiondate")),
            r.get("reporttype"),
            r.get("serious"),
            r.get("seriousnessdeath"),
            r.get("seriousnesslifethreatening"),
            r.get("seriousnesshospitalization"),
            r.get("seriousnessdisabling"),
            r.get("seriousnesscongenitalanomali"),
            r.get("seriousnessother"),
            parse_date(r.get("receivedate")),
            parse_date(r.get("receiptdate")),
            r.get("fulfillexpeditecriteria"),
            r.get("authoritynumb"),
            r.get("primarysource", {}).get("reportercountry"),
            r.get("primarysource", {}).get("qualification"),
            r.get("sender", {}).get("sendertype"),
            r.get("sender", {}).get("senderorganization"),
            r.get("receiver", {}).get("receivertype"),
            r.get("receiver", {}).get("receiverorganization"),
            r.get("patient", {}).get("patientonsetage"),
            r.get("patient", {}).get("patientonsetageunit"),
            r.get("patient", {}).get("patientsex"),
            r.get("patient", {}).get("summary", {}).get("narrativeincludeclinical")
        ))

        for reaction in r.get("patient", {}).get("reaction", []):
            cur.execute("""
                INSERT INTO fda_data.drug_event_reaction (
                    safetyreportid, reactionmeddrapt, reactionmeddraversionpt
                )
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                safetyreportid,
                reaction.get("reactionmeddrapt"),
                reaction.get("reactionmeddraversionpt")
            ))

        for drug in r.get("patient", {}).get("drug", []):
            openfda = drug.get("openfda", {})
            cur.execute("""
                INSERT INTO fda_data.drug_event_drug (
                    safetyreportid, drugcharacterization, medicinalproduct,
                    drugbatchnumb, drugstructuredosagenumb, drugstructuredosageunit,
                    drugseparatedosagenumb, drugintervaldosageunitnumb, drugintervaldosagedefinition,
                    drugdosagetext, drugadministrationroute, activesubstancename,
                    application_number, brand_name, generic_name, manufacturer_name,
                    product_ndc, product_type, route, substance_name, rxcui, package_ndc,
                    nui, pharm_class_epc, pharm_class_moa, unii
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                safetyreportid,
                drug.get("drugcharacterization"),
                drug.get("medicinalproduct"),
                drug.get("drugbatchnumb"),
                drug.get("drugstructuredosagenumb"),
                drug.get("drugstructuredosageunit"),
                drug.get("drugseparatedosagenumb"),
                drug.get("drugintervaldosageunitnumb"),
                drug.get("drugintervaldosagedefinition"),
                drug.get("drugdosagetext"),
                drug.get("drugadministrationroute"),
                drug.get("activesubstance", {}).get("activesubstancename"),
                ", ".join(openfda.get("application_number", [])),
                ", ".join(openfda.get("brand_name", [])),
                ", ".join(openfda.get("generic_name", [])),
                ", ".join(openfda.get("manufacturer_name", [])),
                ", ".join(openfda.get("product_ndc", [])),
                ", ".join(openfda.get("product_type", [])),
                ", ".join(openfda.get("route", [])),
                ", ".join(openfda.get("substance_name", [])),
                ", ".join(openfda.get("rxcui", [])),
                ", ".join(openfda.get("package_ndc", [])),
                ", ".join(openfda.get("nui", [])),
                ", ".join(openfda.get("pharm_class_epc", [])),
                ", ".join(openfda.get("pharm_class_moa", [])),
                ", ".join(openfda.get("unii", []))
            ))

    conn.commit()
    cur.close()
    conn.close()

    print(f"Loaded {len(reports)} safety reports successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python -m drug_data_pipeline.loaders.load_adverse_events <path_to_json>")
        sys.exit(1)
    load_adverse_events(sys.argv[1])
