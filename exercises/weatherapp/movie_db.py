# import argparse
import requests
import json
import os
import argparse

search_file = 'search.json'

# Parse arguments
# parser = argparse.ArgumentParser(description="Get movie information")
# parser.add_argument("-s", "--search", type=str, required=True, help="The movie to search for")
# search = parser.parse_args().search

# Initialize JSON file if it does not exist
if not os.path.exists(search_file):
    with open(search_file, "w") as f:
        json.dump({}, f)

def save_locally(search_file, search, data):
    """Save search result data locally."""
    with open(search_file, "r") as f:
        local_data = json.load(f)

    # Update with new search data
    local_data[search] = data

    with open(search_file, "w") as f:
        json.dump(local_data, f)

def load_locally(pattern):
    """Load search result data locally."""
    with open(search_file, "r") as f:
        return json.load(f).get(pattern)

def exists_locally(search):
    """Check if the search result exists locally."""
    with open(search_file, "r") as f:
        local_data = json.load(f)
        return search in local_data

def movie_search(pattern):
    """Search for movie data, retrieving from local storage if available."""
    # Check if data exists locally
    if exists_locally(pattern):
        return load_locally(pattern)
    
    # Fetch data from API if not found locally
    url = "https://movie-database-alternative.p.rapidapi.com/"
    querystring = {"s": pattern, "r": "json", "page": "1"}

    headers = {
        "x-rapidapi-key": "f4fee9ade6mshb21cb650647e763p1d4eb0jsn7a2b2ea6a7d9",
        "x-rapidapi-host": "movie-database-alternative.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        api_resp = response.json()
        
        if 'Search' not in api_resp:
            return {"Error": "No results found in API response."}
        
        # Process and format API response
        result = {movie['Title']: movie['Year'] for movie in api_resp['Search']}
        
        # Save API result locally
        save_locally(search_file, pattern, result)
        return result
    
    except requests.exceptions.RequestException as e:
        return {"Error": f"API request failed: {str(e)}"}
