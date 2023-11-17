#!/usr/bin/python3
"""
Using what you did in the task #0, extend your Python script to export data in
the JSON format.
Requirements:
-Records all tasks from all employees
-Format must be:
{
    "USER_ID 1":
    [
        {
            "username": "USERNAME",
            "task": "TASK_TITLE",
            "completed": TASK_COMPLETED_STATUS}
        },
        {
            "username": "USERNAME",
            "task": "TASK_TITLE",
            "completed": TASK_COMPLETED_STATUS
        },
        et al.
    ],
    "USER_ID 2":
    [
        ...
    ],
    et al.
}
-File name must be: todo_all_employees.json
"""
import json
import sys
import urllib.request


def dictionary_of_list_of_dictionaries():
    """ Gathers todo list data for all users & exports to JSON file """
    try:
        todos_in = urllib.request.urlopen(
            'https://jsonplaceholder.typicode.com/todos',
            timeout=30
        ).read()
        todos = json.loads(todos_in.decode('utf-8'))
        users_in = urllib.request.urlopen(
            'https://jsonplaceholder.typicode.com/users',
            timeout=30
        ).read()
        users = json.loads(users_in.decode('utf-8'))
    except urllib.request.URLError as url_error:
        print('ERROR')
        if hasattr(url_error, 'code'):
            print(f' : {url_error.code}')
        if hasattr(url_error, 'reason'):
            print(f' : {url_error.reason}')
        sys.exit('Please try again.')
    employee_task_data = {
        user_id['userId']: list(
            {
                'username': next(
                    person['username']
                    for person in users if person['id'] == todo['userId']
                ),
                'task': todo['title'],
                'completed': todo['completed'],
            }
            for todo in todos if todo['userId'] == user_id['userId']
        )
        for user_id in todos
    }
    with open('todo_all_employees.json', 'w') as json_file:
        json.dump(employee_task_data, json_file)


if __name__ == '__main__':
    dictionary_of_list_of_dictionaries()
