import os
import time
from prometheus_client import start_http_server, Gauge
import re
import logging

total_requests = Gauge("total_requests", f"This shows the number of total requests to the API")
port = int(os.environ.get("EXPORTER_PORT", 9876))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def count_POST_request(word, filename):
    with open(filename, 'r') as file:
        text = file.read()
        word_count = len(re.findall(word, text))
    return word_count

# Use a regex pattern to match POST requests
post_pattern = r'\bPOST\b'
log_file = '/root/flask.log'

count_POST_request(post_pattern, log_file)

def httpstarter(port):
    start_http_server(port)

def set_value_totalrequests(metric):
    count = metric.set(count_POST_request(post_pattern, log_file))
    return count

if __name__ == "__main__":
    httpstarter(port)
    while True:
        set_value_totalrequests(total_requests)
        time.sleep(5)
