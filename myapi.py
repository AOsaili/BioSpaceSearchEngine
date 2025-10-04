import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. Load the original file
file_path = "SB_publication_PMC.csv"
df = pd.read_csv(file_path)

# 2. Function to fetch data from PubMed Central API
def fetch_pmc_data(pmc_url):
    try:
        # Extract PMCID from the link
        pmcid = pmc_url.strip("/").split("/")[-1]

        # Call NCBI E-utilities API
        api_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            "db": "pmc",
            "id": pmcid,
            "retmode": "xml"
        }
        resp = requests.get(api_url, params=params)
        resp.raise_for_status()

        # Parse XML
        soup = BeautifulSoup(resp.text, "xml")

        title = soup.find("article-title")
        abstract = soup.find("abstract")
        pub_date = soup.find("pub-date")
        authors = [a.get_text(" ", strip=True) for a in soup.find_all("contrib", attrs={"contrib-type": "author"})]

        return {
            "Title": title.get_text(strip=True) if title else None,
            "Abstract": abstract.get_text(" ", strip=True) if abstract else None,
            "Authors": "; ".join(authors) if authors else None,
            "Date": "-".join([pub_date.find(tag).text for tag in ["year", "month", "day"] if pub_date and pub_date.find(tag)]) if pub_date else None,
            "Link": pmc_url
        }
    except Exception as e:
        return {
            "Title": None,
            "Abstract": None,
            "Authors": None,
            "Date": None,
            "Link": pmc_url,
            "Error": str(e)
        }

# 3. Apply function to all links
results = []
for link in df["Link"]:
    print(f"Fetching {link} ...")
    results.append(fetch_pmc_data(link))

# 4. Save results in a new DataFrame
out_df = pd.DataFrame(results)

# 5. Export to CSV
out_df.to_csv("PMC_enriched.csv", index=False)

print("✅ Done! File saved as PMC_enriched.csv")
print(out_df.head())
