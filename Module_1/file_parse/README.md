# File Parser CLI Tool

## Overview
The `file.py` script is a command-line tool for parsing text files. It allows users to count lines, words, and characters, search for keywords, and extract specific line ranges from a text file.

## Features
- Count total lines in a file
- Count total words in a file
- Count total characters (including spaces and newlines)
- Search for a keyword (case-insensitive) and display matching lines
- Extract and display a range of lines
- Handles file not found errors and invalid inputs

## Requirements
- Python 3.8 or higher
- No additional dependencies (uses standard library)

## Setup Instructions
1. **Ensure the script and text file are available**:
   - Place `file.py` in desired directory.
   - Have a text file (e.g., `sample.txt`) ready in a known location.

2. **Run the script**:
   ```bash
   python file.py
   ```

## Usage
1. Run the script using the command above.
2. Enter the path to the text file when prompted (e.g., `sample.txt` or `/path/to/sample.txt`).
3. Select an option from the menu (1–6):
   - 1: Count total lines
   - 2: Count total words
   - 3: Count total characters
   - 4: Search for a keyword
   - 5: Extract a range of lines
   - 6: Exit
4. Follow prompts for specific actions (e.g., enter a keyword or line numbers).
5. If the file is not found or invalid inputs are provided, appropriate error messages will be displayed.

## Example
```plaintext
Welcome to File Parser CLI Tool
Enter the path to the text file: sample.txt
Menu
1. Count Lines
2. Count Words
3. Count Characters
4. Search Keyword
5. Extract Lines
6. Exit
Choose an option (1-6): 1
Total lines: 10
...
Choose an option (1-6): 4
Enter keyword to search: hello
Line 3: hello world
Line 7: Hello there
...
Choose an option (1-6): 6
Goodbye!
```
