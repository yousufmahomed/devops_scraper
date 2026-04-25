import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# 1. Our expanded list of tech roles
tech_roles = [
    "Cybersecurity", 
    "Front End Developer", 
    "Back End Developer", 
    "Full Stack Engineer", 
    "AI Engineer", 
    "Automation",
    "Data Scientist"
]

# 2. A list of different "browsers" to trick Google into thinking we are human
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

def search_hiring_managers(query):
    print(f"Searching for {query} hiring managers...")
    search_url = f"https://www.google.com/search?q=site:linkedin.com/in/ + \"hiring\" + \"{query}\""
    
    headers = {
        "User-Agent": random.choice(user_agents) # Pick a random browser for each search
    }

    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print(f"  -> Google blocked the request. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for g in soup.find_all('div', class_='tF2Cxc'):
        name_title = g.find('h3').text if g.find('h3') else "No Name Found"
        link = g.find('a')['href'] if g.find('a') else "No Link Found"
        
        parts = name_title.split(' - ')
        name = parts[0]
        company = parts[-1].replace(' | LinkedIn', '') if len(parts) > 1 else "Unknown"

        results.append({
            "Search Term": query, # Added so you know which role they are hiring for
            "Name": name,
            "Company": company,
            "LinkedIn": link
        })

    return results

# --- Main Execution ---
all_managers = []

for role in tech_roles:
    managers = search_hiring_managers(role)
    if managers:
        all_managers.extend(managers)
        print(f"  -> Found {len(managers)} results for {role}!")
    else:
        print(f"  -> No results for {role} (or blocked).")
    
    # SUPER IMPORTANT: Wait 15 to 35 seconds between searches so we don't get banned again
    if role != tech_roles[-1]: # Don't wait after the very last search
        wait_time = random.randint(15, 35)
        print(f"Waiting {wait_time} seconds before the next search to look human...\n")
        time.sleep(wait_time)

# Save all results to CSV
if all_managers:
    print(f"\nFinished! Found {len(all_managers)} total contacts. Saving to file...")
    keys = all_managers[0].keys()
    
    with open('hiring_contacts.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(all_managers)
        
    print("Success! Open 'hiring_contacts.csv' to see the list.")
else:
    print("\nAll searches were blocked. Take a break for an hour, or try turning on a VPN to change your IP address.")