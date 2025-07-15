class FileParser:
    def __init__(self, file_path):
        self.file_path = file_path
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.lines = f.readlines()
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            self.lines = []

    def count_lines(self):
        print(f"Total lines: {len(self.lines)}")

    def count_words(self):
        word_count = sum(len(line.split()) for line in self.lines)
        print(f"Total words: {word_count}")

    def count_characters(self):
        char_count = sum(len(line) for line in self.lines)
        print(f"Total characters: {char_count}")

    def search_keyword(self, keyword):
        found = False
        for i, line in enumerate(self.lines, start=1):
            if keyword.lower() in line.lower():
                print(f"Line {i}: {line.strip()}")
                found = True
        if not found:
            print(f"No matches found for '{keyword}'.")

    def extract_lines(self, start, end):
        if start < 1 or end > len(self.lines) or start > end:
            print("Invalid line range.")
            return
        print(f"\nExtracting lines {start} to {end}:")
        for i in range(start - 1, end):
            print(f"Line {i+1}: {self.lines[i].strip()}")

def main():
    print("Welcome to File Parser CLI Tool")

    file_path = input("Enter the path to the text file: ").strip()
    parser = FileParser(file_path)

    if not parser.lines:
        return  # Exit if file could not be loaded

    while True:
        print("\nMenu")
        print("1. Count Lines")
        print("2. Count Words")
        print("3. Count Characters")
        print("4. Search Keyword")
        print("5. Extract Lines")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == '1':
            parser.count_lines()
        elif choice == '2':
            parser.count_words()
        elif choice == '3':
            parser.count_characters()
        elif choice == '4':
            keyword = input("Enter keyword to search: ").strip()
            parser.search_keyword(keyword)
        elif choice == '5':
            try:
                start = int(input("Enter start line number: "))
                end = int(input("Enter end line number: "))
                parser.extract_lines(start, end)
            except ValueError:
                print("Please enter valid line numbers.")
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
