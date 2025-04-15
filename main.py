from functions import *

def main():
    users = load_users()
    passwords = load_passwords()
    grades = load_grades()
    eca = load_eca()

    print("Welcome to the Student Profile Management System")

    while True:
        username = input("\nEnter username: ")
        password = input("Enter password: ")

        if username in passwords and passwords[username] == password:
            user = users[username]

            if user.role == "admin":
                print(f"\nWelcome, Admin {user.full_name}")
                admin_menu(users, passwords, grades, eca)
            elif user.role == "student":
                print(f"\nWelcome, {user.full_name}")
                student = Student(user.user_id, user.username, user.full_name, user.age, user.email, user.role, grades.get(user.user_id, []), eca.get(user.user_id, []))
                student_menu(student)
            else:
                print("Invalid role.")
        else:
            print("Incorrect username or password. Try again.")

if __name__ == "__main__":
    main()
