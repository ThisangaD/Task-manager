#Author: Thisanga Perera
# IIT ID : 20242008
# UoW ID : 2151959
#Submission date: 20.04.2025
#Course work - stage 03



import json 

# Creating a list to store tasks
# Each task is stored as a list: [name, description, priority, due_date]
tasks = []

# Functions for CRUD operations
def add_task():
    while True:#iterate until user input a valid task name
        name = input("\nEnter the task name: ").strip()  #get the task name  
        if name:
            break
        print("Task name cannot be empty. Please enter a task name.")     
    while True:#iterate until user input a valid task description
        description = input("Enter the task description: ").strip()  #get the task description
        if description:
            break
        print("Task description cannot be empty. Please enter a valid description.") 
    while True: #iterate until user input valid priority
        priority = str(input("Enter the task priority level (High/Medium/Low): ")).lower()   #get the task priority
        if priority in ["high", "medium", "low"]:
            break
        else:
            print("Invalid Input! Enter High/Medium/Low.")
    
    while True:  # iterate until user input the date in correct format
        due_date = input("Enter the Due date for the task (dd/mm/yyyy): ")   # get the task due date
        # Check if the date is in the correct format (dd/mm/yyyy)
        if len(due_date) == 10 and due_date[2] == '/' and due_date[5] == '/':
            day, month, year = due_date.split('/')
            # Check if day, month, and year are all digits
            if day.isdigit() and month.isdigit() and year.isdigit():
                day, month, year = int(day), int(month), int(year)
                # Check if day, month, and year values are valid
                if 1 <= month <= 12 and len(str(year)) == 4:
                    if month in [1, 3, 5, 7, 8, 10, 12] and 1 <= day <= 31:
                        break
                    elif month in [4, 6, 9, 11] and 1 <= day <= 30:
                        break
                    elif month == 2:
                        if ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)) and 1 <= day <= 29: #check for valid date in a leap year
                            break
                        elif 1 <= day <= 28:
                            break
                        else:
                            print("Invalid day for February in the given year.")
                    else:
                        print("Invalid day for the given month.")
                else:
                    print("Invalid date values. Please enter a correct month (1-12) and a four-digit year.")
            else:
                print("Invalid date. Please enter numeric values for day, month, and year.")
        else:
            print("Invalid date format. Please enter (dd/mm/yyyy).")    
    task = {"name": name,"description": description,"priority": priority,"due_date": due_date}
    tasks.append(task) #add the task to the task list
    save_tasks_to_json() # Save changes to file after updating
    print(f"Task: {name} added successfully!")


# Functions for viewing the task to be done
def view_tasks():
    if len(tasks) == 0: #check there is any task to be done at the task list
        print("\nThere is no task to be done!")
        return
    else:
        print("_____________________________Task List_______________________________")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['name']} | Priority: {task['priority']} | Due: {task['due_date']}")
        print(f"   Description: {task['description']}\n")
        print("---------------------------------------------------------------------")



def update_task():
    if len(tasks) == 0:  # Check if there are any tasks available
        print("\nNo tasks available to update!")
        return 
    
    print("\n")
    view_tasks()  # Show task list
    
    while True:
        try:
            task_num = int(input("\nEnter the task number you want to update: "))
            if 1 <= task_num <= len(tasks):  # Validate task number
                break
            else:
                print("Invalid task number! Please enter a number from the list.") #display error message
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    task = tasks[task_num - 1]
    confirm = input(f"Do you want to update task '{task['name']}'? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Task update cancelled!") 
        return

    while True: 
        print("\n______________ Choose an option to update ______________")  # Show update options
        print("1 : Task name")
        print("2 : Description")
        print("3 : Priority")
        print("4 : Due date")
        
        option_num = input("\nEnter the option number to update: ").strip()
        
        if option_num == "1":
            while True:#iterate until user input a correct task name
                new_name = input("Enter new task name: ").strip()
                if new_name:
                    task['name'] = new_name
                    break
                else:
                    print("Task name cannot be empty!Please enter a task name")

        elif option_num == "2":
            while True:#iterate until user input a valid task description
                new_description = input("Enter new task description: ").strip()
                if new_description:
                    task['description'] = new_description
                    break
                else:
                    print("Task description cannot be empty!")

        elif option_num == "3":
            while True:#iterate until user input valid priority
                priority = input("Enter the task priority level (High/Medium/Low): ").strip().lower()
                if priority in ["high", "medium", "low"]:
                    task['priority'] = priority
                    break
                else:
                    print("Invalid input! Enter High/Medium/Low.")

        elif option_num == "4":
            while True:
                due_date = input("Enter the due date (dd/mm/yyyy): ").strip()
                if len(due_date) == 10 and due_date[2] == '/' and due_date[5] == '/':
                    day, month, year = due_date.split('/')
                    if day.isdigit() and month.isdigit() and year.isdigit():
                        day, month, year = int(day), int(month), int(year)
                        if 1 <= month <= 12 and len(str(year)) == 4:
                            if month in [1, 3, 5, 7, 8, 10, 12] and 1 <= day <= 31:
                                break
                            elif month in [4, 6, 9, 11] and 1 <= day <= 30:
                                break
                            elif month == 2:
                                if ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)) and 1 <= day <= 29:
                                    break
                                elif 1 <= day <= 28:
                                    break
                                else:
                                    print("Invalid day for February in the given year.")
                            else:
                                print("Invalid day for the given month.")
                        else:
                            print("Invalid date values. Please enter a correct month (1-12) and a four-digit year.")
                    else:
                        print("Invalid date. Please enter numeric values for day, month, and year.")
                else:
                    print("Invalid date format. Please enter (dd/mm/yyyy).")
            task['due_date'] = due_date

        else:
            print("Invalid choice! Enter a number between 1-4.")
            continue  # Restart the loop if an invalid option is chosen
        
        repeat_choice = input("\nDo you want to update another field? (yes/no): ").strip().lower()
        if repeat_choice != "yes":
            break
    
    save_tasks_to_json()  # Save changes to file after updating
    print("\nTask updated successfully!")



def delete_task():
    if len(tasks) == 0:   #check there is any task to be done at the task list
        print("\nNo tasks available to Delete!")
        return 
    
    print("\n")
    view_tasks()   #show tasks list

    while True:
        try:
            task_num = int(input("\nEnter the task number you want to delete: "))
                # Check the task number is valid or not
            if 1<= task_num <= len(tasks):
                break
            else:
                print("Invalid task number! Please enter a number from the list.")
        
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    task = tasks[task_num - 1]
    confirm = input(f"Confirm! Do you want to delete task '{task['name']}'? (yes/no): ").lower() #make sure the user want to to delete or not

    if confirm != 'yes':
        print("Task deletion cancelled!")
        return
        
    tasks.pop(task_num - 1) # Delete the task from the tasks list
    save_tasks_to_json()
    print("Task deleted successfully!")

def save_tasks_to_json():
    try:
        with open("tasks.json", "w") as file:
            for task in tasks:
                json.dump(task, file)
                file.write("\n")  # write one task per line
    except:
        print("An error occurred while saving tasks.")
        
def load_tasks_from_json():
    global tasks 
    try:
        with open("tasks.json", "r") as file:
            tasks.clear()
            for line in file:
                if line.strip():  # skip empty lines
                    tasks.append(json.loads(line.strip()))
    except FileNotFoundError:
        print("No existing task file found.")
    except:
        print("An error occurred while loading tasks.")



# Function to load tasks from JSON file
def load_tasks_from_json():
    global tasks #update global tasks list
    try:
        with open("tasks.json", "r") as file:
            tasks.clear()  # Clear existing tasks in the task list before loading the file
            tasks = json.load(file)
    except FileNotFoundError:
        print("No existing task file found.") #dispay error message
    except:
        print("An error occurred while loading tasks.") #display error message


# Function to save tasks to JSON file
def save_tasks_to_json():
    try:
        with open("tasks.json", "w") as file:
            json.dump(tasks, file, indent = 2)#store the tasks in the file
            
    except:
        print("An error occurred while saving tasks.") #display error message

#the main menu 
if __name__ == "__main__":
    load_tasks_from_json()
    while True:
        print("\n=============== Task Manager ===============")  #Diplay the main choices in the task manager for user to select
        print("1. Show the tasks")
        print("2. Update a task")
        print("3. Delete a task")
        print("4. Add a task")
        print("5. Exit")
        choice = input("Select the number to do: ")
        
        if choice == "1":
            view_tasks()
        elif choice == "2":
            update_task()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            add_task()
        elif choice == "5":
            print("Exiting Task Manager. Thanks for using!") #exiting message
            break
        else:
            print("Invalid choice! Please select a valid number.") #Display error message
