import requests
from bs4 import BeautifulSoup
import csv
import time
import random

def search_hiring_managers(query):
    print(f"Searching for {query} hiring managers...")
    
    # Google Search URL with a 'site:linkedin.com' filter
    search_url = f"https://www.google.com/search?q=site:linkedin.com/in/ + \"hiring\" + \"{query}\""
    
    # This header makes our script look like a normal web browser to Google
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print("Google blocked the request. Try again later or use a VPN/Proxy.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    # Find the search result blocks
    for g in soup.find_all('div', class_='tF2Cxc'):
        name_title = g.find('h3').text if g.find('h3') else "No Name Found"
        link = g.find('a')['href'] if g.find('a') else "No Link Found"
        
        # Simple parsing to separate name from company if possible
        parts = name_title.split(' - ')
        name = parts[0]
        company = parts[-1].replace(' | LinkedIn', '') if len(parts) > 1 else "Unknown"

        results.append({
            "Name": name,
            "Company": company,
            "LinkedIn": link
        })

    return results

# --- Main Execution ---
# You can change "DevOps" to "Platform Engineering" or "SRE" later if you want
role = "DevOps" 

# Add a slight delay to be safe
time.sleep(random.randint(2, 5)) 

managers = search_hiring_managers(role)

# Save the results to a CSV file
if managers:
    print(f"Found {len(managers)} results! Saving to file...")
    keys = managers[0].keys()
    
    with open('hiring_contacts.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(managers)
        
    print("Success! Open 'hiring_contacts.csv' in your folder to see the list.")
else:
    print("No results found or the search was blocked.")