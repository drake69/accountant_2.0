import os
import shutil
from p7m_to_xml import process_folder
from unzip import estrai_zip_ricorsivo

def separate_files(source_folder, xml_folder, p7m_folder):
    """
    Group 2 main function: Separates XML and P7M files into their respective folders
    """
    # Create directories if they don't exist
    os.makedirs(xml_folder, exist_ok=True)
    os.makedirs(p7m_folder, exist_ok=True)
    
    xml_count = 0
    p7m_count = 0
    other_count = 0
    
    print(f"Processing files from: {source_folder}")
    
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder {source_folder} does not exist")
        return
    
    # Process each file in the source folder
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        
        # Skip directories
        if os.path.isdir(source_path):
            continue
            
        if filename.endswith('.xml'):
            # Move XML files to XML folder
            destination = os.path.join(xml_folder, filename)
            shutil.move(source_path, destination)
            xml_count += 1
            print(f"Moved XML: {filename}")
            
        elif filename.endswith('.p7m'):
            # Move P7M files to P7M folder
            destination = os.path.join(p7m_folder, filename)
            shutil.move(source_path, destination)
            p7m_count += 1
            print(f"Moved P7M: {filename}")
            
        else:
            # Handle other file types
            other_count += 1
            print(f"Unrecognized file type: {filename}")
    
    print(f"\nFile separation complete:")
    print(f"- XML files moved: {xml_count}")
    print(f"- P7M files moved: {p7m_count}")
    print(f"- Other files: {other_count}")

def main(INPUT_FOLDER, UNZIPPED_FOLDER, XML_FOLDER = 'xml', P7M_FOLDER = 'p7m', CSV_OUTPUT = 'output.csv'):
    print("=== PROJECT COORDINATION STARTING ===\n")
    
    # Step 1: Group 1 - Unzip files
    print("Step 1: Group 1 - Unzipping files...")
    unzipped_path = estrai_zip_ricorsivo(INPUT_FOLDER, cartella_destinazione=UNZIPPED_FOLDER)
    print(f"Unzipping completed. Files available at: {unzipped_path}\n")
    
    # Step 2: Group 2 - Separate XML and P7M files
    print("Step 2: Group 2 - Separating files...")
    separate_files(UNZIPPED_FOLDER, XML_FOLDER, P7M_FOLDER)
    print()
    
    # Step 3: Group 3 - Convert P7M to XML
    print("Step 3: Group 3 - Converting P7M to XML...")
    process_folder(P7M_FOLDER, XML_FOLDER)  # This adds converted XMLs to main XML folder
    print()
    
    # Step 4: Group 4 - Convert XML to CSV
    print("Step 4: Group 4 - Converting XML to CSV...")
    # csv_result = xml_to_csv(XML_FOLDER, CSV_OUTPUT)
    print(f"CSV conversion completed: {csv_result}\n")
    
    print("=== PROJECT COORDINATION COMPLETED ===")

if __name__ == "__main__":
    main()