import psycopg2 

def start_connection():
    con = psycopg2.connect(host="localhost",
                           user="postgres",
                           password="root",
                           dbname="epicountdev")
    
    return con


def close(con, cur):
    con.close()
    cur.close()


async def get_all_data_from(table: str) -> list(tuple()):
    query = f"SELECT * FROM public.\"{table}\""
    con = start_connection()
    cur = con.cursor()
    cur.execute(query)
    result = cur.fetchall()
    close(con, cur)
    return result


async def get_watching_series_from_user(user_id: int):
    query = f"SELECT * FROM public.\"Series\" NATURAL JOIN public.\"Users\" WHERE user_id = \"{user_id}\" AND watching = true;"
    con = start_connection()
    cur = con.cursor()
    cur.execute(query)
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
    query = f"INSERT INTO public.\"Episodes\"(episode_name, episode_number, filler, url, series_id) VALUES(%s, %s, %s, %s, %s)"
    cur.execute(query, (title, episode_num, filler, url, series_id))
    con.commit()
    close(con, cur)


def add_show_to_user(title, user_id, total_episodes, prequel):
    prequel_id = "Null" if prequel == None else get_show_id_by_name_and_user_id(prequel, user_id)
    con = start_connection()
    cur = con.cursor()
    query = f"INSERT INTO public.\"Series\"(name, user_id, total_episodes, watching, prequel) VALUES('{title}', {user_id}, {total_episodes}, False, {prequel_id}) RETURNING series_id"
    cur.execute(query)
    series_id = cur.fetchone()[0]
    con.commit()
    close(con, cur)
    return series_id
    
    
def get_user_id(con, discord_id: int, name: str):
    cur = con.cursor()
    user_query = f"SELECT * FROM public.\"Users\" WHERE discord_id = {discord_id}"
    cur.execute(user_query)
    result = cur.fetchone()
    cur.close()
    cur = con.cursor()
    if (result == None):
        add_user_query = f"INSERT INTO public.\"Users\"(user_name, discord_id) VALUES('{name}', {discord_id}) RETURNING user_id"
        cur.execute(add_user_query)
        user_id = cur.fetchone()[0]
        cur.close()
        con.commit()
    else:
        user_id = result[0]
    return user_id


def get_show_id_by_name_and_user_id(show_name, user_id) -> int:
    con = start_connection()
    cur = con.cursor()
    query = f"SELECT series_id FROM public.\"Series\" NATURAL JOIN public.\"Users\" WHERE name = '{show_name}' AND user_id = {user_id}"
    cur.execute(query)
    id = cur.fetchone()[0]
    close(con, cur)
    return id
    

def show_exists_for_user(show: str, user: int) -> bool:
    con = start_connection()
    cur = con.cursor()
    query = f"SELECT * FROM public.\"Series\" NATURAL JOIN public.\"Users\" WHERE user_id = {user} AND name = \'{show}\'"
    cur.execute(query)
    results = cur.fetchall()
    close(con, cur)
    return True if len(results) > 0 else False
    