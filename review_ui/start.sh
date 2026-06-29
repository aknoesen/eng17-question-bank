#!/usr/bin/env bash
# Start the VeriQAI Review UI (Mac/Linux)
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Install backend deps (fastapi, uvicorn, python-dotenv)
echo "Installing backend dependencies..."
python3 -m pip install -r "$SCRIPT_DIR/backend/requirements.txt"

# Install frontend deps if needed
if [ ! -d "$SCRIPT_DIR/frontend/node_modules" ]; then
  echo "Installing frontend dependencies..."
  (cd "$SCRIPT_DIR/frontend" && npm install)
fi

# Start backend
echo "Starting backend on http://localhost:8000 ..."
(cd "$SCRIPT_DIR/backend" && uvicorn main:app --reload --port 8000) &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend on http://localhost:5173 ..."
sleep 1
(cd "$SCRIPT_DIR/frontend" && npm run dev) &
FRONTEND_PID=$!

# Open browser (Mac)
sleep 3
open http://localhost:5173 2>/dev/null || xdg-open http://localhost:5173 2>/dev/null || true

echo ""
echo "Review UI running. Press Ctrl+C to stop both servers."
wait $BACKEND_PID $FRONTEND_PID
