import argparse

def main():
    # 1. Tworzymy parser
    parser = argparse.ArgumentParser(description="Przykład parsowania argumentów")

    # 2. Dodajemy argumenty
    parser.add_argument('--mode', type=str, help='Tryb działania programu')
    parser.add_argument('--input', type=str, help='Plik wejściowy')
    parser.add_argument('--verbose', action='store_true', help='Włącz tryb szczegółowy')

    # 3. Parsujemy argumenty
    args = parser.parse_args()

    # 4. Używamy ich w programie
    print("Tryb działania:", args.mode)
    print("Plik wejściowy:", args.input)
    print("Tryb szczegółowy:", args.verbose)

if __name__ == '__main__':
    main()