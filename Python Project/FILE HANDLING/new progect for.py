## password manager program


""""user:
1-dictonnary
2-loops
3-conditions
4-module:randam
5-file handling

website: password
randam Module
read word
"""""
import random
import string

password = {}
# load existing passwords from file

try: 
    with open("passwords.txt", "r") as file:
        for line in file:
            website, pwd = line.strip().split(":")
            password[website] = pwd
except:
         pass
def generate_password():
     chars = string.ascii_letters + string.digits + "#^$&#^"
     password = "".join(random.choice(chars) for _ in range(12))
     return password
while True:
     print("\n+____PRESONAL PASSWORD MANAGER____")
     print("1. Add a new password")
     print("2. View all passwords") 
     print("3. generate a random password")
     print("4. Exit")

     Choice = input("Enter your choice: ")

     if Choice == "1":
            website = input("Enter the website: ")
            pwd = input("Enter the password (or leave blank to generate): ")

            password[website] = pwd 
            with open("passwords.txt", "a") as file:
                file.write(f"{website}:{pwd}\n")

                print("Password added successfully!")

     elif Choice == "2":
            print("\n--- Saved Passwords ---")
            for website, pwd in password.items():
                print(f"{website}: {pwd}")

     elif Choice == "3":
            generated_password = generate_password()
            print(f"Generated password: {generated_password}")

     elif Choice == "4":
            print("Exiting...")
            break
     
     else:
            print("Invalid choice. Please try again.")
            