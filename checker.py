import multiprocessing
import sqlalchemy
import io
import sys
from utils import *
from data.users import User
from data.task_statuses import TaskStatus
import data.db_session as dses


def set_status(uid, tname, status, info = None, session=None):
    session = dses.create_session()

    if not session.query(TaskStatus).filter(TaskStatus.user_id == uid, TaskStatus.task == tname).first():
        ts = TaskStatus()
        ts.status = status
        ts.info = info
        ts.user_id = uid
        ts.task = tname

        session.add(ts)
        session.commit()
    else:
        session.execute(sqlalchemy.update(TaskStatus).where(TaskStatus.user_id == uid, TaskStatus.task == tname).values(status=status, info=info))
        session.commit()


def give_rating(uid, rating):
    session = dses.create_session()

    session.execute(sqlalchemy.update(User).where(User.id == uid).values(rating=User.rating + rating))
    session.commit()


def suit(uid, tname, code, cases, rating, queue):
    for case in cases:
        _input = '\n'.join(case['input'])
        output = case['output']

        stdin = io.StringIO(_input)
        sys.stdin = stdin

        stdout = io.StringIO()
        sys.stdout = stdout

        try:
            exec(code)
        except Exception as e:
            queue.put('ERROR')
            queue.put(str(e))
            return
        
        result = stdout.getvalue()

        if result.endswith("\n"):
            result = result[:-1]

        if result != output:
            queue.put('ERROR')
            queue.put(f"""Ответы не сошлись
                              Введенный данные:
                              {_input}
                              Ожидаемый вывод:
                              {output}
                              Вывод:
                              {result}""")
            return

    queue.put('SUCCESS')
    queue.put('')


def run(uid, tname, code):
    set_status(uid, tname, 'CHECK')
    task = read_task(tname)

    queue = multiprocessing.Queue()

    proc = multiprocessing.Process(target=suit, args=[uid, tname, code, task['cases'], task['rating'], queue])
    proc.start()
    proc.join(task['timeout'])
    if proc.is_alive():
        return set_status(uid, tname, 'ERROR', f'Превышено время выполнения задачи ({task['timeout']} сек.)')
    
    status = queue.get()
    info = queue.get()

    if status == 'SUCCESS':
        give_rating(uid, task['rating'])
        set_status(uid, tname, status)
    else:
        set_status(uid, tname, status, info)