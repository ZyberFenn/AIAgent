from functions.get_file_content import get_file_content
from config import MAX_FILE_CHARS


if __name__ == "__main__":
    print("Testing large file truncation:")
    lorem_content = get_file_content("calculator", "lorem.txt")
    print(f"Length: {len(lorem_content)}")
    print(lorem_content[-100:])
    print()

    print("Reading main.py:")
    print(get_file_content("calculator", "main.py"))
    print()

    print("Reading pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    print("Attempting to read /bin/cat:")
    print(get_file_content("calculator", "/bin/cat"))
    print()

    print("Attempting to read missing file:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
