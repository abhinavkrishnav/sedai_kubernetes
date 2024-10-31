import requests
import datetime

PROMETHEUS_URL = "http://34.66.104.228:80/api/v1/query"  # Replace with actual host

# Example function to fetch CPU usage of nodes
def fetch_metric(query):
    response = requests.get(PROMETHEUS_URL, params={'query': query})
    if response.status_code == 200:
        result = response.json()
        return result['data']['result']
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Define your PromQL query
cpu_query = 'rate(node_cpu_seconds_total[5m])'

# Collect data
metrics = fetch_metric(cpu_query)
for metric in metrics:
    print(f"Metric: {metric['metric']}")
    print(f"Values: {metric['value']}")

