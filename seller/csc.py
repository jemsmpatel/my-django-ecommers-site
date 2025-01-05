# csc.py

import requests

def get_countries():
    response = requests.get("https://restcountries.com/v3.1/all")
    countries = response.json()
    return [{'id': country['cca2'], 'name': country['name']['common']} for country in countries]

def get_states(country_id):
    # Placeholder states for demonstration purposes
    if country_id == 'US':
        return [{'id': 'CA', 'name': 'California'}, {'id': 'NY', 'name': 'New York'}]
    elif country_id == 'IN':
        return [{'id': 'MH', 'name': 'Maharashtra'}, {'id': 'DL', 'name': 'Delhi'}]
    return []

def get_cities(state_id):
    # Placeholder cities for demonstration purposes
    if state_id == 'CA':
        return [{'id': 'LA', 'name': 'Los Angeles'}, {'id': 'SF', 'name': 'San Francisco'}]
    elif state_id == 'NY':
        return [{'id': 'NYC', 'name': 'New York City'}, {'id': 'BUF', 'name': 'Buffalo'}]
    elif state_id == 'MH':
        return [{'id': 'MUM', 'name': 'Mumbai'}, {'id': 'PUN', 'name': 'Pune'}]
    elif state_id == 'DL':
        return [{'id': 'NDL', 'name': 'New Delhi'}, {'id': 'OLD', 'name': 'Old Delhi'}]
    return []
