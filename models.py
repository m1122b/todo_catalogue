
import sql_queries

DB_FILE = "database.db"

class Todos:
    def __init__(self):
        create_projects_sql = """
        -- projects table
        CREATE TABLE IF NOT EXISTS projects (
            id integer PRIMARY KEY,
            title text NOT NULL,
            author text,
            description text,
            done BOOLEAN
        );
        """
        conn = sql_queries.create_connection(DB_FILE)
        if conn is not None:
            sql_queries.execute_sql(conn, create_projects_sql)
       

    def all(self):     
        conn = sql_queries.create_connection(DB_FILE)
        a = sql_queries.select_all(conn, "projects")
        print(a)
        
        return a

    
    def get(self, todo_id):
        conn = sql_queries.create_connection(DB_FILE)
        print(sql_queries.select_where(conn, "projects", id=todo_id))
        return sql_queries.select_where(conn, "projects", id=todo_id)
    
    
    def create(self, data):
        data.pop('csrf_token')
        print(data)
        a = list(data.values())
        print(a)
        conn = sql_queries.create_connection(DB_FILE)
        sql_queries.add_projects(conn, a)


    """
    def save_all(self):
        with open("todos.json", "w") as f:
            json.dump(self.todos, f)
    """
   
    def update(self, id, data):
        data.pop('csrf_token')
        print(data)
        conn = sql_queries.create_connection(DB_FILE)
        print(sql_queries.update(conn, "projects", id, data))
        return sql_queries.update(conn, "projects", id, data)


    """
    def update(self, id, data):
        data.pop('csrf_token')
        todo = self.get(id)
        if todo:
            index = self.todos.index(todo)
            self.todos[index] = data
            self.save_all()
            return True
        return False
    """

    
    def delete(self, id):
        conn = sql_queries.create_connection(DB_FILE)
        sql_queries.delete_where(conn, "projects", id=id)


todos = Todos()

