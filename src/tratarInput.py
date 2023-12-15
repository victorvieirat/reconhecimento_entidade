import json
import sys

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data


def main():
    if len(sys.argv) != 2:
        print("Uso: python tratarInput.py <caminho_arquivo_json>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    json_data = read_json_file(json_file_path)

    if json_data:
        print(json.dumps(json_data, indent=2))  # Print JSON with indentation

if __name__ == "__main__":
    main()

