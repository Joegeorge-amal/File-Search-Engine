import sqlite3

db_path = 'filesearch.db'

def connection():
    c = sqlite3.connect(db_path, timeout=30)
    c.row_factory =sqlite3.Row
    return c

def create():
    c = connection()
    c.execute("Create table if not exists files(id integer primary key autoincrement, filename text not null, path text not null, filetype text, content text)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_filename ON files(filename)")
    c.commit()
    c.close()

def insert(c, filename, path, filetype, content):
    try:
        c.execute("insert or ignore into files(filename, path, filetype, content) values (?, ?, ?, ?)",(filename, path, filetype, content))
    except Exception as E:
        print(f"Error Inserting {path}: {E}")

def update(path, content):
    c = connection()
    c.execute("Update files set content = ? where path = ?",(content, path))
    c.commit()
    c.close()

def delete(path):
    c = connection
    c.execute("delete from files where path = ?",(path))
    c.commit()
    c.close()

def search(query):
    c = connection()
    like = f"%{query}%"
    result = c.execute('''select filename, path, filetype, 
                                case when content like ? then 1 else 0 end as content_match
                        from files where filename like ? or content like ?
                        order by content_match desc, filename ASC limit 100''',(like,like,like)).fetchall
    c.close()
    return [dict(r) for r in result]

def get_total():
    c = connection()
    count = c.execute("select count(*) from files").fetchone()[0]
    c.close()
    return count