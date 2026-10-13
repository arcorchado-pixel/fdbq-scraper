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
    print("🔍 Conectando a la web de Bàsquet Català evitando el bloqueo de seguridad...")
    
    try:
        # Creamos el scraper capaz de resolver retos de Cloudflare
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        response = scraper.get(URL, timeout=20)
        
        print(f"📥 Código de estado HTTP: {response.status_code}")
        
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find('title')
        title_text = title.text.strip() if title else 'No encontrado'
        print(f"🏷️ Título real de la página: {title_text}")
        
        if "Verificació" not in title_text:
            rows = soup.find_all("tr")
            links = soup.find_all("a")
            partits = [a['href'] for a in links if a.has_attr('href') and ('partit' in a['href'] or 'acta' in a['href'])]
            
            print(f"📊 Filas de tabla encontradas: {len(rows)}")
            print(f"🔗 Enlaces a actas/partidos encontrados: {len(partits)}")
            print("🚀 ¡Pantalla de seguridad superada con éxito!")
        else:
            print("⚠️ Aún detecta la pantalla de verificación. Ajustando hiperparámetros...")

    except Exception as e:
        print(f"❌ Error durante la conexión: {e}")

if __name__ == "__main__":
    run_scraper()
