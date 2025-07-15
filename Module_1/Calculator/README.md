# Calculator Script

## Overview
The `calculator.py` script is a command-line tool that performs basic arithmetic operations (addition, subtraction, multiplication, division, modulus, exponentiation, and floor division) on two user-provided numbers. It includes input validation and allows users to continue or exit calculations.

## Features
- Supports seven arithmetic operations:
  - Addition
  - Subtraction
  - Multiplication
  - Division
  - Modulus
  - Exponentiation
  - Floor division
- Validates numeric inputs and operation selections
- Handles division by zero
- Allows users to continue or exit via a prompt

## Requirements
- Python 3.8 or higher
- No additional dependencies (uses standard library)

## Setup Instructions

1. **Run the script**:
   ```bash
   python calculator.py
   ```

## Usage
1. Run the script using the command above.
2. Enter the first number when prompted.
3. Enter the second number.
4. Select an operation by entering a number (1–7) corresponding to the displayed menu.
5. View the result of the calculation.
6. Choose to continue (`Yes`, `yes`, `y`, or `Y`) or exit (any other input).
7. If invalid inputs are provided (e.g., non-numeric values), an error message will prompt for valid input.

## Example
```plaintext
Enter the first Number: 10
Enter the Second Number: 5
1. Addition
2. Subtraction
3. Multiplication
4. Division
5. Modulus
6. Exponentiation
7. Floor division
Enter the Operation Number (1-7): 1
15
Do you want to continue the calculation (Yes/No): Yes
...
Do you want to continue the calculation (Yes/No): No
Thank you!
```
