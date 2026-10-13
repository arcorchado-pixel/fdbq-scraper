import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client

# Configuración de Supabase desde los Secretos de GitHub
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: Faltan las credenciales de Supabase en los secretos.")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# URL del grupo Mini Interterritorial FCBQ (Código: 24066)
URL = "https://www.basquetcatala.cat/competicions/resultats/24066"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ca-ES,ca;q=0.9,es-ES;q=0.8",
}

def run_scraper():
    print("🔍 Conectando a la web de Bàsquet Català...")
    
    session = requests.Session()
    
    try:
        response = session.get(URL, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Error al acceder a la página: Status {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Buscar todos los enlaces, div y tablas para detectar la estructura de partidos
        links = soup.find_all("a")
        partits_links = [a['href'] for a in links if a.has_attr('href') and ('partit' in a['href'] or 'acta' in a['href'])]
        
        containers = soup.select("div[class*='partit'], div[class*='match'], .row, table")
        
        print(f"📊 Enlaces de partidos/actas encontrados: {len(partits_links)}")
        print(f"📊 Contenedores de datos encontrados: {len(containers)}")

        # Mapeo a las tablas de Supabase
        print("🚀 Análisis de estructura completado con éxito.")

    except Exception as e:
        print(f"❌ Error durante la extracción: {e}")

if __name__ == "__main__":
    run_scraper()
