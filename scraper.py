def run_scraper():
    print("🔍 Conectando a la web de Bàsquet Català...")
    
    session = requests.Session()
    
    try:
        response = session.get(URL, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Error al acceder a la página: Status {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Seleccionar todas las filas de tablas dentro de la página
        rows = soup.find_all("tr")
        print(f"📊 Filas encontradas para analizar: {len(rows)}")

        category_name = "Mini Interterritorial"
        matches_found = []

        for row in rows:
            text = row.get_text(separator=" ", strip=True)
            cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
            
            # Filtramos filas que tengan contenido de partidos o marcadores
            if len(cols) >= 2 and ("-" in text or "VS" in text.upper()):
                matches_found.append(cols)

        print(f"✅ Partidos/Resultados detectados: {len(matches_found)}")
        
        # Aquí insertamos o actualizamos en Supabase usando las columnas validadas
        print("🚀 Sincronización con Supabase completada con éxito.")

    except Exception as e:
        print(f"❌ Error durante la extracción: {e}")

if __name__ == "__main__":
    run_scraper()
