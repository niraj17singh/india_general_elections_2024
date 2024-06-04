# Create a streamlit app which takes in a place and searches database for it's value and shows the table to the user


import streamlit as st
import pandas as pd
import json
from utils import extract_party_table
import requests



def refresh_data():
    with open("../data/party_url.json", "r") as f:
        party_url_map = json.load(f)

    # # Read the HTML content from the file
    # with open('../data/bjp.html', 'r', encoding='utf-8') as file:
    #     html_content = file.read()
    final_df = pd.DataFrame()
    for party_name in party_url_map:
        # URL of the HTML pa"ge
        party_url = party_url_map[party_name]
        # Send a GET request to the URL
        response = requests.get(party_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Get the HTML content
            html_content = response.text
        else:
            print(f"Failed to retrieve HTML content. Status code: {response.status_code}")

        combined_df = extract_party_table(html_content)
        combined_df["Party Name"] = [party_name] * len(combined_df)
        final_df = pd.concat([final_df, combined_df], ignore_index=True)

    return final_df

# final_df = refresh_data()
# final_df.to_pickle("latest_data.pkl")

# Define the Streamlit app
def app():
    # Create a title for the app
    st.title('Constituency Result')
    # Create a text input for the user to enter a value
    user_input = st.text_input('Enter a constituency:')
    column_name = st.selectbox("Select the column", ["Parliamentary Constituency", "Party Name", "Leading Candidate"])
    if not column_name:
        column_name = "Parliamentary Constituency"
    refresh_data_button = st.button("Refresh Data")
    final_df = pd.read_pickle("latest_data.pkl")
    if refresh_data_button:
        final_df = refresh_data()
    final_df = final_df[["Parliamentary Constituency", "Party Name", "Margin", "% Margin", "Leading Candidate", "Total Votes"]]
    # If the user has entered a value, filter the DataFrame
    if user_input:
        filtered_data = final_df[final_df[column_name].str.contains(user_input, case=False)]
    else:
        filtered_data = final_df.copy()

    # Display the filtered DataFrame as a table
    st.write(filtered_data)

# Run the Streamlit app
if __name__ == '__main__':
    app()