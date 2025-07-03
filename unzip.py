import os
import zipfile
from pathlib import Path

def estrai_zip_ricorsivo(cartella_base, elimina_zip=False, cartella_destinazione="unzipped"):
    """
    Estrae tutti i file ZIP trovati ricorsivamente in una cartella.
    Continua l'estrazione fino a quando non rimangono più file ZIP da estrarre (gestisce ZIP annidati).
    
    Args:
        cartella_base (str): Percorso della cartella da esplorare
        elimina_zip (bool): Se True, elimina i file ZIP ORIGINALI (non quelli estratti)
        cartella_destinazione (str): Cartella dove estrarre (default: "unzipped")
    
    Returns:
        list: Lista dei file ZIP elaborati con i relativi stati
    """
    risultati = []
    cartella_base = Path(cartella_base)
    dest_dir = Path(cartella_destinazione)
    
    # Crea la cartella di destinazione se non esiste
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Set per tenere traccia dei file già processati (per evitare loop infiniti)
    file_processati = set()
    
    ciclo = 1
    while True:
        zip_trovati = False
        zip_di_questo_ciclo = []
        
        print(f"\n--- Ciclo {ciclo} di estrazione ---")
        
        # Cerca ZIP nella cartella base E nella cartella di destinazione
        cartelle_da_cercare = [cartella_base, dest_dir]
        
        for cartella in cartelle_da_cercare:
            if not cartella.exists():
                continue
                
            print(f"Cerco ZIP in: {cartella}")
            
            for zip_path in cartella.rglob("*.zip"):
                # Evita di processare lo stesso file più volte
                zip_path_str = str(zip_path.resolve())
                if zip_path_str in file_processati:
                    print(f"⏭️ Già processato: {zip_path}")
                    continue
                    
                print(f"🔍 Trovato ZIP: {zip_path}")
                zip_trovati = True
                zip_di_questo_ciclo.append(zip_path)
                file_processati.add(zip_path_str)
                
                try:
                    # Verifica che sia un ZIP valido
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        file_list = zip_ref.namelist()
                        print(f"📋 Contenuto di {zip_path.name}: {file_list}")
                        
                        # Estrai il file ZIP
                        zip_ref.extractall(dest_dir)
                    
                    risultati.append({
                        'file': str(zip_path),
                        'stato': f'estratto (ciclo {ciclo})',
                        'destinazione': str(dest_dir),
                        'contenuto': file_list
                    })
                    
                    print(f"✓ Estratto: {zip_path}")
                    
                except zipfile.BadZipFile:
                    risultati.append({
                        'file': str(zip_path),
                        'stato': 'errore - file ZIP corrotto',
                        'destinazione': None
                    })
                    print(f"✗ Errore - file corrotto: {zip_path}")
                    continue
                    
                except PermissionError:
                    risultati.append({
                        'file': str(zip_path),
                        'stato': 'errore - permessi insufficienti',
                        'destinazione': None
                    })
                    print(f"✗ Errore - permessi: {zip_path}")
                    continue
                    
                except Exception as e:
                    risultati.append({
                        'file': str(zip_path),
                        'stato': f'errore - {str(e)}',
                        'destinazione': None
                    })
                    print(f"✗ Errore generico: {zip_path} - {e}")
                    continue
        
        # Elimina i file ZIP di questo ciclo (dopo averli tutti estratti)
        for zip_path in zip_di_questo_ciclo:
            try:
                # Elimina ZIP dalla cartella originale se richiesto
                if elimina_zip and not str(zip_path).startswith(str(dest_dir)):
                    zip_path.unlink()
                    print(f"✓ Eliminato ZIP originale: {zip_path}")
                # Elimina sempre i ZIP estratti nella cartella di destinazione
                elif str(zip_path).startswith(str(dest_dir)):
                    zip_path.unlink()
                    print(f"✓ Eliminato ZIP estratto: {zip_path}")
            except Exception as e:
                print(f"⚠️ Errore eliminazione {zip_path}: {e}")
        
        # Se non sono stati trovati ZIP, esci dal ciclo
        if not zip_trovati:
            print(f"✓ Nessun altro file ZIP trovato. Estrazione completata in {ciclo-1} cicli.")
            break
            
        ciclo += 1
        
        # Protezione contro cicli infiniti
        if ciclo > 100:
            print("⚠️ Raggiunto limite massimo di cicli (100). Interruzione per sicurezza.")
            break
    
    return risultati


# Esempio di utilizzo
if __name__ == "__main__":
    # Estrai tutti i ZIP (inclusi quelli annidati) nella cartella "unzipped"
    risultati = estrai_zip_ricorsivo("/Users/lcorsaro/Desktop/PW_2025/ZIP", elimina_zip=False, 
                                     cartella_destinazione="/Users/lcorsaro/Desktop/PW_2025/ALL")
    
    print(f"\nRiepilogo finale: {len(risultati)} file ZIP elaborati")
    for r in risultati:
        print(f"- {r['file']}: {r['stato']}")
    
    # Esempio con cartella specifica
    # risultati = estrai_zip_ricorsivo("/percorso/alla/cartella")
    
    # Esempio con cartella di destinazione personalizzata
    # risultati = estrai_zip_ricorsivo("root", cartella_destinazione="documenti_estratti")