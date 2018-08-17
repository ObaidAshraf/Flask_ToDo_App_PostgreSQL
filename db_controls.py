import json
import psycopg2 as pg
from urllib.parse import urlparse


DATABASE_URL = "postgres://orexymdo:TOlzCH3WeUPHjqYseymDfJ4flwOj_nKI@pellefant.db.elephantsql.com:5432/orexymdo"

#urlparse.uses_netloc.append("postgre")
url = urlparse(DATABASE_URL)


def insert_task(*data):
    conn = pg.connect(database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port
    )
    cur = conn.cursor()
    sql = "INSERT INTO tasks (id, title, description, done) VALUES (" +\
          str(data[0]) + ",'" + data[1] + "','" + data[2] + "'," + str(data[3]) +")"
    cur.execute(sql)
    conn.commit()
    conn.close()

def get_all_tasks():
    data = []
    conn = pg.connect(database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port
    )
    cur = conn.cursor()
    sql = "SELECT * FROM tasks"
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [cur.rowcount, rows]


def get_task(task_id):
    data = []
    conn = pg.connect(database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port
    )
    cur = conn.cursor()
    sql = "SELECT * FROM tasks WHERE id = " + str(task_id)
    cur.execute(sql)
    rows = cur.fetchone()
    cur.close()
    conn.close()
    return [cur.rowcount, rows]


def update_task(task_id, **task_data):
    data = []
    title = task_data["title"]
    description = task_data["description"]
    done = task_data["done"]

    conn = pg.connect(database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port
    )
    cur = conn.cursor()
    sql = "SELECT * FROM tasks WHERE id = " + str(task_id)
    cur.execute(sql)
    if (cur.rowcount > 0):
        sql = "UPDATE tasks SET "
        if (title):
            sql += "title='" + title + "',"
        if (description):
            sql += "description = '" + description + "',"
        if (done):
            sql += "done = " + str(done) + ","
        sql = sql[:len(sql)-1]
        sql += " WHERE id = " + str(task_id)
        cur.execute(sql)
        res = 200
    else:
        res = 500
    cur.close()
    conn.commit()
    conn.close()
    return res


def delete_task(task_id):
    conn = pg.connect(database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port
    )
    cur = conn.cursor()
    sql = "DELETE FROM tasks WHERE id = " + str(task_id)
    cur.execute(sql)
    conn.commit()
    conn.close()


def get_max_id():
    data = []
    conn = pg.connect(database=url.path[1:],
                      user=url.username,
                      password=url.password,
                      host=url.hostname,
                      port=url.port
                      )
    cur = conn.cursor()
    sql = "SELECT COALESCE((SELECT max(id) from tasks), 0)"
    cur.execute(sql)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row