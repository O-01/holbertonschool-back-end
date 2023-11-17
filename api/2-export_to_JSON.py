#!/usr/bin/python3
"""
Using what you did in the task #0, extend your Python script to export data in
the JSON format.
Requirements:
-Records all tasks that are owned by this employee
-Format must be:
{
    "USER_ID":
    [
        {
            "task": "TASK_TITLE",
            "completed": TASK_COMPLETED_STATUS,
            "username": "USERNAME"
        },
        {
            "task": "TASK_TITLE",
            "completed": TASK_COMPLETED_STATUS,
            "username": "USERNAME"
        },
        et. al.
    ]
}
-File name must be: USER_ID.json
"""
import json
import sys
import urllib.request


def export_to_JSON(user_id):
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
        person['username'] for person in users if person['id'] == user_id
    )
    found = next(
        todo['userId'] for todo in todos if todo['userId'] == user_id
    )
    employee_task_data = {
        found: list(
            {
                'task': todo['title'],
                'completed': todo['completed'],
                'username': employee_name
            }
            for todo in todos if todo['userId'] == user_id
        )
    }
    with open(f'{user_id}.json', 'w') as json_file:
        json.dump(employee_task_data, json_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Please input only the requested employee's ID number")
    elif sys.argv[1].isdigit() is False:
        sys.exit("Please input employee's ID number (whole digit)")
    else:
        user_id = int(sys.argv[1])
    export_to_JSON(user_id)
