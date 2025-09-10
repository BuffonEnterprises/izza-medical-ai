#!/bin/bash

echo "🚀 Installing Claude GitHub App..."

# Check if gh CLI is authenticated
if ! gh auth status &>/dev/null; then
    echo "❌ GitHub CLI is not authenticated. Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is authenticated"

# Get the current user
GITHUB_USER=$(gh api user --jq .login)
echo "👤 GitHub User: $GITHUB_USER"

# Check if the app is already installed
echo "🔍 Checking if Claude GitHub App is already installed..."
INSTALLATIONS=$(gh api /user/installations 2>/dev/null || echo "{}")

if echo "$INSTALLATIONS" | jq -e '.installations[]? | select(.app_slug == "claude-for-github")' &>/dev/null; then
    echo "✅ Claude GitHub App is already installed!"
    INSTALLATION_ID=$(echo "$INSTALLATIONS" | jq -r '.installations[] | select(.app_slug == "claude-for-github") | .id')
    echo "📦 Installation ID: $INSTALLATION_ID"
else
    echo "📦 Claude GitHub App is not installed yet"
    echo ""
    echo "Please complete the installation manually:"
    echo "1. Opening Claude GitHub App installation page..."
    
    # Open the installation page
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "https://github.com/apps/claude-for-github/installations/new"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "https://github.com/apps/claude-for-github/installations/new"
    else
        echo "Please visit: https://github.com/apps/claude-for-github/installations/new"
    fi
    
    echo ""
    echo "2. Select repositories to grant access"
    echo "3. Click 'Install' button"
    echo "4. Complete the authorization"
    echo ""
    read -p "Press Enter after you've completed the installation..."
    
    # Verify installation
    echo "🔍 Verifying installation..."
    INSTALLATIONS=$(gh api /user/installations 2>/dev/null || echo "{}")
    
    if echo "$INSTALLATIONS" | jq -e '.installations[]? | select(.app_slug == "claude-for-github")' &>/dev/null; then
        echo "✅ Claude GitHub App successfully installed!"
        INSTALLATION_ID=$(echo "$INSTALLATIONS" | jq -r '.installations[] | select(.app_slug == "claude-for-github") | .id')
        echo "📦 Installation ID: $INSTALLATION_ID"
    else
        echo "❌ Installation not found. Please try again."
        exit 1
    fi
fi

# List repositories with access
echo ""
echo "📚 Repositories with Claude GitHub App access:"
gh api "/user/installations/$INSTALLATION_ID/repositories" --jq '.repositories[].full_name' 2>/dev/null || echo "Unable to fetch repository list"

echo ""
echo "✨ Claude GitHub App setup complete!"
echo ""
echo "You can now use Claude to:"
echo "  • Read and write code in your repositories"
echo "  • Create pull requests and issues"
echo "  • Manage GitHub Actions workflows"
echo "  • Access repository metadata"