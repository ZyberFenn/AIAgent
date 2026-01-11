from functions.write_file import write_file


if __name__ == "__main__":
    print("Overwriting lorem.txt:")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print()

    print("Writing new file in pkg/:")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print()

    print("Attempting to write outside working directory:")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
