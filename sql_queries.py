
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # conn.row_factory = sqlite3.Row
        print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
        return conn
    except Error as e:
        print(e)
    
    return conn


def execute_sql(conn, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
        print(f"Executed sql to {conn} and {sql}, sqlite version: {sqlite3.version}")
    except Error as e:
        print(e)
    conn.close()


def add_projects(conn, projects):
    """Create a new todo into the todos table
    :param conn:
    :param projects:
    :return: projekt id
    """

    sql = """INSERT INTO projects(title, author, description, done)
            VALUES(?,?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, projects)
    conn.commit()
    return cur.lastrowid


def add_task(conn, task):
    """Create a new task into the tasks table
    :param conn:
    :param task:
    :return: task id
    """

    sql = """INSERT INTO tasks(projekt_id, nazwa, opis, status, start_date, end_date)
            VALUES(?,?,?,?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid


def select_task_by_status(conn, status):
    """Query tasks by priority
    :param conn: the Connection object
    :param status:
    :return:
    """
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE status=?", (status,))

    rows = cur.fetchall()
    return rows


def select_all(conn, table):
    """Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    
    rows = cur.fetchall()
    return rows


def select_where(conn, table, **query):
    """Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param table: table name
    :param query: dict of attributes and values
    :return:
    """
    # conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
        
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
    
    rows = cur.fetchall()
    return rows


def update(conn, table, id, data):
    """update status, begin_date, and end date of a task
    :param conn:
    :param table: table name
    :param id: row id
    :param data: 
    :return:
    """

    parameters = [f"{k} = ?" for k in data.keys()]
    print(parameters)
    parameters2 = ", ".join(parameters)
    print(parameters2)
    values = tuple(v for v in data.values())
    print(values)
    values2 = values + (id, )
    print(values2)

    sql = f''' UPDATE {table}
                SET {parameters2}
                WHERE id = ?'''
    print(sql)
    try:
        cur = conn.cursor()
        print(cur.execute(sql, values2))
        cur.execute(sql, values2)
        conn.commit()
        print("UPDATE OK")
    except sqlite3.OperationalError as e:
        print(e)


def delete_where(conn, table, **kwargs):
    """Delete from table where attributes from
    :param conn:  Connection to the SQLite database
    :param table: table name
    :param kwargs: dict of attributes and values
    :return:
   """

    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Deleted")


def delete_all(conn, table):
    """Delete all rows from table
    :param conn: Connection to the SQLite database
    :param table: table name
    :return:
    """
    
    sql = f'DELETE FROM {table}'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Deleted")


if __name__ == "__main__":

    create_projects_sql = """
    -- projects table
    CREATE TABLE IF NOT EXISTS projects (
        id integer PRIMARY KEY,
        nazwa text NOT NULL,
        start_date text,
        end_date text
    );
    """

    create_tasks_sql = """
    -- zadanie table
    CREATE TABLE IF NOT EXISTS tasks (
        id integer PRIMARY KEY,
        projekt_id integer NOT NULL,
        nazwa VARCHAR(250) NOT NULL,
        opis TEXT,
        status VARCHAR(15) NOT NULL,
        start_date text NOT NULL,
        end_date text NOT NULL,
        FOREIGN KEY (projekt_id) REFERENCES projects (id)
    );
    """
    
    db_file = "database.db"

    conn = create_connection(db_file)
    
    if conn is not None:
        execute_sql(conn, create_projects_sql)
        execute_sql(conn, create_tasks_sql)
        task = (2, "Rozdział 2","Do Powtórki z angielskiego","Wykonane" , "2020-05-11 00:00:00", "2020-05-13 00:00:00")
        tas_id = add_task(conn, task)
        print(f"Last number of task {tas_id}")
        # conn.close()
    
    print(select_all(conn, "projects"))
    print('/')
    print(select_all(conn, "tasks"))
    print('/')
    print(select_where(conn, "tasks", projekt_id=2))
    print('/')
    print(select_where(conn, "projects", id=10))

    # updated 
    print('/')
    print(select_where(conn, "tasks", id=2))

    update(conn, "tasks", 2, status="started")
    update(conn, "tasks", 2, stat="started")

    print('/')
    print(select_where(conn, "tasks", id=2))

    # delete
    print('/')
    print(select_all(conn, "tasks"))
    delete_where(conn, "tasks", id=3)
    # delete_all(conn, "tasks")
    print('/')
    print(select_all(conn, "tasks"))




