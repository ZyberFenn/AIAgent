from functions.run_python_file import run_python_file


if __name__ == "__main__":
    print("Running calculator with no args:")
    print(run_python_file("calculator", "main.py"))
    print()

    print("Running calculator with expression:")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    print("Running calculator tests:")
    print(run_python_file("calculator", "tests.py"))
    print()

    print("Attempting to execute outside working directory:")
    print(run_python_file("calculator", "../main.py"))
    print()

    print("Attempting to execute nonexistent file:")
    print(run_python_file("calculator", "nonexistent.py"))
    print()

    print("Attempting to execute non-Python file:")
    print(run_python_file("calculator", "lorem.txt"))
