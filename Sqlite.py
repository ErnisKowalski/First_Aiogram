import sqlite3 as sl


async def db_start():
    global db, cur
    db = sl.connect('profile.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Info_user(user_id INT PRIMARY KEY,name TEXT, photo TEXT, leisure TEXT);")
    db.commit()


async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM Info_user WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO Info_user VALUES(?, ?, ?, ?)", (user_id, '','',''))
        db.commit()



async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE Info_user SET name = '{}', photo ='{}', leisure  ='{}' WHERE user_id =='{}'".format(
            data['name'], data['photo'], data['leisure'], user_id))
        db.commit()


#def save_location(latitude, longitude):
    #cur.execute("INSERT INTO location(longitude, latitude) VALUES (?, ?)", (longitude, latitude))
    #db.commit()


async def delete_profile(user_id):
    cur.execute("DELETE FROM Info_user WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    db.commit()


async def check_info(user_id):
    user = int(user_id)
    cur.execute("SELECT 1 FROM Info_user WHERE user_id =='{key}'".format(key=user)).fetchone()
    db.commit()