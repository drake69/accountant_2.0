from p7m_to_xml import process_folder
from unzip import estrai_zip_ricorsivo
from separazione import separate_files
from Anonimizzazione import xml_tocsvs

def main(INPUT_FOLDER, UNZIPPED_FOLDER, XML_FOLDER = 'xml', P7M_FOLDER = 'p7m', CSV_OUTPUT = 'output.csv'):
    print("=== PROJECT COORDINATION STARTING ===\n")
    
    # Step 1: Group 1 - Unzip files
    print("Step 1: Group 1 - Unzipping files...")
    unzipped_path = estrai_zip_ricorsivo(INPUT_FOLDER, cartella_destinazione=UNZIPPED_FOLDER)
    print(f"Unzipping completed. Files available at: {unzipped_path}\n")
    
    # Step 2: Group 2 - Separate XML and P7M files
    print("Step 2: Group 2 - Separating files...")
    separate_files(UNZIPPED_FOLDER, XML_FOLDER, P7M_FOLDER)
    print("File separation completed.\n")
    
    # Step 3: Group 3 - Convert P7M to XML
    print("Step 3: Group 3 - Converting P7M to XML...")
    process_folder(P7M_FOLDER, XML_FOLDER)  # This adds converted XMLs to main XML folder
    print()
    
    # Step 4: Group 4 - Convert XML to CSV
    print("Step 4: Group 4 - Converting XML to CSV...")
    xml_tocsvs(XML_FOLDER, CSV_OUTPUT)
    
    print("=== PROJECT COORDINATION COMPLETED ===")

if __name__ == "__main__":
    main(INPUT_FOLDER='input', # Da cambiare in base alla cartella di input
         UNZIPPED_FOLDER='unzipped') # Da cambiare in base alla cartella di output degli unzip