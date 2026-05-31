from extract import extract
from load import load
from tests.show_bronze import show_bronze

def main() -> None:
    data = extract()
    load(data)

if __name__ == "__main__":
    main()