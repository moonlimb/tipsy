#Put initial dataset into the tipsy database

import model

db = model.connect_db()

list_of_users = [
("sanby@hackbright.com", "sanby_password", "Sanby"),
("moon@hackbright.com", "moon_password", "Moon"),
("sara@hackbright.com", "sara_password", "Sara"),
("lydia@hackbright.com", "lydia_password", "Lydia"),
("annie@hackbright.com", "annie_password", "Annie"),
("michelle@hackbright.com","michelle_password","Michelle"),
("nicole@hackbright.com","nicole_password","Nicole"),
("meredith@hackbright.com","meredith_password","Meredith"),
("susan@hackbright.com","susan_password","Susan"),
("sonya@hackbright.com","sonya_password","Sonya")]

list_of_tasks = [
"Eat at Thai 360",
"Eat at Tartine Bakery",
"Eat at Dante's Weird Fish",
"Eat at Pancho Villa",
"Eat at Rhea's Sandwiches",
"Eat at Limon Rotisserie",
"Eat at Foreign Cinema",
"Eat at The House",
"Eat at Pesce",
"Eat somewhere in Chinatown (mysterious)",
"Eat at the Ferry Building",
"Go to farmer's market",
"Watch reality tv",
"Watch a movie",
"Get tipsy",
"Get drunk",
"Get wasted",
"Blackout",
"Eat brunch the following day to cure hangover",
"Buy wine"]

index = 19

for email, pwd, name in list_of_users:
    user_id = model.new_user(db, email, pwd, name)

    if index >= 1:
        task1 = model.new_task(db, list_of_tasks[index], user_id)
        task2 = model.new_task(db, list_of_tasks[index-1], user_id)
        index -= 2
