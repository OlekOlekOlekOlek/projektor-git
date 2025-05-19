import argparse
import json
import os
import sys


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


def main():
    parser = argparse.ArgumentParser(description="Konwerter plików (.json, .xml, .yml)")
    parser.add_argument("source", help="Plik wejściowy (.json)")
    parser.add_argument("target", help="Plik wyjściowy (np. wynik.yaml)")
    args = parser.parse_args()

    print("Plik wejściowy:", args.source)
    print("Plik wyjściowy:", args.target)

    ext = os.path.splitext(args.source)[1].lower()
    if ext != ".json":
        print("  Na tym etapie obsługiwane są tylko pliki .json")
        sys.exit(1)

    data = read_json(args.source)
    if data is not None:
        print(" Dane wczytane z JSON:", data)


if __name__ == "__main__":
    main()