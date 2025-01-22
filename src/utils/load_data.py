import json
import random
import ast

def load_jsonl(data_path):
    data = []
    with open(data_path, mode='r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data


def get_random_tasks(instruction_type, k=1):
    # Split the string into lines and filter out any empty lines
    lines = instruction_type.strip().split('\n')
    
    # Prepare an empty list to store tasks
    tasks = []
    
    # Loop through the lines in pairs (name and description)
    for i in range(0, len(lines), 2):
        task_name = lines[i].split(':')[1].strip().strip('"')
        task_description = lines[i + 1].split(':')[1].strip().strip('"')
        
        # Create a task dictionary and append it to the list
        tasks.append({
            "name": task_name,
            "description": task_description
        })
    
    # Randomly select k tasks from the list of tasks
    selected_tasks = random.sample(tasks, k)

    tasks_description = ""
    for task in selected_tasks:
        tasks_description += f"Task Name: {task['name']}\nDescription: {task['description']}\n\n"
    return tasks_description

import os

def get_relative_jsonl_paths(folder_path):
    # List to store the relative paths of all *.jsonl files
    relative_paths = []

    # Iterate through all files in the directory and subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.jsonl'):  # Check if the file is a .jsonl file
                # Get the relative path
                relative_path = os.path.relpath(os.path.join(root, file), folder_path)
                relative_paths.append(relative_path)
    return relative_paths
