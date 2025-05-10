import json
import os.path

def read_task(uid: str):
    with open(f'tasks/{uid}.json', encoding='utf-8') as f:
        return json.load(f)


def task_exists(uid: str):
    return os.path.isfile(f'tasks/{uid}.json')
