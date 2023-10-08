import sqlite3

# these methods handle all interactions with the database

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
def queryLifepath(location, age, links):
    q = lifepaths.execute(
        "SELECT NAME,LINKS,APTITUDES0,APTITUDES1,APTITUDES2,APTITUDES3,APTITUDES4,SKILLS0,SKILLS1,SKILLS2,SKILLS3,SKILLS4,SKILLS5,SKILLS6,SKILLS7,SKILLS8,SKILLS9,DESCRIPTION,QUESTIONS,END FROM {} "
        "WHERE AGE='{}' "
        "AND ID IN ({})".format(location, age, links))
    return q.fetchall()


# lighter function to query the lifepaths database, to be used for getting birth lifepaths
def queryLifepaths(location, age):
    q = lifepaths.execute(
        "SELECT NAME,LINKS,APTITUDES0,APTITUDES1,APTITUDES2,APTITUDES3,APTITUDES4,SKILLS0,SKILLS1,SKILLS2,SKILLS3,SKILLS4,SKILLS5,SKILLS6,SKILLS7,SKILLS8,SKILLS9,DESCRIPTION,QUESTIONS,END FROM {} "
        "WHERE AGE='{}' ".format(location, age))
    return q.fetchall()


def queryAltLifepaths(location, age):
    q = lifepaths.execute(
        "SELECT NAME,LINKS,APTITUDES0,APTITUDES1,APTITUDES2,APTITUDES3,APTITUDES4,SKILLS0,SKILLS1,SKILLS2,SKILLS3,SKILLS4,SKILLS5,SKILLS6,SKILLS7,SKILLS8,SKILLS9,DESCRIPTION,QUESTIONS,END FROM *"
        "WHERE AGE='{}'"
        "AND ENTRY CONTAINS '{}'".format(location, age))
    return q.fetchall()


# function to fetch the base game stats
def queryGameData(fields, table):
    q = gamedata.execute("SELECT {} FROM {}".format(fields, table))
    return q.fetchall()


# function to fetch aptitude names
def queryAptitudeNames():
    q = gamedata.execute("SELECT NAME FROM APTITUDES")
    return q.fetchall()


# function to fetch aptitude to display
def queryAptitudePrintable(name):
    q = gamedata.execute("SELECT PRINTABLE,DESCRIPTION FROM APTITUDES WHERE NAME='{}'".format(name))
    return q.fetchall()


# function to fetch skill names
def querySkillNames():
    q = gamedata.execute("SELECT NAME FROM SKILLS")
    return q.fetchall()


# function to fetch playbooks
def queryPlaybooks():
    q = gamedata.execute("SELECT * FROM PLAYBOOKS")
    return q.fetchall()


def queryPlayer(server, player):
    q = characters.execute(
        "SELECT NAME FROM CHARACTERS"
        "WHERE SERVER = '{}' AND PLAYER = '{}'")
    return q.fetchall()


def queryCharacters(server, player, name):
    q = characters.execute(
        "SELECT * FROM CHARACTERS"
        "WHERE SERVER = '{}' AND PLAYER = '{}' AND NAME = '{}'")
    return q


def addCharacter(server, player, name, thread, alias, playbook, traits, luck, abilities, realization, aptitudes1,
                 aptitudes2,
                 aptitudes3, aptitudes4, skills1, skills2, skills3, skills4, skills5, skills6):
    characters.execute((
                           "INSERT INTO CHARACTERS(SERVER,THREAD,PLAYER,NAME,ALIAS,PLAYBOOK,ABILITIES,TRAITS,LUCK,REALIZATION,APTITUDES1,APTITUDES2,APTITUDES3,APTITUDES4,SKILLS1,SKILLS2,SKILLS3,SKILLS4,SKILLS5,SKILLS6)"
                           "VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') "
                       ).format(server, thread, player, name, alias, playbook, abilities, traits, luck, realization,
                                aptitudes1, aptitudes2, aptitudes3, aptitudes4, skills1, skills2, skills3, skills4,
                                skills5, skills6))
    characters.commit()
    return


def queryAptitudes():
    q = gamedata.execute("SELECT NAME, DESCRIPTION FROM APTITUDES")
    return q.fetchall()


def querySkills():
    q = gamedata.execute("SELECT NAME, DESCRIPTION FROM SKILLS")
    return q.fetchall()


def queryLocations():
    q = gamedata.execute("SELECT * FROM LOCATIONS")
    return q.fetchall()
