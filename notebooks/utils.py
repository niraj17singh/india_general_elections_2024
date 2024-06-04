from bs4 import BeautifulSoup
import pandas as pd

def extract_party_table(html_content: str):
    # Assuming you have the HTML content in a string variable `html_content`
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <table> elements
    tables = soup.find_all('table')

    # Extract data from each table
    dfs = []
    for table in tables:
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            row_data = [col.text.strip() for col in cols]
            data.append(row_data)
        df = pd.DataFrame(data)
        dfs.append(df)

    # Combine all DataFrames into one
    combined_df = pd.concat(dfs, ignore_index=True)
    columns = ["S.No", "Parliamentary Constituency", "Leading Candidate", "Total Votes", "Margin"]
    combined_df.columns = columns
    combined_df = combined_df[combined_df["S.No"].notna()]
    combined_df["S.No"] = combined_df["S.No"].astype(int)
    combined_df["Margin"] = combined_df["Margin"].astype(int)
    combined_df["Total Votes"] = combined_df["Total Votes"].astype(int)
    combined_df["% Margin"] = combined_df["Margin"] / combined_df["Total Votes"] * 100
    return combined_df