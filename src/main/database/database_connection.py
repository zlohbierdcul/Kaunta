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

async def get_watching_series_from_user(user_id: int) -> list(str):
    query = f"SELECT * FROM public.\"Series\" NATURAL JOIN public.\"Users\" WHERE user_id = \"{user_id}\" AND watching = true;"
    con = start_connection()
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    close(con, cur)
    return results
    