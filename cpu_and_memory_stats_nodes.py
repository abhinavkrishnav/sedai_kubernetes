import requests
import numpy as np

PROMETHEUS_URL = "http://34.66.104.228:80/api/v1/query"  # Replace with actual host

# Fetch data from Prometheus
def fetch_metric(query):
    response = requests.get(PROMETHEUS_URL, params={'query': query})
    if response.status_code == 200:
        result = response.json()
        return [float(metric['value'][1]) for metric in result['data']['result']]
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

# Helper function to calculate statistics
def calculate_stats(data):
    if data:
        avg = np.mean(data)
        max_val = np.max(data)
        p99 = np.percentile(data, 99)
        return avg, max_val, p99
    return None, None, None

# Define PromQL queries for CPU and memory metrics
cpu_query = 'rate(node_cpu_seconds_total[5m])'  # Adjust interval as needed
memory_query = 'node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes'

# Fetch CPU and memory data
cpu_data = fetch_metric(cpu_query)
memory_data = fetch_metric(memory_query)

# Calculate and display statistics
cpu_avg, cpu_max, cpu_p99 = calculate_stats(cpu_data)
memory_avg, memory_max, memory_p99 = calculate_stats(memory_data)

print("CPU Usage (in cores):")
print(f"  Average: {cpu_avg}")
print(f"  Max: {cpu_max}")
print(f"  P99: {cpu_p99}")

print("\nMemory Usage (in bytes):")
print(f"  Average: {memory_avg}")
print(f"  Max: {memory_max}")
print(f"  P99: {memory_p99}")
