import os
from bs4 import BeautifulSoup
from supabase import create_client, Client
from curl_cffi import requests as cffi_requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: Faltan las credenciales de Supabase en los secretos.")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Probamos con la URL base de resultados del grupo 24066
URL = "https://www.basquetcatala.cat/competicions/resultats/24066"

def run_scraper():
    print("🔍 Conectando con headers avanzados y cookies simuladas...")
    
    try:
        # Configuramos cabeceras que simulan una petición XHR (Ajax) real desde el navegador
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "ca,es;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.basquetcatala.cat/"
        }

        response = cffi_requests.get(URL, headers=headers, impersonate="chrome120", timeout=25)
        
        print(f"📥 Código de estado HTTP: {response.status_code}")
        
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find('title')
        title_text = title.text.strip() if title else 'No encontrado'
        print(f"🏷️ Título de la página: {title_text}")
        
        # Buscamos tablas o contenedores de partidos directamente
        tables = soup.find_all("table")
        print(f"📊 Tablas HTML encontradas: {len(tables)}")
        
        if len(tables) > 0:
            print("¡Éxito! Las tablas de partidos son accesibles directamente.")
            for i, table in enumerate(tables):
                rows = table.find_all("tr")
                print(f"   - Tabla {i+1}: {len(rows)} filas.")
        else:
            print("⚠️ No se detectan tablas en el HTML recibido. Es posible que los datos carguen por JavaScript dinámico.")

    except Exception as e:
        print(f"❌ Error durante la conexión: {e}")

if __name__ == "__main__":
    run_scraper()
