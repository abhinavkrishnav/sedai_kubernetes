#http://34.66.104.228:80/api/v1/query
import requests
import numpy as np

PROMETHEUS_URL = "http://34.66.104.228:80/api/v1/query"  # Replace with actual host

# Function to fetch metrics for a query
def fetch_metric(query):
    response = requests.get(PROMETHEUS_URL, params={'query': query, 'start': '<start_time>', 'end': '<end_time>', 'step': '5m'})
    if response.status_code == 200:
        result = response.json()
        return result['data']['result']
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

# CPU and Memory PromQL Queries
cpu_query = 'rate(node_cpu_seconds_total[5m])'
memory_query = 'node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes'

# Fetch and process CPU usage metrics
cpu_metrics = fetch_metric(cpu_query)
print("CPU Usage (in cores) per node:")
for metric in cpu_metrics:
    if 'values' in metric:  # Check if 'values' key exists
        cpu_values = [float(value[1]) for value in metric['values']]
        node_name = metric['metric'].get('node', 'Unknown Node')
        print(f"Node: {node_name}")
        print(f"  Average: {np.mean(cpu_values):.2f}")
        print(f"  Max: {np.max(cpu_values):.2f}")
        print(f"  P99: {np.percentile(cpu_values, 99):.2f}")
    else:
        print(f"Metric data for node {metric['metric'].get('node', 'Unknown Node')} does not contain 'values' key.")

# Fetch and process Memory usage metrics
memory_metrics = fetch_metric(memory_query)
print("\nMemory Usage (in bytes) per node:")
for metric in memory_metrics:
    if 'values' in metric:  # Check if 'values' key exists
        memory_values = [float(value[1]) for value in metric['values']]
        node_name = metric['metric'].get('node', 'Unknown Node')
        print(f"Node: {node_name}")
        print(f"  Average: {np.mean(memory_values):.2f}")
        print(f"  Max: {np.max(memory_values):.2f}")
        print(f"  P99: {np.percentile(memory_values, 99):.2f}")
    else:
        print(f"Metric data for node {metric['metric'].get('node', 'Unknown Node')} does not contain 'values' key.")
