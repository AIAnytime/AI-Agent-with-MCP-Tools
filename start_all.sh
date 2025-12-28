#!/bin/bash

echo "========================================"
echo "AI Agent with MCP & RBAC"
echo "========================================"
echo ""

trap 'kill $(jobs -p)' EXIT

echo "[1/3] Starting MCP HTTP Server on port 8765..."
source backend/.venv/bin/activate
python3 -m backend.mcp.mcp_server &
MCP_PID=$!
sleep 3

echo "[2/3] Starting API Server on port 8000..."
python3 -m backend.api.main &
API_PID=$!
sleep 3

echo "[3/3] Starting Frontend on port 3000..."
cd frontend
npm install --silent
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "All services started successfully!"
echo "========================================"
echo "MCP Server:  http://localhost:8765"
echo "API Server:  http://localhost:8000"
echo "Frontend:    http://localhost:3000"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

wait
