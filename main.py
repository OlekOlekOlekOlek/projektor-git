import argparse
import json
import os
import sys
import yaml

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

def read_json(file_path: str) -> dict | None:
    """Wczytuje plik JSON i zwraca dane jako obiekt Pythona.
    Gdy składnia jest niepoprawna – wypisuje błąd i zwraca None."""
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
    ext = os.path.splitext(args.source)[1].lower()

    if ext == ".json":
        data = read_json(args.source)
    elif ext in [".yaml", ".yml"]:
        data = read_yaml(args.source)
    else:
        print("Na tym etapie obsługiwane są tylko pliki .json i .yaml")
    sys.exit(1)    
    
    if os.path.splitext(args.target)[1].lower() != ".json":
            print("  Na tym etapie plik wyjściowy musi mieć rozszerzenie .json")
            sys.exit(1)




    data = read_json(args.source)
    if data is not None:
        print(" Dane wczytane z JSON:", data)

    write_json(data, args.target)

if __name__ == "__main__":
    main()