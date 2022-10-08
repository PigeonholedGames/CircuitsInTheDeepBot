import sqlite3

# this opens the database where all the lifepaths are stored
lf = sqlite3.connect('Lifepaths.db')
lifepaths = lf.cursor()

# this opens the database where all the characters are stored
char = sqlite3.connect('Characters.db')
characters = char.cursor()

# this opens the database where all the game data is stored
gd = sqlite3.connect('GameData.db')
gamedata = gd.cursor()


# function to query the lifepaths database
def queryLifepaths(location, age, links):
    q = lifepaths.execute(
        "SELECT NAME,LINKS,APTITUDES,SKILLS,DESCRIPTION,QUESTIONS,END FROM {} "
        "WHERE AGE='{}' "
        "AND ID IN ({})".format(location, age, links))
    return q


def queryAltLifepaths(location, age):
    q = lifepaths.execute(
        "SELECT NAME,LINKS,APTITUDES,SKILLS,DESCRIPTION,QUESTIONS FROM *"
        "WHERE AGE='{}'"
        "AND ENTRY CONTAINS '{}'".format(location, age))
    return q


# function to fetch the base game stats
def queryGameData(fields, table):
    q = gamedata.execute("SELECT {} FROM {}".format(fields, table))
    return q


def queryPlayer(server, player):
    q = characters.execute("SELECT NAME FROM CHARACTERS"
                           "WHERE SERVER = '{}' AND PLAYER = '{}'")
    return q


def queryCharacters(server, player, name):
    q = characters.execute("SELECT * FROM CHARACTERS"
                           "WHERE SERVER = '{}' AND PLAYER = '{}' AND NAME = '{}'")
    return q


def addCharacter(server, player, name, thread, alias, playbook, traits, luck, abilities, realization, aptitudes1, aptitudes2,
                 aptitudes3, aptitudes4, skills1, skills2, skills3, skills4, skills5, skills6):
    characters.execute((
                           "INSERT INTO CHARACTERS(SERVER,THREAD,PLAYER,NAME,ALIAS,PLAYBOOK,ABILITIES,TRAITS,LUCK,REALIZATION,APTITUDES1,APTITUDES2,APTITUDES3,APTITUDES4,SKILLS1,SKILLS2,SKILLS3,SKILLS4,SKILLS5,SKILLS6)"
                           "VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') "
                           "").format(server, thread, player, name, alias, playbook, abilities, traits, luck, realization,
                                      aptitudes1, aptitudes2, aptitudes3, aptitudes4, skills1, skills2, skills3,
                                      skills4, skills5, skills6))
    characters.commit()
    return
