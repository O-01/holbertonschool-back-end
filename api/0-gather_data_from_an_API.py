#!/usr/bin/python3
"""
Write a Python script that, using this REST API, for a given employee ID,
returns information about his/her TODO list progress.
Requirements:
-You must use urllib or requests module
-The script must accept an integer as a parameter, which is the employee ID
-The script must display on the standard output the employee TODO list progress
in this exact format:
--First line:
Employee EMPLOYEE_NAME is done with tasks
(NUMBER_OF_DONE_TASKS/TOTAL_NUMBER_OF_TASKS):
---EMPLOYEE_NAME: name of the employee
---NUMBER_OF_DONE_TASKS: number of completed tasks
---TOTAL_NUMBER_OF_TASKS: total number of tasks, which is the sum of completed
and non-completed tasks
--Second and N next lines display the title of completed tasks: TASK_TITLE (
with 1 tabulation and 1 space before the TASK_TITLE)
"""
import json
import sys
import urllib.request


def gather_data_from_an_API(user_id):
    """ Gathers todo list data for specified user """
    todos_in = urllib.request.urlopen(
        'https://jsonplaceholder.typicode.com/todos'
    ).read()
    todos = json.loads(todos_in.decode('utf-8'))
    users_in = urllib.request.urlopen(
        'https://jsonplaceholder.typicode.com/users'
    ).read()
    users = json.loads(users_in.decode('utf-8'))
    employee_name = next(
        person['name'] for person in users if person['id'] == user_id
    )
    done = sum(
        1 if todo['userId'] == user_id and todo['completed'] is True else 0
        for todo in todos
    )
    total_tasks = sum(1 if todo['userId'] == user_id else 0 for todo in todos)
    dones = list(
        filter(
            lambda confirmed: confirmed,
            (
                todo['title']
                for todo in todos
                if todo['userId'] == user_id and todo['completed'] is True
            )
        )
    )
    print(
        f'Employee {employee_name} is done with tasks({done}/{total_tasks}):'
    )
    [
        print(f'\t {task}')
        for task in dones
    ]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Please input only the requested employee's ID number")
    elif sys.argv[1].isdigit() is False:
        sys.exit("Please input employee's ID number (whole digit)")
    else:
        user_id = int(sys.argv[1])
    gather_data_from_an_API(user_id)
