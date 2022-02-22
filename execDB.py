from sqlite3 import *

conn = connect('music.db')
cursor = conn.cursor()



def main():
    conn.execute("drop table playlist")
    conn.commit()

    conn.execute('''Create table if not exists playlist(
                        id integer primary key AUTOINCREMENT not null,
                        title text not null,
                        author text not null,
                        duration text not null,
                        url text not null,
                        img text not null,
                        music text not null,
                        played boolean not null
                    )''')
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


if __name__ == "__main__":
    conn = connect('music.db')
    conn.execute("delete from playlist")
    print(exec("select * from playlist"))

