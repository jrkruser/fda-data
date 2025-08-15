import requests

def fetch_recalls(limit=5):
    """
    Fetch recent drug recall (enforcement) reports from OpenFDA.
    """
    url = f"https://api.fda.gov/drug/enforcement.json?limit={limit}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])

if __name__ == "__main__":
    recalls = fetch_recalls(limit=5)
    print("\n=== OpenFDA Drug Recalls ===\n")
    for i, recall in enumerate(recalls, start=1):
        product = recall.get("product_description")
        reason = recall.get("reason_for_recall")
        recall_date = recall.get("recall_initiation_date")
        print(f"{i}. Product: {product}\n   Reason: {reason}\n   Initiated: {recall_date}\n")
