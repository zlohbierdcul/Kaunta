import psycopg2

def start_connection():
    con = psycopg2.connect(host="localhost",
                           user="postgres",
                           password="root",
                           dbname="kauntadb")
    return con


def close(con, cur):
    con.close()
    cur.close()


async def get_all_data_from(table: str) -> list(tuple()):
    query = f"SELECT * FROM {table}"
    con = start_connection()
    cur = con.cursor()
    cur.execute(query)
    result = cur.fetchall()
    close(con, cur)
    return result


def get_show_by_show_id(show_id: int):
    query = f"SELECT discord_id, name, current_episode, total_episodes, prequel FROM Series NATURAL JOIN Users WHERE series_id = %s"
    con = start_connection()
    cur = con.cursor()
    cur.execute(query, (show_id, ))
    results = cur.fetchall()
    close(con, cur)
    return results


def get_linked_show(show_id: int):
    query = f"SELECT series_id, name FROM Series WHERE prequel = %s"
    con = start_connection()
    cur = con.cursor()
    cur.execute(query, (show_id, ))
    results = cur.fetchall()
    close(con, cur)
    return results


def get_episode_data(show_id, episode_num):
    query = f"SELECT episode_name, filler, url FROM Episodes WHERE series_id = %s AND episode_number = %s"
    con = start_connection()
    cur = con.cursor()
    cur.execute(query, (show_id, episode_num))
    results = cur.fetchall()
    close(con, cur)
    return results


def get_shows_from_user(user_id: int):
    query = f"SELECT name, series_id, current_episode, total_episodes FROM Users NATURAL JOIN Series WHERE discord_id = %s ORDER BY time_added DESC"
    con = start_connection()
    cur = con.cursor()
    cur.execute(query, [user_id])
    results = cur.fetchall()
    shows = [(x[0],x[1],x[2],x[3]) for x in results]
    close(con, cur)
    return shows


async def get_watching_series_from_user(user_id: int):
    query = f"SELECT * FROM Series NATURAL JOIN Users WHERE user_id = %s AND watching = true;"
    con = start_connection()
    cur = con.cursor()
    cur.execute(query, (user_id))
    results = cur.fetchall()
    close(con, cur)
    return results


def add_episodes_to_show(episodes: dict, show: str, discord_id: int, name: str, prequel):
    con = start_connection()
    user_id = get_user_id(con, discord_id, name) 
    total_episodes = len(list(episodes.keys()))
    series_id = add_show_to_user(show, user_id, total_episodes, prequel)
    for episode_num in range(1, total_episodes + 1):
        add_episode(episode_num, episodes[episode_num]["Titel"], episodes[episode_num]["Filler"],  episodes[episode_num]["URL"], series_id)
    con.close()
 
 
def add_episode(episode_num, title, filler, url, series_id):
    con = start_connection()
    cur = con.cursor()
    query = f"INSERT INTO Episodes(episode_name, episode_number, filler, url, series_id) VALUES(%s, %s, %s, %s, %s)"
    cur.execute(query, (title, episode_num, filler, url, series_id))
    con.commit()
    close(con, cur)


def add_show_to_user(title, user_id, total_episodes, prequel):
    prequel_id = "Null" if prequel == None else get_show_id_by_name_and_user_id(prequel, user_id)
    con = start_connection()
    cur = con.cursor()
    query = f"INSERT INTO Series(name, user_id, total_episodes, watching, prequel) VALUES(%s, %s, %s, False, {prequel_id}) RETURNING series_id"
    cur.execute(query, (title, user_id, total_episodes))
    series_id = cur.fetchone()[0]
    con.commit()
    close(con, cur)
    return series_id
    
    
def get_user_id(con, discord_id: int, name: str):
    cur = con.cursor()
    user_query = f"SELECT * FROM Users WHERE discord_id = {discord_id}"
    cur.execute(user_query)
    result = cur.fetchone()
    cur.close()
    cur = con.cursor()
    if (result == None):
        add_user_query = f"INSERT INTO Users(user_name, discord_id) VALUES(%s, %s) RETURNING user_id"
        cur.execute(add_user_query, (name, discord_id))
        user_id = cur.fetchone()[0]
        cur.close()
        con.commit()
    else:
        user_id = result[0]
    return user_id


def get_show_id_by_name_and_user_id(show_name, user_id) -> int:
    con = start_connection()
    cur = con.cursor()
    query = f"SELECT series_id FROM Series NATURAL JOIN Users WHERE name = %s AND user_id = %s"
    cur.execute(query, (show_name, user_id))
    id = cur.fetchone()[0]
    close(con, cur)
    return id
    

def show_exists_for_user(show: str, user: int) -> bool:
    con = start_connection()
    cur = con.cursor()
    query = f"SELECT * FROM Series NATURAL JOIN Users WHERE user_id = %s AND name = %s"
    cur.execute(query, (user, show))
    results = cur.fetchall()
    close(con, cur)
    print(f"show_exists results: {results}")
    return True if len(results) > 0 else False
    
    
def increment_current_ep(show_id: int):
    query = f"UPDATE Series SET current_episode = current_episode + 1 WHERE series_id = %s"
    con = start_connection()
    cur = con.cursor()
    cur.execute(query, (show_id, ))
    con.commit()
    close(con, cur)
    
    
def decrement_current_ep(show_id: int):
    query = f"UPDATE Series SET current_episode = current_episode - 1 WHERE series_id = %s"
    con = start_connection()
    cur = con.cursor()
    cur.execute(query, (show_id, ))
    con.commit()
    close(con, cur)
