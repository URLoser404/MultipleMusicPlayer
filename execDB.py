from sqlite3 import *

conn = connect('music.db')
cursor = conn.cursor()

conn.execute("Drop table playlist")
conn.commit()

conn.execute('''Create table if not exists playlist
                    (id integer primary key not null,
                    songName text not null,
                    url text not null,
                    type text not null)''')
conn.commit()

for i in range(20):
    conn.execute(f"insert into playlist values({i},'{i+1}','{i+2}','{i+3}')")
conn.commit()


def exec(command):
    def dict_factory(cursor, row):
        dict = {}
        for idx, col in enumerate(cursor.description):
            dict[col[0]] = row[idx]
        return dict
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(command)
    return cursor.fetchall()









# cursor = conn.execute("select * from playlist")

# for row in cursor:
#     print(row)
