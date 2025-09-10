#!/bin/bash

echo "======================================"
echo "GitHub MCP Configuration Verification"
echo "======================================"
echo ""

# Check if MCP config exists
if [ -f "/Users/leo/.config/claude-code/mcp.json" ]; then
    echo "✅ MCP configuration file found"
else
    echo "❌ MCP configuration file not found"
    exit 1
fi

# Check if GitHub MCP server is installed
if [ -f "/Users/leo/.nvm/versions/node/v18.20.8/bin/mcp-server-github" ]; then
    echo "✅ GitHub MCP server is installed"
else
    echo "❌ GitHub MCP server not installed"
    echo "   Run: npm install -g @modelcontextprotocol/server-github"
    exit 1
fi

# Check GitHub token
TOKEN=$(grep -o '"GITHUB_PERSONAL_ACCESS_TOKEN": "[^"]*"' /Users/leo/.config/claude-code/mcp.json | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ GitHub token not configured in MCP"
    exit 1
else
    echo "✅ GitHub token is configured"
fi

# Test GitHub API
echo ""
echo "Testing GitHub API connection..."
USER=$(curl -s -H "Authorization: token $TOKEN" https://api.github.com/user | jq -r '.login')

if [ "$USER" != "null" ] && [ -n "$USER" ]; then
    echo "✅ GitHub API connection successful"
    echo "   Authenticated as: $USER"
    
    # Get rate limit info
    RATE_LIMIT=$(curl -s -H "Authorization: token $TOKEN" https://api.github.com/rate_limit | jq -r '.rate.remaining')
    echo "   API Rate Limit Remaining: $RATE_LIMIT"
else
    echo "❌ GitHub API connection failed"
    echo "   Please check your token permissions"
    exit 1
fi

echo ""
echo "======================================"
echo "✅ GitHub MCP is properly configured!"
echo "======================================"
echo ""
echo "Your GitHub MCP integration is ready to use."
echo "The MCP server will be available when you restart Claude Code."