import requests
import json

PROMETHEUS_URL = "http://34.66.104.228:80/api/v1/query"

def fetch_metric(query):
    response = requests.get(PROMETHEUS_URL, params={'query': query})
    if response.status_code == 200:
        result = response.json()
        return result['data']['result']
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

cpu_query = 'rate(node_cpu_seconds_total[5m])'
memory_total_query = 'node_memory_MemTotal_bytes'
memory_available_query = 'node_memory_MemAvailable_bytes'

print("CPU Metrics: ")
cpu_metrics = fetch_metric(cpu_query)
if cpu_metrics:
   for metric in cpu_metrics:
      print("\nMetric Information:")
      print(json.dumps(metric['metric'],indent=4))
      print("values:")
      print(f"  Timestamp: {metric['value'][0]}")
      print(f"  CPU Usage: {metric['value'][1]}")
else:
    print("No CPU metrics data retrieved.")

print("\nMemory Metrics")
memory_total = fetch_metric(memory_total_query)
memory_available = fetch_metric(memory_available_query)

if memory_total and memory_available:
    for total, available in zip(memory_total, memory_available):
        print("\nNode:", total['metric']['node'])
        print("Memory Total:", total['value'][1])
        print("Memory Available:", available['value'][1])
        used_memory = float(total['value'][1]) - float(available['value'][1])
        print("Memory Used:", used_memory)
else:
    print("No memory metrics data retrieved.")


