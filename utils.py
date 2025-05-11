import json
import os.path
import data.db_session as dses
from data.task_statuses import TaskStatus

def read_task(uid: str):
    with open(f'tasks/{uid}.json', encoding='utf-8') as f:
        return json.load(f)


def task_exists(uid: str):
    return os.path.isfile(f'tasks/{uid}.json')


def get_list_of_tasks():
    return [{'name': read_task(i.replace('.json', ''))['name'], 'index': i.replace('.json', '')} for i in os.listdir('tasks/')]


def get_task_status(uid, tname):
    db_sess = dses.create_session()
    return db_sess.query(TaskStatus).filter(TaskStatus.user_id == uid, TaskStatus.task == tname).first()