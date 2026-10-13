import os
import cloudscraper
from bs4 import BeautifulSoup
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: Faltan las credenciales de Supabase en los secretos.")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

URL = "https://www.basquetcatala.cat/competicions/resultats/24066"

def run_scraper():
    print("🔍 Conectando a la web de Bàsquet Català superando el reto de Cloudflare...")
    
    try:
        # Inicializamos cloudscraper para resolver el reto JS automáticamente
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        response = scraper.get(URL, timeout=25)
        
        print(f"📥 Código de estado HTTP: {response.status_code}")
        
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find('title')
        title_text = title.text.strip() if title else 'No encontrado'
        print(f"🏷️ Título real de la página: {title_text}")
        
        if "Verificació" not in title_text:
            # Buscamos las filas de partidos en la página de resultados
            rows = soup.find_all("tr")
            matches_found = 0
            
            for row in rows:
                text = row.get_text(separator=" ", strip=True)
                if "-" in text or "VS" in text.upper():
                    matches_found += 1
            
            print(f"📊 Filas de partidos detectadas: {matches_found}")
            print("🚀 ¡Acceso concedido y datos listos para sincronizar con Supabase!")
        else:
            print("⚠️ Cloudflare sigue reteniendo la página. Revisando cookies...")

    except Exception as e:
        print(f"❌ Error durante la conexión: {e}")

if __name__ == "__main__":
    run_scraper()
