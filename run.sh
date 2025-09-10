#!/bin/bash

# Exit on error
set -e

# Set port from environment variable
PORT=${PORT:-8080}

echo "Starting Streamlit on port $PORT..."

# Create .streamlit directory if it doesn't exist
mkdir -p ~/.streamlit

# Create config file with proper port
cat > ~/.streamlit/config.toml << EOF
[server]
port = $PORT
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
EOF

# Start Streamlit
exec streamlit run op.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false