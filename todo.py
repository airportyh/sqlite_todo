#!/usr/bin/env python3
import sqlite3
import sys

db = sqlite3.connect("todo.db")
db.row_factory = sqlite3.Row

db.execute("""
create table if not exists task (
    id integer primary key,
    name text,
    complete integer
);
""")

db.commit()

cmd = sys.argv[1]

if cmd == 'list':
    tasks = db.execute('select * from task').fetchall()
    for task in tasks:
        status = '▢'
        if task['complete']:
            status = '✓'
        print('%d. %s %s' % (task['id'], task['name'], status))
elif cmd == 'add':
    task_name = sys.argv[2]
    db.execute('insert into task (name, complete) values (?, 0)', (task_name,))
    db.commit()
elif cmd == 'done':
    task_id = sys.argv[2]
    db.execute('update task set complete = 1 where id = ?', (task_id,))
    db.commit()
elif cmd == 'undone':
    task_id = sys.argv[2]
    db.execute('update task set complete = 0 where id = ?', (task_id,))
    db.commit()
elif cmd == 'remove':
    task_id = sys.argv[2]
    db.execute('delete from task where id = ?', (task_id,))
    db.commit()
else:
    print('Unknown command %s' % cmd)
    exit(1)
    
    