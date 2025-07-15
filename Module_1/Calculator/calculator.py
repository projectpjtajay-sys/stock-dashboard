while True:
    try:
        a = int(input("Enter the first Number: "))
        b = int(input("Enter the Second Number: "))
        
        print("1. Addition\n2. Subtraction\n3. Multiplication\n4. Division\n5. Modulus\n6. Exponentiation\n7. Floor division")
        Operation_number = int(input("Enter the Operation Number (1-7): "))
        
        if Operation_number == 1:
            print(a + b)
        elif Operation_number == 2:
            print(a - b)
        elif Operation_number == 3:
            print(a * b)
        elif Operation_number == 4:
            if b != 0:
                print(a / b)
            else:
                print("Cannot divide by zero")
        elif Operation_number == 5:
            if b != 0:
                print(a % b)
            else:
                print("Cannot compute modulus with zero")
        elif Operation_number == 6:
            print(a ** b)
        elif Operation_number == 7:
            if b != 0:
                print(a // b)
            else:
                print("Cannot divide by zero")
        else:
            print("Invalid arithmetic operation selected. Please choose a number between 1 and 7.")
        
        s = input("Do you want to continue the calculation (Yes/No): ")
        if s not in ["Yes", "yes", "y", "Y"]:
            print("Thank you!")
            break
    
    except ValueError:
        print("Invalid input. Please enter valid numbers.")