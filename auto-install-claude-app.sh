#!/bin/bash

echo "🚀 Automated Claude GitHub App Installation"
echo "==========================================="

# Check gh CLI authentication
if ! gh auth status &>/dev/null; then
    echo "❌ GitHub CLI not authenticated. Authenticating now..."
    gh auth login --web
fi

echo "✅ GitHub CLI authenticated"

# Get current user info
USER=$(gh api user --jq .login)
echo "👤 User: $USER"

# Function to wait for app installation
wait_for_installation() {
    echo "⏳ Waiting for Claude GitHub App installation..."
    echo ""
    echo "📌 IMPORTANT: A browser window will open. Please:"
    echo "   1. Select the repositories you want Claude to access"
    echo "   2. Click the green 'Install' button"
    echo "   3. Complete any authorization prompts"
    echo ""
    
    # Open installation URL
    URL="https://github.com/apps/claude-for-github/installations/new"
    echo "🌐 Opening: $URL"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$URL"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "$URL"
    else
        echo "Please manually visit: $URL"
    fi
    
    # Poll for installation
    echo ""
    echo "⏳ Checking for installation (this will check every 5 seconds)..."
    
    for i in {1..60}; do
        sleep 5
        
        # Check if app is installed
        if gh api /user/installations 2>/dev/null | jq -e '.installations[]? | select(.app_slug == "claude-for-github")' &>/dev/null; then
            echo ""
            echo "✅ Claude GitHub App detected!"
            return 0
        fi
        
        # Show progress
        echo -n "."
    done
    
    echo ""
    echo "❌ Timeout waiting for installation"
    return 1
}

# Check if already installed
echo "🔍 Checking existing installations..."
if gh api /user/installations 2>/dev/null | jq -e '.installations[]? | select(.app_slug == "claude-for-github")' &>/dev/null; then
    echo "✅ Claude GitHub App is already installed!"
    INSTALLATION_ID=$(gh api /user/installations | jq -r '.installations[] | select(.app_slug == "claude-for-github") | .id')
else
    # Trigger installation
    if wait_for_installation; then
        INSTALLATION_ID=$(gh api /user/installations | jq -r '.installations[] | select(.app_slug == "claude-for-github") | .id')
    else
        echo "❌ Installation failed or timed out"
        echo "Please try running this script again or install manually at:"
        echo "https://github.com/apps/claude-for-github"
        exit 1
    fi
fi

echo ""
echo "📦 Installation ID: $INSTALLATION_ID"

# Get installation details
echo ""
echo "📊 Installation Details:"
echo "------------------------"

# Get repository access
echo ""
echo "📚 Repositories with access:"
gh api "/user/installations/$INSTALLATION_ID/repositories" 2>/dev/null | jq -r '.repositories[].full_name' | while read repo; do
    echo "   • $repo"
done

# Get permissions
echo ""
echo "🔐 App Permissions:"
gh api "/app/installations/$INSTALLATION_ID" 2>/dev/null | jq -r '.permissions | to_entries[] | "   • \(.key): \(.value)"' || echo "   (Unable to fetch permissions)"

echo ""
echo "✨ Claude GitHub App is ready to use!"
echo ""
echo "🎯 You can now:"
echo "   • Use Claude to read and write code in your repositories"
echo "   • Create pull requests and issues with Claude"
echo "   • Manage GitHub Actions workflows"
echo "   • Access repository metadata and more"
echo ""
echo "🔧 To manage the app, visit:"
echo "   https://github.com/settings/installations"