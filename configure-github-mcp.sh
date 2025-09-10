#!/bin/bash

echo "========================================="
echo "GitHub MCP Configuration"
echo "========================================="
echo ""
echo "Current GitHub account: BuffonEnterprises (leo@nefrologiabuffon.com)"
echo ""
echo "Please enter your GitHub Personal Access Token"
echo "(Get one at: https://github.com/settings/tokens)"
echo ""
read -sp "GitHub Token: " github_token
echo ""

if [ -z "$github_token" ]; then
    echo "Error: Token cannot be empty"
    exit 1
fi

# Update MCP configuration
CONFIG_FILE="$HOME/.config/claude-code/mcp.json"

if [ -f "$CONFIG_FILE" ]; then
    # Create backup
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
    
    # Update the GitHub token in the config
    jq --arg token "$github_token" '.mcpServers.github.env.GITHUB_PERSONAL_ACCESS_TOKEN = $token' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    
    echo "✓ GitHub Token configured successfully!"
    echo ""
    echo "Configuration saved to: $CONFIG_FILE"
    echo ""
    echo "To test the integration:"
    echo "1. Restart Claude Code"
    echo "2. The GitHub MCP server will be available automatically"
    echo ""
    echo "You can now use GitHub features in Claude Code!"
else
    echo "Error: Configuration file not found at $CONFIG_FILE"
    exit 1
fi