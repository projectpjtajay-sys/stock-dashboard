class Student:
    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade

    def display_info(self):
        print(f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Grade: {self.grade}")

class StudentManagementSystem:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        for s in self.students:
            if s.student_id == student.student_id:
                print(f"Student ID {student.student_id} already exists.")
                return
        self.students.append(student)
        print(f"Student {student.name} added successfully!")

    def remove_student(self, student_id):
        for i, s in enumerate(self.students):
            if s.student_id == student_id:
                removed = self.students.pop(i)
                print(f"Student {removed.name} removed successfully!")
                return
        print("Student not found.")

    def display_all_students(self):
        if not self.students:
            print("No students in the system.")
        else:
            print("\nAll Students:")
            for s in self.students:
                s.display_info()

    def search_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                print("Student found:")
                s.display_info()
                return
        print("Student not found.")

def get_valid_id():
    while True:
        try:
            student_id = int(input("Enter student ID: "))
            if student_id > 0:
                return student_id
            print("ID must be a positive number.")
        except ValueError:
            print("Please enter a valid number.")

def get_valid_age():
    while True:
        try:
            age = int(input("Enter age: "))
            if 1 <= age <= 120:
                return age
            print("Age must be between 1 and 120.")
        except ValueError:
            print("Please enter a valid number.")

def get_valid_grade():
    grades = ['A', 'B', 'C', 'D', 'F']
    while True:
        grade = input("Enter grade (A, B, C, D, F): ").strip().upper()
        if grade in grades:
            return grade
        print("Grade must be A, B, C, D, or F.")

def main():
    system = StudentManagementSystem()
    while True:
        print("\nStudent Management System")
        print("1. Add Student")
        print("2. Remove Student")
        print("3. Search Student")
        print("4. Display All Students")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            print("\nAdd New Student")
            student_id = get_valid_id()
            name = input("Enter name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            age = get_valid_age()
            grade = get_valid_grade()
            student = Student(student_id, name, age, grade)
            system.add_student(student)

        elif choice == '2':
            print("\nRemove Student")
            student_id = get_valid_id()
            system.remove_student(student_id)

        elif choice == '3':
            print("\nSearch Student")
            student_id = get_valid_id()
            system.search_student(student_id)

        elif choice == '4':
            system.display_all_students()

        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()


