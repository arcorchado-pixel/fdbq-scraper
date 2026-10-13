import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: Faltan las credenciales de Supabase en los secretos.")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

URL = "https://www.basquetcatala.cat/competicions/resultats/24066"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,ca;q=0.8,en;q=0.7",
    "Referer": "https://www.basquetcatala.cat/",
}

def run_scraper():
    print("🔍 Conectando a la web de Bàsquet Català...")
    
    try:
        session = requests.Session()
        response = session.get(URL, headers=HEADERS, timeout=15)
        
        print(f"📥 Código de estado HTTP: {response.status_code}")
        print(f"📏 Longitud del texto recibido: {len(response.text)} caracteres")
        
        if response.status_code == 200 and len(response.text) > 500:
            soup = BeautifulSoup(response.text, "html.parser")
            # Vamos a buscar cualquier texto visible o título en la página
            title = soup.find('title')
            print(f"🏷️ Título de la página: {title.text if title else 'No encontrado'}")
            
            # Buscar elementos generales
            all_tags = len(soup.find_all(True))
            print(f"📊 Total de etiquetas HTML encontradas: {all_tags}")
        else:
            print("⚠️ La página ha respondido con contenido muy corto o bloqueado.")
            print(response.text[:300]) # Mostrar los primeros 300 caracteres para diagnosticar

    except Exception as e:
        print(f"❌ Error durante la conexión: {e}")

if __name__ == "__main__":
    run_scraper()
