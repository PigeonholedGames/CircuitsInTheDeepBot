import discord
import dbmanager


# this method handles initializing the character creation process
async def chargen(thread, author):
    # pings the player to add them to the thread
    await thread.send(f"Hi {author.mention}, we'll make a character here.")
    await birth(thread, author)
    return


# this method handles querying and messaging for birth lifepaths
async def birth(thread, author):
    # first we get all the lifepaths for this age
    lifepaths = dbmanager.queryLifepaths(location="NEWATLANTIS", age="BIRTH")
    if len(lifepaths) == 0:
        await thread.send("Something has gone terribly wrong, please contact us.")
        raise Exception("Lifepath query empty.")

    currentx = 0

    # we make the embed which will show the player their options
    embed = makeembedbirth(lifepaths[x][0], lifepaths[x][17])

    listoptions = []
    for x in range(len(lifepaths)):
        if x != currentx:
            listoptions.append(discord.SelectOption(label=lifepaths[x][0], value=x))


    await thread.send(embed=embed, components = )


# this method handles querying and messaging for childhood lifepaths
async def child(thread, author, links):
    x = 0

    # we make the embed which will show the player their options
    #

    # await thread.send(embed=embed)

    return


# this method handles querying and messaging for teenage lifepaths
async def teen(thread, author, links):
    return


# this method handles querying and messaging for young adult lifepaths
async def ya(thread, author, links):
    return


# this method handles querying and messaging for adult lifepaths
async def adult(thread, author, links):
    return


# make an embed of birth lifepath
async def makeembedbirth(title, description):
    embed = discord.Embed(title=title, description=description, color=0x288830)
    embed.set_footer(
        text="Find the Lifepath you want from the drop-down list then click the green button to proceed.")
    return embed


# make an embed of non-birth lifepaths
async def makeembed(title, description, aptitudes, skills):
    embed = discord.Embed(title=title, description=description, color=0x288830)
    embed.add_field(name=" ", value=aptitudes, inline=True)
    embed.add_field(name=" ", value=skills, inline=True)
    embed.set_footer(
        text="Use the red undo button to go to the previous age, and the green submit button to confirm your choice.")

    return embed
