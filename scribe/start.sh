#!/bin/bash

echo "Starting Scribe web-server..."
fastapi dev src/api/app.py &
fastapi_pid=$!
echo "Scribe web-server started with the PID: $fastapi_pid"

echo "Starting ChromaDB..."
chroma run --port 8001 > /dev/null 2>&1 &
chroma_pid=$!
echo "ChromaDB started with the PID: $chroma_pid"

echo "Press CTRL+C to safely end the processes"

cleanup() {
	echo "CTRL+C pressed, killing the processes..."
	kill $fastapi_pid
	kill $chroma_pid
	echo "Processes killed. Good bye ;)"
}

trap cleanup SIGINT

wait
