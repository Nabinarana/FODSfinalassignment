import matplotlib.pyplot as plt

class User:
    def __init__(self, user_id, username, full_name, age, email, role):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.age = age
        self.email = email
        self.role = role

class Student(User):
    def __init__(self, user_id, username, full_name, age, email, role, grades=[], activities=[]):
        super().__init__(user_id, username, full_name, age, email, role)
        self.grades = grades
        self.activities = activities

    def view_profile(self):
        print(f"\n--- Profile for {self.full_name} ---")
        print(f"ID: {self.user_id}")
        print(f"Age: {self.age}")
        print(f"Email: {self.email}")
        print(f"Grades: {self.grades}")
        print(f"ECA Activities: {self.activities}")

    def update_profile(self):
        print("\n--- Update Profile ---")

        new_full_name = input(f"Enter new full name (Current: {self.full_name}): ")
        self.full_name = new_full_name if new_full_name else self.full_name

        new_age = input(f"Enter new age (Current: {self.age}): ")
        if new_age:
            self.age = new_age

        new_email = input(f"Enter new email (Current: {self.email}): ")
        self.email = new_email if new_email else self.email

        print("Profile updated successfully.")

        self.save_user_data()

    def save_user_data(self):
        with open("data/users.txt", "r") as f:
            lines = f.readlines()

        with open("data/users.txt", "w") as f:
            for line in lines:
                parts = line.strip().split(",")
                if parts[0] == self.user_id:
                    f.write(f"{self.user_id},{self.username},{self.full_name},{self.age},{self.email},{self.role}\n")
                else:
                    f.write(line)
        print("User data saved.")

def load_users():
    users = {}
    try:
        with open("data/users.txt", "r") as f:
            for line in f:
                user_id, username, full_name, age, email, role = line.strip().split(",")
                users[username] = User(user_id, username, full_name, age, email, role)
    except FileNotFoundError:
        pass
    return users

def load_passwords():
    passwords = {}
    try:
        with open("data/passwords.txt", "r") as f:
            for line in f:
                username, password = line.strip().split(",")
                passwords[username] = password
    except FileNotFoundError:
        pass
    return passwords

def load_grades():
    grades = {}
    try:
        with open("data/grades.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                user_id = parts[0]
                grades[user_id] = list(map(int, parts[1:]))
    except FileNotFoundError:
        pass
    return grades

def load_eca():
    eca = {}
    try:
        with open("data/eca.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                user_id = parts[0]
                activities = parts[1].split(";") if len(parts) > 1 else []
                eca[user_id] = activities
    except FileNotFoundError:
        pass
    return eca

def save_users(users):
    with open("data/users.txt", "w") as f:
        for user in users.values():
            f.write(f"{user.user_id},{user.username},{user.full_name},{user.age},{user.email},{user.role}\n")

def save_passwords(passwords):
    with open("data/passwords.txt", "w") as f:
        for username, password in passwords.items():
            f.write(f"{username},{password}\n")

def save_grades(grades):
    with open("data/grades.txt", "w") as f:
        for user_id, marks in grades.items():
            f.write(f"{user_id}," + ",".join(map(str, marks)) + "\n")

def save_eca(eca):
    with open("data/eca.txt", "w") as f:
        for user_id, activities in eca.items():
            f.write(f"{user_id}," + ";".join(activities) + "\n")

def admin_menu(users, passwords, grades, eca):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add new user")
        print("2. Update user")
        print("3. Delete user")
        print("4. View insights")
        print("5. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            user_id = input("Enter ID: ")
            username = input("Enter username: ")
            full_name = input("Enter full name: ")
            age = input("Enter age: ")
            email = input("Enter email: ")
            role = "student"
            password = input("Enter password: ")
            eca_list = list(map(str.strip, input("Enter ECA activities separated by commas: ").split(",")))
            grades_list = list(map(int, input("Enter 5 subject marks separated by spaces: ").split()))
            if username in users:
                print("Username already exists.")
            else:
                users[username] = User(user_id, username, full_name, age, email, role)
                passwords[username] = password
                grades[user_id] = grades_list
                eca[user_id] = eca_list
                save_users(users)
                save_passwords(passwords)
                save_grades(grades)
                save_eca(eca)
                print("Student added successfully.")

        elif choice == "2":
            user_id = input("Enter the ID of the student to update: ").strip()

            target_user = None
            for user in users.values():
                if user.user_id == user_id:
                    target_user = user
                    break

            if target_user:
                print(f"\nFound student: {target_user.full_name} ({target_user.username})")
                print("What do you want to update?")
                print("1. Name")
                print("2. Email")
                print("3. Password")
                print("4. Grades")
                print("5. ECA Activities")
                update_choice = input("Enter choice: ")

                if update_choice == "1":
                    new_name = input("Enter new full name: ")
                    target_user.full_name = new_name
                    save_users(users)
                    print("Name updated successfully.")

                elif update_choice == "2":
                    new_email = input("Enter new email: ")
                    target_user.email = new_email
                    save_users(users)
                    print("Email updated successfully.")

                elif update_choice == "3":
                    new_password = input("Enter new password: ")
                    passwords[target_user.username] = new_password
                    save_passwords(passwords)
                    print("Password updated successfully.")

                elif update_choice == "4":
                    new_grades = list(map(int, input("Enter new 5 subject marks separated by spaces: ").split()))
                    grades[target_user.user_id] = new_grades
                    save_grades(grades)
                    print("Grades updated successfully.")

                elif update_choice == "5":
                    new_eca = list(map(str.strip, input("Enter new ECA activities separated by commas: ").split(",")))
                    eca[target_user.user_id] = new_eca
                    save_eca(eca)
                    print("ECA activities updated successfully.")

                else:
                    print("Invalid choice. Try again.")
            else:
                print("Student with this ID does not exist.")

        elif choice == "3":
            user_id = input("Enter user ID to delete: ").strip()
            username_to_delete = None
            for username, user in users.items():
                if user.user_id == user_id:
                    username_to_delete = username
                    break
            if username_to_delete:
                del users[username_to_delete]
                if username_to_delete in passwords:
                    del passwords[username_to_delete]
                if user_id in grades:
                    del grades[user_id]
                if user_id in eca:
                    del eca[user_id]
                save_users(users)
                save_passwords(passwords)
                save_grades(grades)
                save_eca(eca)
                print("User deleted successfully.")
            else:
                print("User ID not found.")


        if choice == "4":
            analytics_dashboard(users, grades, eca)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Try again.")


def show_grade_trends(grades):
    subjects = ["Math", "Science", "English", "History", "Art"]
    averages = [sum(grades[user_id][i] for user_id in grades) / len(grades) for i in range(5)]

    plt.bar(subjects, averages, color='skyblue')
    plt.title("Average Grades per Subject")
    plt.ylabel("Average Marks")
    plt.xlabel("Subjects")
    plt.ylim(0, 100)
    plt.show()

def show_eca_impact(grades, eca):
    user_ids = list(grades.keys())
    x = []
    y = []

    for uid in user_ids:
        if uid in eca:
            x.append(len(eca[uid]))
            y.append(sum(grades[uid]) / len(grades[uid]))

    plt.scatter(x, y, color='green')
    plt.title("ECA Involvement vs Academic Performance")
    plt.xlabel("Number of ECA Activities")
    plt.ylabel("Average Grade")
    plt.grid(True)
    plt.show()


def analytics_dashboard(users, grades, eca):
    while True:
        print("\n--- Analytics Dashboard ---")
        print("1. Grade Trends")
        print("2. ECA Impact")
        print("3. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            show_grade_trends(grades)
        elif choice == "2":
            show_eca_impact(grades, eca)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def student_menu(student):
    while True:
        print("\n--- Student Menu ---")
        print("1. View Profile")
        print("2. Update Profile")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            student.view_profile()
        elif choice == "2":
            student.update_profile()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")
