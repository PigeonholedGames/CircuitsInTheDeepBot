import asyncio
import copy

import discord
import db
import character


# this method handles initializing the character creation process
async def begin(thread, author):
    # pings the player otherwise they won't be added to the thread
    await thread.send(f"Hi {author.mention}, we'll make a character here.")
    await asyncio.sleep(0.75)

    # explanation messages
    await thread.send("Character creation in Circuits in the Deep uses a lifepath system.")
    await asyncio.sleep(0.75)
    await thread.send("This means that we'll go through the broad strokes of your backstory.")
    await asyncio.sleep(0.75)
    await thread.send("You'll be presented with several options for each stage of your life.")
    await asyncio.sleep(0.75)
    await thread.send(
        "Depending on your choice you'll gain some stats and change what lifepaths you have access to further down the line.")
    await asyncio.sleep(0.75)
    await thread.send("Without further ado:")
    await asyncio.sleep(0.75)
    # begin!
    gen = Chargen(thread, author)
    await gen.layer0()


# oh boy here we go
class Chargen:

    def __init__(self, thread, author):
        # variables that ill need in every stage
        self.character0 = None
        self.links0 = ''
        self.character1 = None
        self.links1 = ''

        # and some simple global ones
        self.thread = thread
        self.author = author
        self.currentlayer = None

    # handles picking a birth lifepath
    async def layer0(self):

        # set the layer
        self.currentlayer = 0

        # makes the character for this layer
        self.character0 = character.Character(aptitudenames=db.queryAptitudeNames(),
                                              skillnames=db.querySkillNames(), server=self.thread.guild,
                                              thread=self.thread, player=self.author)

        # empties the links in case we've gone back
        self.links0 = ''

        # first we get all the lifepaths for this age
        lifepaths = db.queryLifepaths(location="NEWATLANTIS", age="BIRTH")

        # and check that we actually got them
        if len(lifepaths) == 0:
            await self.thread.send("Something has gone terribly wrong, please contact us.")
            raise Exception("Lifepaths query empty.")

        # we make the embed to display the first lifepath
        embed = discord.Embed(title='Birth',
                              description='You don\'t remember much from your first few years on Earth, so you won\'t get any skills from this choice. Instead, this will tell us a little about who your parents were.',
                              color=0x288830)
        embed.set_footer(
            text="Browse through the lifepaths using the drop-down list.")

        # then the drop-down menu with all the rest
        select = selectLifepath(chargen=self, lifepaths=lifepaths, placeholder='Who were you born to?')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking a childhood lifepath
    async def layer1(self, links):
        # hi we're here
        self.currentlayer = 1

        # makes the character for this layer
        self.character1 = copy.deepcopy(self.character0)

        # set the links for this layer
        self.links1 = links

        # first we get all the lifepaths for this age
        lifepaths = db.queryLifepath(location="NEWATLANTIS", age="CHILD", links=self.links1)

        # and check that we actually got them
        if len(lifepaths) == 0:
            await self.thread.send("Something has gone terribly wrong, please contact us.")
            raise Exception("Lifepaths query empty.")

        # we make the embed to display the first lifepath
        embed = discord.Embed(title='Childhood',
                              description='You can trace your affinity for certain skills all the way back here.',
                              color=0x288830)
        embed.set_footer(
            text="Browse through the lifepaths using the drop-down list.")

        # then the drop-down menu with all the rest
        select = selectLifepath(chargen=self, lifepaths=lifepaths, placeholder='What is a core memory from your childhood?')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking an aptitude from childhood
    async def layer2(self, links):
        # hi we're here
        self.currentlayer = 2

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking skills from childhood
    async def layer3(self, links):
        # hi we're here
        self.currentlayer = 3

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking a teenage lifepath
    async def layer4(self, links):
        # hi we're here
        self.currentlayer = 4

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking an aptitude from teenage years
    async def layer5(self, links):
        # hi we're here
        self.currentlayer = 5

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking skills from teenage years
    async def layer6(self, links):
        # hi we're here
        self.currentlayer = 6

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking a young adult lifepath
    async def layer7(self, links):
        # hi we're here
        self.currentlayer = 7

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking an aptitude from young adulthood
    async def layer8(self, links):
        # hi we're here
        self.currentlayer = 8

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking skills from young adulthood
    async def layer9(self, links):
        # hi we're here
        self.currentlayer = 9

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking the first adult lifepath
    async def layer10(self, links):
        # hi we're here
        self.currentlayer = 10

        # makes the character for this layer
        character1 = character(self.character0)

    # moving ooooooon moving on
    async def nextLayer(self, links):
        if self.currentlayer == 0:
            await self.layer1(links=links)
        elif self.currentlayer == 1:
            await self.layer2(links=links)
        elif self.currentlayer == 2:
            await self.layer3(links=links)
        elif self.currentlayer == 3:
            await self.layer4(links=links)
        elif self.currentlayer == 4:
            await self.layer5(links=links)
        elif self.currentlayer == 5:
            await self.layer6(links=links)
        elif self.currentlayer == 6:
            await self.layer7(links=links)
        elif self.currentlayer == 7:
            await self.layer8(links=links)
        elif self.currentlayer == 8:
            await self.layer9(links=links)
        elif self.currentlayer == 9:
            await self.layer10(links=links)
        elif self.currentlayer == 10:
            await self.layer11(links=links)
        elif self.currentlayer == 11:
            await self.layer12(links=links)
        elif self.currentlayer == 12:
            await self.layer13(links=links)
        elif self.currentlayer == 13:
            await self.layer14(links=links)
        elif self.currentlayer == 14:
            await self.layer15(links=links)

    # moving back moving baaaaaaaaaaaaaaaaack
    async def prevLayer(self):
        if self.currentlayer == 0:
            await self.layer0()
        elif self.currentlayer == 1:
            await self.layer0()
        elif self.currentlayer == 2:
            await self.layer1()
        elif self.currentlayer == 3:
            await self.layer2()
        elif self.currentlayer == 4:
            await self.layer3()
        elif self.currentlayer == 5:
            await self.layer4()
        elif self.currentlayer == 6:
            await self.layer5()
        elif self.currentlayer == 7:
            await self.layer6()
        elif self.currentlayer == 8:
            await self.layer7()
        elif self.currentlayer == 9:
            await self.layer8()
        elif self.currentlayer == 10:
            await self.layer9()
        elif self.currentlayer == 11:
            await self.layer10()
        elif self.currentlayer == 12:
            await self.layer11()
        elif self.currentlayer == 13:
            await self.layer12()
        elif self.currentlayer == 14:
            await self.layer13()

    def getLayer(self):
        return self.currentlayer


# this class handles displaying the drop-down list of lifepaths
class selectLifepath(discord.ui.Select):

    # constructor needs the chargen to pass onto its buttons, the list of lifepaths, the position of the currently displayed lifepath to be removed from the list, and the placeholder text
    def __init__(self, chargen, lifepaths, position='', placeholder=''):
        self.chargen = chargen
        self.lifepaths = lifepaths
        self.position = position

        # the options list is constructed from the lifepaths list minus the one being currently displayed
        options = []
        for x in range(len(lifepaths)):
            if x != position:
                options.append(discord.SelectOption(label=lifepaths[x][0], value=x, default=False))

        super().__init__(placeholder=placeholder, max_values=1, options=options)

    # once the user picks an option the embed is updated to display what they chose and a new drop-down list is generated
    async def callback(self, interaction: discord.Interaction):
        # get the index of the pressed option
        self.position = int(self.values[0])

        # make the new embed
        embed = await makeembedlifepaths(self.lifepaths[self.position][0], self.lifepaths[self.position][17],
                                         aptitudes=None, skills=None, chargen=self.chargen)
        # make the new drop-down list
        select = selectLifepath(chargen=self.chargen, lifepaths=self.lifepaths, position=self.position,
                                placeholder=self.placeholder)
        # make the view with the two buttons
        view = ButtonView(select=select, chargen=self.chargen, links=self.lifepaths[self.position][1])
        # ship it
        await interaction.message.edit(embed=embed, view=view)
        try:
            await interaction.response.send_message(" ")
        except:
            pass


# make an embed of lifepaths
async def makeembedlifepaths(title, description, aptitudes, skills, chargen):
    embed = discord.Embed(title=title, description=description, color=0x288830)

    if aptitudes is not None:
        embed.add_field(name=" ", value=aptitudes, inline=True)
        embed.add_field(name=" ", value=skills, inline=True)
        if chargen.getLayer() > 0:
            embed.set_footer(
                text="Use the red undo button to go back, or the green tick button to confirm your choice.")
        else:
            embed.set_footer("Use the green tick button to confirm your choice.")

    else:
        embed.set_footer(text="Browse through the lifepaths using the drop-down list and confirm your selection using the green tick button.")

    return embed


# makes a view with buttons and stuff
class ButtonView(discord.ui.View):

    def __init__(self, *, timeout=180, select, chargen, links=None):
        super().__init__(timeout=timeout)
        self.add_item(select)
        if links is not None:
            self.add_item(
                okButton(chargen=chargen, links=links))

        if chargen.getLayer() > 0:
            self.add_item(
                undoButton(chargen=chargen))


# button to progress the lifepath selection
class okButton(discord.ui.Button):

    # we need the chargen to take us to the next step and also prob smth else in the future so yea, that
    def __init__(self, chargen, links):
        self.chargen = chargen
        self.links = links
        super().__init__(emoji=discord.PartialEmoji.from_str("✅"), style=discord.ButtonStyle.green)

    # when pressed, the chargen takes over
    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
        await self.chargen.nextLayer(links=self.links)
        return


# button to take us a step back
class undoButton(discord.ui.Button):
    # we need the chargen to take us to the previous step and also prob smth else in the future so yea, that
    def __init__(self, chargen):
        self.chargen = chargen
        super().__init__(emoji=discord.PartialEmoji.from_str("↩"), style=discord.ButtonStyle.red)

    # when pressed, the chargen takes over
    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
        await self.chargen.prevLayer()
        return
