#!/bin/bash

echo "Starting fake ChromaDB..."
chroma run --path ./chroma_fake --port 8001 > /dev/null 2>&1 &
chroma_pid=$!
echo "Fake ChromaDB started with the PID: $chroma_pid"

echo "Running tests..."
pytest tests/e2e -v
echo "Tests completed"

echo "Stopping fake ChromaDB..."
kill $chroma_pid
echo "Fake ChromaDB stopped"

echo "Deleting fake ChromaDB..."
rm -rf ./chroma_fake
echo "Fake ChromaDB deleted"