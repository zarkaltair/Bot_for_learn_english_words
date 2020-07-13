import sqlite3


def ensure_connection(func):
    '''Decorator for connection to DBMS
       open connection execute function
       close connection
    '''
    def inner(*args, **kwargs):
        with sqlite3.connect('database.db') as conn:
            print('Connecting to database...')
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner

@ensure_connection
def init_tables(conn):
    c = conn.cursor()

    # c.execute('''CREATE TABLE IF NOT EXISTS users(
    #                 id        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    #                 user_id   INTEGER NOT NULL,
    #                 date_time DATETIME DEFAULT CURRENT_TIMESTAMP)
    #           ''')

    c.execute('''CREATE TABLE IF NOT EXISTS user_words(
                    id        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    user_id   INTEGER NOT NULL,
                    word      TEXT UNIQUE ON CONFLICT IGNORE,
                    translate TEXT NOT NULL)
              ''')

    # save all changes
    conn.commit()


@ensure_connection
def add_word(conn, user_id: int, word: str, translate: str):
    c = conn.cursor()
    c.execute('INSERT INTO user_words (user_id, word, translate) VALUES (?,?,?)', (user_id, word, translate))
    conn.commit()


@ensure_connection
def count_words(conn, user_id: int):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_words WHERE user_id = ?', (user_id, ))
    (res, ) = c.fetchone()
    return res


@ensure_connection
def list_all_words(conn, user_id: int, limit: int=10):
    c = conn.cursor()
    c.execute('SELECT * FROM user_words WHERE user_id = ? ORDER BY id LIMIT ?', (user_id, limit))
    return c.fetchall()


if __name__ == '__main__':
    init_tables()

    add_word(user_id=1, word='learn', translate='учить')
    add_word(user_id=1, word='learn', translate='учить')
    add_word(user_id=1, word='insted of', translate='вместо')
    add_word(user_id=1, word='otherwise', translate='иначе')

    r = count_words(user_id=252027450)
    print(f'{r} words in database')

    r = list_all_words(user_id=252027450)
    for i in r:
        print(i)
