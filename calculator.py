def add(x, y):
    """Add two numbers"""
    return x + y

def subtract(x, y):
    """Subtract two numbers"""
    return x - y

def multiply(x, y):
    """Multiply two numbers"""
    return x * y

def divide(x, y):
    """Divide two numbers"""
    if y == 0:
        return "Error: Cannot divide by zero"
    return x / y

def calculator():
    """Run the calculator app"""
    print("=" * 40)
    print("       SIMPLE CALCULATOR")
    print("=" * 40)
    
    while True:
        print("\nSelect operation:")
        print("1. Add (+)")
        print("2. Subtract (-)")
        print("3. Multiply (*)")
        print("4. Divide (/)")
        print("5. Exit")
        
        choice = input("\nEnter choice (1/2/3/4/5): ").strip()
        
        if choice == '5':
            print("\nThank you for using the calculator. Goodbye!")
            break
        
        if choice not in ['1', '2', '3', '4']:
            print("Invalid input. Please select a valid operation.")
            continue
        
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if choice == '1':
                print(f"\n{num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"\n{num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"\n{num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                result = divide(num1, num2)
                print(f"\n{num1} / {num2} = {result}")
        
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

if __name__ == "__main__":
    calculator()
