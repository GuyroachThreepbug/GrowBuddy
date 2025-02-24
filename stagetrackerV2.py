# Write your code here :-)
from datetime import timedelta, datetime
import datetime
import json
from json import JSONEncoder
import os


STAGES = {"Baby" : 14,
        "Green" : 21,
        "Oven" : 32,
        }

notYET = {"more_time" : 7,
        "almost" : 5,
        "b_patient" : 2,
        }



def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()

def parse_date(date_str):
    return datetime.datetime.fromisoformat(date_str)

def view_jobs():
    print("\nCurrent jobs:")
    if not pending:
        print("Empty nest!")
        return
    for job in pending:
        print(f"Name: {job['name']}, Stage: {job['stage']}")
        print(f"Start Date: {job['start date']}")
        print(f"Check Date: {job['check-in']} days from {job['maintenance date']}")
        print(f"Maintenance Date: {job['maintenance date']}")
        print("-" * 30)

def check_schedules():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    for job in pending:
        check_start_date = job["maintenance date"] - timedelta(days=job["check-in"])
        if check_start_date <= today <= job["maintenance date"]:
            print(f"Reminder: Check '{job['name']}' daily until {job['maintenance date'].strftime('%Y-%m-%d')}")
        elif today == job["maintenance date"]:
            print(f"Reminder: Perform maintenance for '{job['name']}' today!")

def save_to_file(data, file_path="stageData.json"):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4, default=default)
    print("Data saved to stageData.json.")

def load_from_file(file_path="stageData.json"):
    if os.path.exists(file_path):  # Check if the file exists
        with open(file_path, "r") as file:
            data = json.load(file)
            for job in data:
                job["start date"] = parse_date(job["start date"])
                job["maintenance date"] = parse_date(job["maintenance date"])
                return data
    return []

pending = load_from_file()

def add_job():
    print("\nAvailable Stages:")
    for idx, stage in enumerate(STAGES.keys(), start=1):
        print(f"{idx}. {stage} ({STAGES[stage]} days)")

    stage_choice = int(input("\nEnter the number for the stage: "))

    use_today = input("Start today? (y/n): ").strip().lower()
    if use_today == "y":
        start_date = datetime.datetime. today()
        print(f"Using today's date: {start_date.strftime('%Y-%m-%d')}")
    else:
        start_date_str = input("Enter the start date (YYYY-MM-DD): ")
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please try again.")
            return

    nickname = input("Enter nickname: ")
    stage_name = list(STAGES.keys())[stage_choice - 1]
    duration = STAGES[stage]
    check_window = int(input(f"Enter how many days before {duration} days to start checking daily: "))

    maintenance_date = start_date + timedelta(days=duration)
    check_start_date = maintenance_date - timedelta(days=check_window)


    new_job = {"name": nickname,
        "stage": stage_name,
        "start date": start_date,
        "maintenance date": maintenance_date,
        "check-in": check_window}

    pending.append(new_job)
    save_to_file(pending)
    print(f"\njob {nickname} added successfully!")

def main():
    print("Welcome to the Grow Tracker!")
    while True:
        print("\n1. Add a new job")
        print("2. View Jobs")
        print("3. Check Schedule")
        print("x. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_job()
        elif choice == "2":
            view_jobs()
        elif choice == "3":
            check_schedules()
        elif choice == "x":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()