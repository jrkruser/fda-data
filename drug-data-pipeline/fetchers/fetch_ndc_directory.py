import requests

def fetch_ndc_directory(limit=5):
    """
    Fetch drug listing (NDC directory) data from OpenFDA.
    """
    url = f"https://api.fda.gov/drug/ndc.json?limit={limit}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])

if __name__ == "__main__":
    ndcs = fetch_ndc_directory(limit=5)
    print("\n=== OpenFDA NDC Directory ===\n")
    for i, ndc in enumerate(ndcs, start=1):
        product_ndc = ndc.get("product_ndc")
        brand_name = ndc.get("brand_name")
        generic_name = ndc.get("generic_name")
        print(f"{i}. NDC: {product_ndc}\n   Brand: {brand_name}\n   Generic: {generic_name}\n")
