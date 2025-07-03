import os
import shutil
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