#!/bin/bash
# this file is a script working only on the developer's pc 

echo "Starting the Prometheus..."
/home/oleksii/prometheus/prometheus --config.file=/home/oleksii/prometheus/configs/scribe.yml --storage.tsdb.path=/home/oleksii/prometheus/data > /dev/null  2>&1 &
prom_pid=$!
echo "Prometheus started"

echo "Starting the Grafana..."
/bin/systemctl start grafana-server
echo "Grafana started"

cleanup() {
	echo "CTRL+C pressed, killing the processes..."
	kill $prom_pid
	systemctl stop grafana-server
	echo "Processes killed. Good bye ;)"
}

trap cleanup SIGINT

wait
