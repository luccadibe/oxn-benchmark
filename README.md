# "threshold" is the amount of miliseconds that the latency metric (avg, p90, p99) of the service is allowed to increase for the alert  to be triggered
# "window" is the amount of time that the latency has to be above the threshold for the alert to be triggered

# Detected
python3 benchmark.py reports/report_2024-12-02_21-07-55.yaml --prometheus-data prometheus_responses/prometheus_data_20241202-150813.json  --log-level INFO

# Not detected

python3 benchmark.py reports/report_2024-12-02_21-02-13.yaml --prometheus-data prometheus_responses/prometheus_data_20241202-150813.json  --log-level INFO
