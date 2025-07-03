import re
import base64
import os

def extract_xml_from_p7m(file_data):
    """Estrae XML da P7M senza OpenSSL"""
    
    # Metodo 1: Cerca pattern XML direttamente
    xml_patterns = [b'<?xml', b'<FatturaElettronica', b'<p:FatturaElettronica']
    
    for pattern in xml_patterns:
        start = file_data.find(pattern)
        if start != -1:
            xml_data = file_data[start:]
            # Trova fine XML
            end_patterns = [b'</FatturaElettronica>', b'</p:FatturaElettronica>']
            for end_pattern in end_patterns:
                end = xml_data.find(end_pattern)
                if end != -1:
                    xml_data = xml_data[:end + len(end_pattern)]
                    return xml_data.decode('utf-8', errors='ignore')
            return xml_data.decode('utf-8', errors='ignore')
    
    # Metodo 2: Se base64 encoded
    if not re.findall(b'<', file_data):
        try:
            decoded = base64.decodebytes(file_data)
            return extract_xml_from_p7m(decoded)  # Ricorsione sul decoded
        except:
            pass
    
    # Metodo 3: Prova encoding diversi
    try:
        text = file_data.decode('unicode_escape')
        xml_start = text.find('<?xml')
        if xml_start != -1:
            xml_content = text[xml_start:]
            end_pos = xml_content.find('</FatturaElettronica>')
            if end_pos == -1:
                end_pos = xml_content.find('</p:FatturaElettronica>')
            if end_pos != -1:
                xml_content = xml_content[:end_pos + 21]  # +21 per tag di chiusura
            return xml_content
    except:
        pass
    
    return None

def p7m_to_xml_file(file_path, output_folder="xml_clean"):
    """Processa file P7M per file"""
    os.makedirs(output_folder, exist_ok=True)
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    xml_content = extract_xml_from_p7m(data)
    
    if xml_content:
        filename = os.path.basename(file_path).replace('.p7m', '_clean.xml')
        output_path = os.path.join(output_folder, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f" XML estratto: {output_path}")
        return output_path
    else:
        print(f" XML non trovato in: {file_path}")
        return None

def p7m_to_xml(input_folder="p7m", output_folder="xml_clean"):
    """Processa tutti i P7M in una cartella"""
    count = 0
    for filename in os.listdir(input_folder):
        if filename.endswith('.p7m'):
            file_path = os.path.join(input_folder, filename)
            if p7m_to_xml_file(file_path, output_folder):
                count += 1
    print(f" Processati {count} file")

if __name__ == "__main__":
    # Esegui il processo su una cartella specifica
    p7m_to_xml("/Users/lcorsaro/Desktop/PW_2025/P7M", "/Users/lcorsaro/Desktop/PW_2025/XML")
