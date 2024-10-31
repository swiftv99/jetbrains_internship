import sys
import random

def main():
    while True:
        welcome_message = """_________________________________________
Welcome to Pseudo-Random Number Generator
Available options: 'Hi', 'GetRandom' or 'Shutdown'

Please enter your input : """
        print(welcome_message)
        
        command = input().strip()
        if command == "Hi":
            print("Hi")
            sys.stdout.flush()
        elif command == "GetRandom":
            print(random.randint(1, 100)) # Generates a pseudo-random number between 1 and 100
            sys.stdout.flush()
        elif command == "Shutdown":
            print("Program terminated")
            break
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
