"""
Main entry point for App Engine with proper warmup handling
"""
import os
import sys
from flask import Flask, jsonify
import subprocess
import threading

app = Flask(__name__)

# Handle warmup requests
@app.route('/_ah/warmup')
def warmup():
    """Handle App Engine warmup requests"""
    return '', 200

@app.route('/_ah/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

# Start Streamlit in a separate thread
def start_streamlit():
    """Start Streamlit application"""
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "op.py",
        "--server.port=8081",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false"
    ])

# Start Streamlit when module loads
if os.environ.get('GAE_ENV', '').startswith('standard'):
    thread = threading.Thread(target=start_streamlit, daemon=True)
    thread.start()

if __name__ == '__main__':
    # This is used when running locally only
    app.run(host='0.0.0.0', port=8080, debug=True)