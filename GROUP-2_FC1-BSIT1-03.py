import datetime

students = []
attendance_records = []

TEACHER_PASSWORD = "teacher123"


def validate_input(prompt_text):
    while True:
        value = input(prompt_text).strip()

        if not value:
            print("Input cannot be empty. Please try again.")
        else:
            return value


def validate_student_id():
    while True:
        student_id = validate_input("Enter Student ID: ")

        if (
            all(char.isdigit() or char == "-" for char in student_id)
            and any(char.isdigit() for char in student_id)
        ):
            return student_id

        print("Invalid Student ID. Please use numbers and hyphens only.")


def validate_student_name():
    while True:
        name = validate_input("Enter Student Name: ")
        
        if not all(char.isalpha() or char.isspace() or char=="," for char in name):
            print("Invalid Student Name. Please use letters and spaces only.")
        elif not any(char.isalpha() for char in name):
            print("Name must contain letters.")
        else:
            return name




def validate_date():
    while True:
        date = input("Enter Date (MM/DD/YYYY): ").strip()
        parts = date.split("/")

        if len(parts) != 3:
            print("Invalid date format. Use MM/DD/YYYY.")
            continue

        month_text, day_text, year_text = parts

        if not (
            month_text.isdigit()
            and day_text.isdigit()
            and year_text.isdigit()
        ):
            print("Invalid date. Please use numbers only.")
            continue

        if (
            len(month_text) != 2
            or len(day_text) != 2
            or len(year_text) != 4
        ):
            print("Use the exact format MM/DD/YYYY.")
            continue

        try:
            entered_date = datetime.datetime.strptime(
                date, "%m/%d/%Y"
            ).date()
        except ValueError:
            print("Invalid date. Please enter a valid calendar date.")
            continue

        today = datetime.date.today()

        if entered_date != today:
            print("Invalid date. Please enter today's date")
            continue

        return entered_date.strftime("%m/%d/%Y")




def find_student(student_list, student_id):
    for student in student_list:
        if student["id"] == student_id:
            return student
    return None


def add_student(student_list):
    print("\n--- ADD STUDENT ---")

    while True:
        student_id = validate_student_id()

        if find_student(student_list, student_id):
            print("This Student ID already exists. Please enter a different one.")
        else:
            break

    student_name = validate_student_name()

    student_list.append({"id": student_id, "name": student_name})
    print("Student added successfully!")


def mark_attendance(student_list, attendance_list, student_id, date, status):
    student = find_student(student_list, student_id)

    if not student:
        return "not_found"

    for record in attendance_list:
        if record["id"] == student_id and record["date"] == date:
            return "already_marked"

    attendance_list.append({
        "id": student_id,
        "name": student["name"],
        "date": date,
        "status": status
    })

    return "success"


def mark_attendance_for_date(student_list, attendance_list):
    print("\n--- MARK ATTENDANCE ---")

    if not student_list:
        print("No students registered yet.")
        return

    date = validate_date()

    print("\nStatus options: present / absent / late")

    for student in student_list:
        print("\nStudent ID:", student["id"])
        print("Student Name:", student["name"])

        while True:
            status = validate_input("Enter status: ").lower()

            if status in ["present", "absent", "late"]:
                break

            print("Invalid status.")

        result = mark_attendance(
            student_list, attendance_list, student["id"], date, status
        )

        if result == "success":
            print("Attendance marked successfully!")
        elif result == "already_marked":
            print("Attendance for this student is already marked for this date.")
        else:
            print("Student ID not found.")


def view_students(student_list):
    print("\n--- STUDENT LIST ---")

    if not student_list:
        print("No students found.")
        return

    print("-" * 45)
    print(f"{'Student ID':<15}{'Name':<30}")
    print("-" * 45)

    for student in student_list:
        print(f"{student['id']:<15}{student['name']:<30}")

    print("-" * 45)


def generate_summary(student_list, attendance_list):
    print("\n--- ATTENDANCE SUMMARY ---")

    if not student_list:
        print("No student records available.")
        return

    if not attendance_list:
        print("No attendance records available.")
        return

    print("-" * 70)
    print(f"{'ID Number':<15}{'Student Name':<25}{'Date':<15}{'Status':<15}")
    print("-" * 70)

    for record in attendance_list:
        print(
            f"{record['id']:<15}{record['name']:<25}"
            f"{record['date']:<15}{record['status']:<15}"
        )

    print("-" * 70)


def view_my_attendance(student_list, attendance_list):
    print("\n--- MY ATTENDANCE ---")

    student_id = validate_student_id()
    student = find_student(student_list, student_id)

    if not student:
        print("Student ID not found. Please ask your teacher to add you.")
        return

    my_records = [r for r in attendance_list if r["id"] == student_id]

    print(f"\nStudent: {student['name']} ({student['id']})")

    if not my_records:
        print("No attendance records yet.")
        return

    print("-" * 30)
    print(f"{'Date':<15}{'Status':<15}")
    print("-" * 30)

    for record in my_records:
        print(f"{record['date']:<15}{record['status']:<15}")

    print("-" * 30)

    present = sum(1 for r in my_records if r["status"] == "present")
    late = sum(1 for r in my_records if r["status"] == "late")
    absent = sum(1 for r in my_records if r["status"] == "absent")
    print(f"Present: {present}  Late: {late}  Absent: {absent}")


def teacher_menu():
    password = input("Enter teacher password: ")

    if password != TEACHER_PASSWORD:
        print("Wrong password.")
        return

    while True:
        print("\n==============================")
        print("          TEACHER MENU")
        print("==============================")
        print("1. Add Student")
        print("2. Mark Attendance")
        print("3. View Student List")
        print("4. Generate Attendance Summary")
        print("5. Log Out")
        print("==============================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            mark_attendance_for_date(students, attendance_records)
        elif choice == "3":
            view_students(students)
        elif choice == "4":
            generate_summary(students, attendance_records)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


def student_menu():
    while True:
        print("\n==============================")
        print("          STUDENT MENU")
        print("==============================")
        print("1. View My Attendance")
        print("2. Back")
        print("==============================")

        choice = input("Enter your choice (1-2): ").strip()

        if choice == "1":
            view_my_attendance(students, attendance_records)
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


def main():
    while True:
        print("\n==============================")
        print("  ATTENDANCE MONITORING SYSTEM")
        print("==============================")
        print("1. Teacher")
        print("2. Student")
        print("3. Exit")
        print("==============================")

        choice = input("Who's using the system? (1-3): ").strip()

        if choice == "1":
            teacher_menu()
        elif choice == "2":
            student_menu()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 3.")


if __name__ == "__main__":
    main()
    