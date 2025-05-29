import argparse
import json
import os
import sys
import yaml
import xml.etree.ElementTree as ET

def dict_to_xml(tag: str, d) -> ET.Element:
    elem = ET.Element(tag)


    if not isinstance(d, dict):
        elem.text = str(d)
        return elem

    for key, val in d.items():
        if isinstance(val, dict):
            child = dict_to_xml(key, val)
            elem.append(child)
        elif isinstance(val, list):
            for item in val:
                child = dict_to_xml(key, item)
                elem.append(child)
        else:
            child = ET.SubElement(elem, key)
            child.text = str(val)
    return elem

def write_xml(data: dict, file_path: str) -> bool:
    try:
        if len(data) != 1:
            print("Dane do zapisu XML powinny mieć dokładnie jeden klucz - nazwę głównego elementu.")
            return False
        root_tag = list(data.keys())[0]
        root_elem = dict_to_xml(root_tag, data[root_tag])

        tree = ET.ElementTree(root_elem)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        print(f"Dane zapisane do pliku XML: {file_path}")
        return True
    except Exception as e:
        print(f"Błąd zapisu XML: {e}")
        return False

def read_xml(file_path: str) -> ET.Element | None:
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        print("Plik XML poprawny.")
        return root
    except FileNotFoundError:
        print(f"Plik '{file_path}' nie istnieje.")
    except ET.ParseError as e:
        print(f"Błąd składni XML – {e}")
    return None

def read_yaml(file_path: str) -> dict | None:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        print("Plik YAML poprawny.")
        return data
    except FileNotFoundError:
        print(f" Plik '{file_path}' nie istnieje.")
    except yaml.YAMLError as e:
        print(f" Błąd składni YAML – {e}")
    return None

def write_yaml(data: dict, file_path: str) -> bool:
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
        print(f" Dane zapisane do pliku YAML: {file_path}")
        return True
    except Exception as e:
        print(f" Błąd zapisu YAML: {e}")
        return False




def read_json(file_path: str) -> dict | None:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(" Plik JSON poprawny.")
        return data
    except FileNotFoundError:
        print(f" Plik '{file_path}' nie istnieje.")
    except json.JSONDecodeError as e:
        print(f" Błąd składni JSON – {e.msg} (linia {e.lineno}, kolumna {e.colno})")
    return None

def write_json(data: dict, file_path: str) -> bool:
    """Zapisuje obiekt Pythona do pliku JSON.  Zwraca True/False."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f" Dane zapisane do {file_path}")
        return True
    except Exception as e:
        print(f" Nie udało się zapisać pliku: {e}")
    return False

def main():
    parser = argparse.ArgumentParser(description="Konwerter plików (.json, .xml, .yml)")
    parser.add_argument("source", help="Plik wejściowy (.json)")
    parser.add_argument("target", help="Plik wyjściowy (np. wynik.yaml)")
    args = parser.parse_args()

    print("Plik wejściowy:", args.source)
    print("Plik wyjściowy:", args.target)

    ext = os.path.splitext(args.source)[1].lower()

    if ext == ".json":
        data = read_json(args.source)
    elif ext in [".yaml", ".yml"]:
        data = read_yaml(args.source)
    elif ext == ".xml":
        root = read_xml(args.source)
        if root is None:
            print("Nie udało się wczytać danych z XML.")
            sys.exit(1)
        data = {root.tag: {child.tag: child.text for child in root}}
    else:
        print("Obsługiwane wejścia to tylko .json, .yaml i .xml")
        sys.exit(1)
    
    if data is None:
        print(" Nie udało się wczytać danych.")
        sys.exit(1)

    ext_out = os.path.splitext(args.target)[1].lower()

    if ext_out == ".json":
        write_json(data, args.target)
    elif ext_out in [".yaml", ".yml"]:
        write_yaml(data, args.target)
    elif ext_out == ".xml":
        write_xml(data, args.target)
    
    else:
        print("Obsługiwane wyjścia to tylko .json i .yaml")
        sys.exit(1)

if __name__ == "__main__":
    main()