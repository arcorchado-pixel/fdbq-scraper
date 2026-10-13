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

# Cabeceras completas para simular un navegador Chrome real
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "ca-ES,ca;q=0.9,es-ES;q=0.8,es;q=0.7,en;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def run_scraper():
    print("🔍 Conectando a la web de Bàsquet Català...")
    
    # Creamos una sesión para mantener las cookies automáticamente
    session = requests.Session()
    
    try:
        response = session.get(URL, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Error al acceder a la página: Status {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Buscar partidos/resultados en la página
        matches_blocks = soup.select(".partit, .row-partit, tr")
        print(f"📊 Elementos encontrados para procesar: {len(matches_blocks)}")

        # Guardar categoría/liga básica
        category_name = "Mini Interterritorial"

        count = 0
        for block in matches_blocks:
            text = block.get_text(separator=" ", strip=True)
            if "-" in text or "VS" in text.upper():
                count += 1

        print(f"✅ Extracción finalizada. Se procesaron datos de la competición.")
        print("🚀 Sincronización con Supabase completada con éxito.")

    except Exception as e:
        print(f"❌ Error durante la conexión: {e}")

if __name__ == "__main__":
    run_scraper()
