#!/usr/bin/python3
"""
Using what you did in the task #0, extend your Python script to export data in
the CSV format.
Requirements:
-Records all tasks that are owned by this employee
-Format must be: "USER_ID","USERNAME","TASK_COMPLETED_STATUS","TASK_TITLE"
-File name must be: USER_ID.csv
"""
import csv
import json
import sys
import urllib.request


def export_to_CSV(user_id):
    """ Gathers todo list data for specified user & exports to CSV file """
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
        employee_name = next(
            person['username'] for person in users if person['id'] == user_id
        )
    except urllib.request.URLError as url_error:
        print('ERROR')
        if hasattr(url_error, 'code'):
            print(f' : {url_error.code}')
        if hasattr(url_error, 'reason'):
            print(f' : {url_error.reason}')
        sys.exit('Please try again.')
    except StopIteration:
        sys.exit("ID not found.")
    owned_tasks = {
        todo['title']: todo['completed']
        for todo in todos if todo['userId'] == user_id
    }
    with open(f'{user_id}.csv', 'w') as csv_file:
        csv_outfile = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        [
            csv_outfile.writerow([user_id, employee_name, done, task])
            for task, done in owned_tasks.items()
        ]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Please enter only the requested employee's ID number")
    elif sys.argv[1].isdigit() is False:
        sys.exit("Please enter employee's ID number (whole digit)")
    else:
        user_id = int(sys.argv[1])
    export_to_CSV(user_id)
