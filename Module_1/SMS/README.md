# Student Management System

## Overview
The `sms.py` script is a command-line tool for managing student records. It allows users to add, remove, search, and display student information, with validation for student ID, age, and grade.

## Features
- Add a student with a unique ID, name, age, and grade
- Remove a student by ID
- Search for a student by ID
- Display all students
- Validates:
  - Student ID (positive integer)
  - Age (1–120)
  - Grade (A, B, C, D, or F)
- Prevents duplicate student IDs

## Requirements
- Python 3.8 or higher
- No additional dependencies (uses standard library)

## Setup Instructions

**Run the script**:
   ```bash
   python sms.py
   ```

## Usage
1. Run the script using the command above.
2. Select an option from the menu (1–5):
   - 1: Add a new student
   - 2: Remove a student by ID
   - 3: Search for a student by ID
   - 4: Display all students
   - 5: Exit
3. Follow prompts for specific actions (e.g., enter student details or ID).
4. Input validation ensures valid student IDs, ages, grades, and non-empty names.
5. Appropriate messages are displayed for successful actions or errors (e.g., duplicate ID, student not found).

## Example
```plaintext
Student Management System
1. Add Student
2. Remove Student
3. Search Student
4. Display All Students
5. Exit
Choose an option (1-5): 1
Add New Student
Enter student ID: 1
Enter name: Ajay K
Enter age: 21
Enter grade (A, B, C, D, F): A
Student Ajay K added successfully!
...
Choose an option (1-5): 4
All Students:
ID: 1, Name: Ajay K, Age: 21, Grade: A
...
Choose an option (1-5): 5
Goodbye!
```
