import sys
import json
import os


def load_tasks():
    """If there are already tasks within the json file, load them or return an empty list"""
    if os.path.exists("task.json"):
        with open("task.json", "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_tasks(tasks):
    """Save the list of tasks to the json file"""
    with open("task.json", "w") as file:
        json.dump(tasks, file)


def add_task(description):
    """Add a task to the json file using other created functions"""
    tasks = load_tasks()

    # get the id for the next task 
    # each task will have an id assinged to it for easy access
    if tasks:
        new_id = tasks[-1]["id"] + 1
    else:
        new_id = 1

    # format for json
    new_task = {
        "id": new_id,
        "description": description
    }

    # add task to the list of tasks and then save by dumping
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")


def update_task(task_id, description):
    """Update an existing task in the json file"""
    tasks = load_tasks()
    updated = False

    # have to search through the list using a for loop since we didn't implement tasks as a dictionary
    # searches list with for loop looking for the task id's description we want to update
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            updated = True
            break
    
    if updated:
        save_tasks(tasks)
        print(f"Task (ID: {task_id}) updated successfully")
    else:
        print(f"No task found at (ID: {task_id})")


def delete_task(task_id):
    """Deletes a task from the json if the given task id exists"""
    tasks = load_tasks()

    # new list that doesn't have the deleted task
    new_tasks = []
    for task in tasks:
        if task["id"] != task_id:
            new_tasks.append(task)

    if len(tasks) == len(new_tasks): # means nothing was deleted because they are same length
        print(f"No task found with id: {task_id}")
    else:
        save_tasks(new_tasks)
        print(f"Task (ID: {task_id}) deleted successfully")


def handle_command(command, arguments):
    """Handles commands that could be used (add, delete, update) and more"""
    if command == "add":
        if arguments:
            description = " ".join(arguments)
            add_task(description)
        else:
            print("nothing was added; consider the correct format")
    elif command == "update":
        if arguments:
            try:
                task_id = int(arguments[0])
                description = " ".join(arguments[1:])
                update_task(task_id, description)
            except ValueError:
                print("Invalid ID. Must be a number")
        else:
            print("task was not updated; see readme for instructions on how to update")
    elif command == "delete":
        if arguments:
            try:
                task_id = int(arguments[0])
                delete_task(task_id)
            except ValueError:
                print("Invalid ID. Must be a number")
        else:
            print("nothing was deleted")
    else:
        print(f"Unknown command: {command}")


def parse_command():
    """Parses the command line by using sys.argv. The first string should be 
    the command followed by its arguments"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        arguments = sys.argv[2:]
        return command, arguments
    else:
        print("no commands to parse")
        sys.exit(1)


def main():
    command, arguments = parse_command()
    handle_command(command, arguments)

  
if __name__ == "__main__":
    main()
