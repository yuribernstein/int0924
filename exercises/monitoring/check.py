import requests
import json
import time

# Measure start time
start_time = time.time()

results = []

# Load URLs and check each one sequentially
with open('120.domains.txt', 'r') as infile:
    for line in infile:
        url = line.strip()
        result = {'url': url, 'status_code': 'FAILED'}  # Default to FAILED
        try:
            response = requests.get(f'http://{url}', timeout=1)
            if response.status_code == 200:
                result['status_code'] = 'OK'
        except requests.exceptions.RequestException:
            result['status_code'] = 'FAILED'
        
        print(result)
        results.append(result)

# Write results to JSON file
with open('report.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)
print("Report generated in report.json")

# Measure end time
end_time = time.time()
elapsed_time = end_time - start_time

print(f"URL liveness check complete in {elapsed_time:.2f} seconds.")
