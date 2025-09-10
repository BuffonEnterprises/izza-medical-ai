#!/bin/bash

echo "========================================="
echo "Configuração de Chaves API para MCP"
echo "========================================="
echo ""
echo "Para usar completamente os servidores MCP, você precisa configurar as seguintes chaves:"
echo ""
echo "1. GITHUB PERSONAL ACCESS TOKEN"
echo "   - Acesse: https://github.com/settings/tokens"
echo "   - Clique em 'Generate new token (classic)'"
echo "   - Selecione os scopes necessários (repo, user, etc.)"
echo "   - Copie o token gerado"
echo ""
echo "2. BRAVE SEARCH API KEY"
echo "   - Acesse: https://api.search.brave.com/app/keys"
echo "   - Crie uma conta gratuita"
echo "   - Gere uma chave API"
echo ""

read -p "Você tem um GitHub Personal Access Token? (s/n): " has_github
if [ "$has_github" = "s" ]; then
    read -sp "Cole seu GitHub Token aqui: " github_token
    echo ""
    sed -i.bak "s|\"GITHUB_PERSONAL_ACCESS_TOKEN\": \"\"|\"GITHUB_PERSONAL_ACCESS_TOKEN\": \"$github_token\"|" ~/.config/claude-code/mcp.json
    echo "✓ GitHub Token configurado!"
fi

read -p "Você tem uma Brave Search API Key? (s/n): " has_brave
if [ "$has_brave" = "s" ]; then
    read -sp "Cole sua Brave API Key aqui: " brave_key
    echo ""
    sed -i.bak "s|\"BRAVE_API_KEY\": \"\"|\"BRAVE_API_KEY\": \"$brave_key\"|" ~/.config/claude-code/mcp.json
    echo "✓ Brave API Key configurada!"
fi

echo ""
echo "========================================="
echo "Configuração concluída!"
echo "========================================="
echo ""
echo "Servidores MCP instalados e configurados:"
echo "✓ GitHub - Integração com repositórios GitHub"
echo "✓ FileSystem - Acesso a arquivos locais"
echo "✓ Memory - Armazenamento temporário de dados"
echo "✓ Puppeteer - Automação de navegador"
echo "✓ Brave Search - Pesquisas na web"
echo ""
echo "Para usar os servidores MCP no Claude Code:"
echo "1. Reinicie o Claude Code"
echo "2. Use o comando: /mcp"
echo "3. Os servidores estarão disponíveis automaticamente"
echo ""