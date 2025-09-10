#!/usr/bin/env python3
import re

# Read the file
with open('op.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define emoji replacements
replacements = {
    '🧠': '',
    '🔬': '',
    '🎯': '##',
    '🚨': '##',
    '📊': '##', 
    '🔄': '##',
    '🏥': '',
    '📎': '[ANEXO]',
    '🔢': '',
    '🗑️': 'Excluir',
    '💾': 'Salvar',
    '📒': '',
    '📄': 'Ver',
    '➕': '+',
    '🖼️': '[IMG]',
    '🇧🇷': '[PT-BR]',
    '🇺🇸': '[EN]',
    '🇪🇸': '[ES]',
    '🇫🇷': '[FR]',
    '🇩🇪': '[DE]',
    '🇮🇹': '[IT]',
    '⏱️': '',
    '🤖': '',
    '⏳': '',
    '❓': '',
    '📤': '',
}

# Replace emojis
for emoji, replacement in replacements.items():
    content = content.replace(emoji, replacement)

# Remove any remaining emojis using regex
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002500-\U00002BEF"  # chinese char
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"  # dingbats
    "\u3030"
    "]+", flags=re.UNICODE
)

content = emoji_pattern.sub('', content)

# Write the cleaned content
with open('op.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("All emojis removed successfully!")