import requests

def fetch_drug_shortages(limit=5):
    url = f"https://api.fda.gov/drug/shortages.json?limit={limit}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])

if __name__ == "__main__":
    print("\n=== OpenFDA Drug Shortages ===\n")
    shortages = fetch_drug_shortages(limit=5)
    for idx, shortage in enumerate(shortages, 1):
        product = shortage.get("generic_name", "Unknown")
        start_date = shortage.get("shortage_start_date", "Unknown")
        print(f"{idx}. {product} | Shortage Start: {start_date}")
