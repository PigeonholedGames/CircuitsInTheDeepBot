import asyncio
import discord
import dbmanager
import character


# this method handles initializing the character creation process
async def chargen(thread, author):
    # pings the player to add them to the thread
    await thread.send(f"Hi {author.mention}, we'll make a character here.")

    # create a new character, a questions list
    # character0 = character(dbmanager.queryAptitudeNames(), dbmanager.querySkillNames(), thread.guild, thread, author)

    await thread.send("The first step in creating a character is picking a playbook.")
    await asyncio.sleep(1)
    await thread.send("This will define your expertise and role within the crew.")
    await asyncio.sleep(1)
    await thread.send("Your choices are:")
    await playbook(thread, author)

    # await birth(thread, author)
    return


# this method handles querying and messaging for playbook selection
async def playbook(thread, author):
    playbooks = dbmanager.queryPlaybooks()
    if len(playbooks) == 0:
        await thread.send("Something has gone terribly wrong, please contact us.")
        raise Exception("Playbooks query empty.")

    currentx = 0
    embed = await makeembedplaybook(playbooks[currentx][0], playbooks[currentx][1], playbooks[currentx][4],
                                    playbooks[currentx][5], playbooks[currentx][6], playbooks[currentx][7],
                                    playbooks[currentx][8], playbooks[currentx][9])

    select = SelectPlaybook(playbooks, currentx)
    view = SelectView()
    view.add_item(select)

    await thread.send(embed=embed, view=view)


# this method handles querying and messaging for birth lifepaths
async def birth(thread, author):
    # first we get all the lifepaths for this age
    lifepaths = dbmanager.queryLifepaths(location="NEWATLANTIS", age="BIRTH")
    if len(lifepaths) == 0:
        await thread.send("Something has gone terribly wrong, please contact us.")
        raise Exception("Lifepaths query empty.")

    currentx = 0
    # we make the embed which will show the player their options
    embed = await makeembedbirth(lifepaths[currentx][0], lifepaths[currentx][17])

    select = SelectLifepath(lifepaths, currentx, "Who were you born to?")
    view = SelectView()
    view.add_item(select)

    await thread.send(embed=embed, view=view)


# this method handles querying and messaging for childhood lifepaths
async def child(thread, author, links):
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


# make an embed of a playbook
async def makeembedplaybook(title, description, aptitude, skill0, skill1, skill2, skill3, skill4):
    embed = discord.Embed(title=title, description=description, color=0x288830)
    if aptitude is None:
        embed.add_field(name="",
                        value="You get to pick any Aptitude as your field of expertise.\nYou will also get to pick any 2 Skills to invest in.",
                        inline=True)
    else:
        embed.add_field(name="",
                        value="You'll be in your element when you can {} to solve problems.\nYou'll excel in two Skills from amongst {}, {}, {}, {} and {}.".format(
                            aptitude, skill0, skill1, skill2, skill3, skill4),
                        inline=True)

    embed.set_footer(text="Use the red undo button to go back, or the green submit button to confirm your choice.")

    return embed


# make an embed of birth lifepath
async def makeembedbirth(title, description):
    embed = discord.Embed(title=title, description=description, color=0x288830)
    embed.set_footer(
        text="Use the red undo button to go back, or the green submit button to confirm your choice.")
    return embed


# make an embed of non-birth lifepaths
async def makeembed(title, description, aptitudes, skills):
    embed = discord.Embed(title=title, description=description, color=0x288830)
    embed.add_field(name=" ", value=aptitudes, inline=True)
    embed.add_field(name=" ", value=skills, inline=True)
    embed.set_footer(
        text="Use the red undo button to go back, or the green submit button to confirm your choice.")

    return embed


class SelectPlaybook(discord.ui.Select):

    def __init__(self, playbooks, currentx):
        self.playbooks = playbooks
        self.currentx = currentx
        options = []
        for x in range(len(playbooks)):
            if x != currentx:
                options.append(discord.SelectOption(label=playbooks[x][0], value=x, default=False))
        super().__init__(placeholder="Pick a Playbook", max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        self.currentx = int(self.values[0])

        embed = await makeembedplaybook(self.playbooks[self.currentx][0], self.playbooks[self.currentx][1],
                                        self.playbooks[self.currentx][4], self.playbooks[self.currentx][5],
                                        self.playbooks[self.currentx][6], self.playbooks[self.currentx][7],
                                        self.playbooks[self.currentx][8], self.playbooks[self.currentx][9])

        select = SelectPlaybook(self.playbooks, self.currentx)
        view = SelectView()
        view.add_item(select)
        await interaction.message.edit(embed=embed, view=view)
        try:
            await interaction.response.send_message(" ")
        except:
            pass


class SelectLifepath(discord.ui.Select):

    def __init__(self, lifepaths, currentx, placeholder):
        self.lifepaths = lifepaths
        self.currentx = currentx
        self.placeholder = placeholder
        options = []
        for x in range(len(lifepaths)):
            if x != currentx:
                options.append(discord.SelectOption(label=lifepaths[x][0], value=x, default=False))
        super().__init__(placeholder=placeholder, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        self.currentx = int(self.values[0])

        embed = await makeembedbirth(self.lifepaths[self.currentx][0], self.lifepaths[self.currentx][17])

        select = SelectLifepath(self.lifepaths, self.currentx, self.placeholder)
        view = SelectView()
        view.add_item(select)
        await interaction.message.edit(embed=embed, view=view)
        try:
            await interaction.response.send_message(" ")
        except:
            pass


class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
