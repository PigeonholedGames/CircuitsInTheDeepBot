import dbmanager


async def chargen(thread, author):
    thread.send("*Welcome to character creation!*\n\n"
                "We're going to go through every step to keep yo")

    dbmanager.queryLifepaths(location="NEW ATLANTIS", age="CHILD", links="9,10,13,14,15,41,42,43")
    return
