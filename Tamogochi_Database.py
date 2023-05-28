import sqlite3


def write_data_database(pet):
    connect = sqlite3.connect('Tamogochi.db')
    cursor = connect.cursor()

    cursor.execute(
        """INSERT INTO Pets (name, scores, eat, health, mood, sleep, hygiena) VALUES (?, 100, 100, 100, 100, 100, 100)""",
        [pet])

    cursor.close()
    connect.commit()
    connect.close()


def delete_data_database():
    connect = sqlite3.connect('Tamogochi.db')
    cursor = connect.cursor()
    cursor.execute("""DELETE FROM Pets""")
    cursor.close()
    connect.commit()
    connect.close()


def update_pets_from_database(choice_pet):
    connect = sqlite3.connect('Tamogochi.db')
    cursor = connect.cursor()
    cursor.execute(f"""SELECT * FROM Pets WHERE name = '{choice_pet.replace("'", "''")}'""")

    data = cursor.fetchall()
    # data_status = [list(row) for row in data]

    # print(data_status)

    data_scores = data[0][1]
    data_eat = data[0][2]
    data_health = data[0][3]
    data_mood = data[0][4]
    data_sleep = data[0][5]
    data_hygiena = data[0][6]

    cursor.close()
    connect.commit()
    connect.close()

    return data_scores, data_eat, data_health, data_mood, data_sleep, data_hygiena
