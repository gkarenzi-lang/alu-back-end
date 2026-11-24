#!/usr/bin/python3
"""Solves tasks 0-3 in one go.

Usage:
    ./all_tasks.py EMPLOYEE_ID   -> progress on stdout, EMPLOYEE_ID.csv,
                                    EMPLOYEE_ID.json, todo_all_employees.json
    ./all_tasks.py               -> only todo_all_employees.json
"""
import csv
import json
import requests
import sys

BASE = "https://jsonplaceholder.typicode.com"


def task0_progress(user, todos):
    """Task 0: print TODO progress."""
    done = [t for t in todos if t.get("completed")]
    print("Employee {} is done with tasks({}/{}):".format(
        user.get("name"), len(done), len(todos)))
    for t in done:
        print("\t {}".format(t.get("title")))


def task1_csv(user_id, user, todos):
    """Task 1: export to USER_ID.csv."""
    with open("{}.csv".format(user_id), "w", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for t in todos:
            writer.writerow([user_id, user.get("username"),
                             str(t.get("completed")), t.get("title")])


def task2_json(user_id, user, todos):
    """Task 2: export to USER_ID.json."""
    data = {user_id: [{"task": t.get("title"),
                       "completed": t.get("completed"),
                       "username": user.get("username")} for t in todos]}
    with open("{}.json".format(user_id), "w") as f:
        json.dump(data, f)


def task3_all():
    """Task 3: export every employee to todo_all_employees.json."""
    users = requests.get("{}/users".format(BASE)).json()
    todos = requests.get("{}/todos".format(BASE)).json()
    data = {}
    for u in users:
        data[str(u.get("id"))] = [
            {"username": u.get("username"),
             "task": t.get("title"),
             "completed": t.get("completed")}
            for t in todos if t.get("userId") == u.get("id")]
    with open("todo_all_employees.json", "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        uid = sys.argv[1]
        user = requests.get("{}/users/{}".format(BASE, uid)).json()
        todos = requests.get("{}/todos".format(BASE),
                             params={"userId": uid}).json()
        task0_progress(user, todos)
        task1_csv(uid, user, todos)
        task2_json(uid, user, todos)
    task3_all()
