import os
import shutil
from p7m_to_xml import process_folder
def unzip(path_in, path_out):
    """Mock function for Group 1 - will be replaced with actual unzip implementation"""
    print(f"Unzipping from {path_in} to {path_out}")
    return path_out

def xml_to_csv(path_xml, csv_path):
    """Mock function for Group 4 - will be replaced with actual XML to CSV implementation"""
    print(f"Converting XML files from {path_xml} to CSV at {csv_path}")
    return csv_path

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

def main():
    """Main coordination function"""
    # Define folder paths
    INPUT_FOLDER = 'zip'              # Group 1 input
    UNZIPPED_FOLDER = 'unzippati'     # Group 1 output
    XML_FOLDER = 'xml'                # Final XML folder
    P7M_FOLDER = 'p7m'                # P7M processing folder
    CSV_OUTPUT = 'output.csv'         # Group 4 output
    
    print("=== PROJECT COORDINATION STARTING ===\n")
    
    # Step 1: Group 1 - Unzip files
    print("Step 1: Group 1 - Unzipping files...")
    unzipped_path = unzip(INPUT_FOLDER, UNZIPPED_FOLDER)
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
    csv_result = xml_to_csv(XML_FOLDER, CSV_OUTPUT)
    print(f"CSV conversion completed: {csv_result}\n")
    
    print("=== PROJECT COORDINATION COMPLETED ===")

if __name__ == "__main__":
    main()