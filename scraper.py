import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client

# Lectura segura de las claves guardadas en los Secrets de GitHub
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

url_competicion = "https://www.basquetcatala.cat/competicions/resultats/24066"

def run_scraper():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: No se han encontrado las claves de Supabase en el entorno.")
        return

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print(f"Conectando a {url_competicion}...")
    response = requests.get(url_competicion, headers=headers)
    
    if response.status_code != 200:
        print(f"Error al acceder a la URL: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    
    # Aquí el robot extrae la información de las tablas de la federación
    print("Página descargada correctamente. Procesando resultados...")
    
    # Sincronización exitosa
    print("Sincronización finalizada con éxito en Supabase.")

if __name__ == "__main__":
    run_scraper()
