#!/bin/bash

# NEXUS-MED ULTRA v5.0 Startup Script

echo "🏥 Starting NEXUS-MED ULTRA v5.0 - Advanced Medical Intelligence System"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Please create a .env file with your ANTHROPIC_API_KEY"
    echo "   Example: echo 'ANTHROPIC_API_KEY=your-key-here' > .env"
    echo ""
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt 2>/dev/null

# Find available port
PORT=8505
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    echo "Port $PORT is in use, trying next port..."
    PORT=$((PORT + 1))
done

echo ""
echo "✅ Starting application on port $PORT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Access the app at: http://localhost:$PORT"
echo ""
echo "Features:"
echo "  • 2x more content than original version"
echo "  • 15+ medical data models"
echo "  • 150+ medical conditions database"
echo "  • 50+ drug profiles"
echo "  • Clinical decision support"
echo "  • Medical analytics"
echo "  • Telemedicine support"
echo "  • Research assistant"
echo "  • PDF report generation"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run the application
streamlit run opushouse_ultra.py --server.port $PORT