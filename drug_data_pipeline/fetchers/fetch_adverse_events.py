import requests


def fetch_adverse_events(limit=5):
    """
    Fetch recent adverse drug event reports from OpenFDA.

    Args:
        limit (int): Number of records to fetch.

    Returns:
        list[dict]: List of adverse event records.
    """
    url = f"https://api.fda.gov/drug/event.json?limit={limit}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])

if __name__ == "__main__":
    events = fetch_adverse_events(limit=5)

    print("\n=== OpenFDA Adverse Event Reports ===\n")
    for i, result in enumerate(events, start=1):
        report_id = result.get("safetyreportid")
        received = result.get("receivedate")
        print(f"{i}. Report ID: {report_id} | Received: {received}")