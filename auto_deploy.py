import webbrowser
import time

# URLs de deploy
urls = [
    "https://share.streamlit.io/deploy?repository=BuffonEnterprises/izza-medical-ai&branch=main&mainModule=op.py",
    "https://dashboard.render.com/select-repo?type=web",
    "http://localhost:8080"
]

print("🚀 Abrindo páginas de deploy...")
for url in urls:
    webbrowser.open(url)
    time.sleep(2)

print("✅ Páginas abertas! Complete o deploy clicando nos botões.")
