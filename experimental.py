import csv
import os
from datetime import date, timedelta

# Function to create or update CSV file
def update_csv(employee_duties, employees_list):
    days_count = 6
    filename = "~/Desktop/employee_duties.csv"
    filepath = os.path.expanduser(filename)

    # Create date range for the next 'days_count' days
    date_range = [date.today() + timedelta(days=i) for i in range(days_count)]
    date_columns = [day.strftime("%Y-%m-%d") for day in date_range]

    file_exists = os.path.isfile(filepath)

    # Check if file exists
    if not file_exists:
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            header_row = ["Employee"] + date_columns
            writer.writerow(header_row)
            for emp in employees_list:
                writer.writerow([emp] + [""] * days_count)
        print(f"File '{filename}' created successfully.")
    else:
        with open(filepath, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        with open(filepath, mode='w', newline='') as file:
            headers = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            for row in rows:
                emp = row['Employee']
                if emp in employee_duties:
                    for i in range(days_count - 1, 0, -1):
                        row[date_columns[i]] = row[date_columns[i - 1]]
                    row[date_columns[0]] = employee_duties[emp]
                writer.writerow(row)
        print(f"File '{filename}' updated successfully.")

# Function to assign duties to employees
def assign_duties(employees_list):
    duties = ['Stow-Pick', 'Pick-Stow', 'Loading-Induct', 'Induct-Loading','Push-Stow','Stow-Diverter']
    employees = {emp: duties[i % len(duties)] for i, emp in enumerate(employees_list)}
    return employees

# Function to rotate duties for the next day
def rotate_duties(employees):
    duties = ['Stow-Pick', 'Pick-Stow', 'Loading-Induct', 'Induct-Loading','Push-Stow','Stow-Diverter']
    for emp, duty in employees.items():
        current_index = duties.index(duty)
        next_index = (current_index + 1) % len(duties)
        employees[emp] = duties[next_index]
    return employees

# Main function
def main():
    employees_list = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eva', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack',
               'Katherine', 'Leo', 'Mia', 'Nathan', 'Olivia', 'Peter', 'Quinn', 'Rachel', 'Samuel', 'Tina',
               'Ursula', 'Victor', 'Wendy', 'Xander', 'Yvonne', 'Zane', 'Emma', 'David', 'Sophia', 'Liam',
               'Ava', 'Noah', 'Isabella', 'James', 'Mia']  # Add your employee names here
    employees = assign_duties(employees_list)

    for _ in range(6):
        update_csv(employees, employees_list)
        employees = rotate_duties(employees)

    print("Duties rotated for the next six days.")

if __name__ == "__main__":
    main()
