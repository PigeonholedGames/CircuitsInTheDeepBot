import asyncio
import copy

import discord
import db
import character


# this method handles initializing the character creation process
async def begin(thread, author):
    # pings the player otherwise they won't be added to the thread
    await thread.send(f"Hi {author.mention}, we'll make a character here.")
    await asyncio.sleep(2.00)

    # explanation messages
    await thread.send("Character creation in Circuits in the Deep uses a lifepath system.")
    await asyncio.sleep(0.95)
    await thread.send(
        "This means that we'll go through the broad strokes of your backstory and you'll decide what you were doing during each stage of your life.")
    await asyncio.sleep(2.05)
    await thread.send("Your choices will grant you some stats and unlock different lifepaths later down the line.")
    await asyncio.sleep(1.05)
    await thread.send(
        "But first you'll pick your trappings, which describe the role you'll end up filling within the crew.")
    await asyncio.sleep(1.45)
    await thread.send("Without further ado:")
    await asyncio.sleep(0.1)
    # begin!
    gen = Chargen(thread, author)
    await gen.layer0()


# oh boy here we go
class Chargen:

    def __init__(self, thread, author):
        # lists for variables that ill need in every stage
        self.characters = []
        self.location = []
        self.links = []

        # and some simple global ones
        self.thread = thread
        self.author = author
        self.currentlayer = None

    # handles picking trappings
    async def layer0(self):
        self.currentlayer = 0
        self.characters.append(character.Character(aptitudenames=db.queryAptitudeNames(),
                                                   skillnames=db.querySkillNames(), server=self.thread.guild,
                                                   thread=self.thread, player=self.author))
        await self.nextLayer("")

    # handles picking a birth location
    async def layer1(self):
        self.currentlayer = 1
        await self.nextLayer("NEWATLANTIS")

    # handles picking a birth lifepath
    async def layer2(self):

        # set the layer
        self.currentlayer = 2

        # first we get all the lifepaths for this age
        lifepaths = db.queryLifepaths(location=self.location[0], age="BIRTH")

        # and check that we actually got them
        if len(lifepaths) == 0:
            await self.thread.send("Something has gone terribly wrong, please contact us.")
            raise Exception("Lifepaths query empty.")

        # we make the embed to display the first lifepath
        embed = discord.Embed(title='Birth',
                              description='You don\'t remember much from your first few years on Earth, so you won\'t get any stats from this choice. Instead, this will tell us a little about who your parents were.',
                              color=0x288830)
        embed.set_footer(
            text="Browse through the lifepaths using the drop-down list.")

        # then the drop-down menu with all the rest
        select = selectLifepath(chargen=self, lifepaths=lifepaths, placeholder='Who were you born to?')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking childhood location
    async def layer3(self):
        # hi we're here
        self.currentlayer = 3
        await self.nextLayer("NEWATLANTIS")

    # handles picking a childhood lifepath
    async def layer4(self):
        # hi we're here
        self.currentlayer = 4

        # first we get all the lifepaths for this age
        lifepaths = db.queryLifepath(location=self.location[1], age="CHILD", links=self.links[0])

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
        select = selectLifepath(chargen=self, lifepaths=lifepaths,
                                placeholder='What is a core memory from your childhood?')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking an aptitude from childhood
    async def layer5(self):
        # hi we're here
        self.currentlayer = 5
        self.characters.append(copy.deepcopy(self.characters[0]))

        await self.nextLayer()

    # handles picking the first skill from childhood
    async def layer6(self):
        # hi we're here
        self.currentlayer = 6

        # makes the character for this layer
        self.characters.append(copy.deepcopy(self.characters[1]))

        await self.nextLayer()

    # handles picking the second skill from childhood
    async def layer7(self):
        # hi we're here
        self.currentlayer = 7

        # makes the character for this layer
        self.characters.append(copy.deepcopy(self.characters[2]))

        await self.nextLayer()

    # handles picking a teen location
    async def layer8(self):
        # hi we're here
        self.currentlayer = 8

        await self.nextLayer("NEWATLANTIS")

    # handles picking a teen lifepath
    async def layer9(self):
        # hi we're here
        self.currentlayer = 9

        # first we get all the lifepaths for this age
        lifepaths = db.queryLifepath(location=self.location[2], age="TEEN", links=self.links[1])

        # and check that we actually got them
        if len(lifepaths) == 0:
            await self.thread.send("Something has gone terribly wrong, please contact us.")
            raise Exception("Lifepaths query empty.")

        # we make the embed to display the first lifepath
        embed = discord.Embed(title='Teenage Years',
                              description='You\'ve begun to grow into your own person, but there\'s still a long way to go.',
                              color=0x288830)
        embed.set_footer(
            text="Browse through the lifepaths using the drop-down list.")

        # then the drop-down menu with all the rest
        select = selectLifepath(chargen=self, lifepaths=lifepaths,
                                placeholder='What were you doing during your teenage years?')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking an aptitude from the teenage years
    async def layer10(self):
        # hi we're here
        self.currentlayer = 10

        # makes the character for this layer
        self.characters.append(copy.deepcopy(self.characters[3]))

    # handles picking the first skill from the teenage years
    async def layer11(self):
        # hi we're here
        self.currentlayer = 11

        # makes the character for this layer
        self.characters.append(copy.deepcopy(self.characters[4]))

    # handles picking the second skill from the teenage years
    async def layer12(self):
        # hi we're here
        self.currentlayer = 12
        # makes the character for this layer
        self.characters.append(copy.deepcopy(self.characters[5]))

    # handles picking the young adult location
    async def layer13(self):
        # hi we're here
        self.currentlayer = 13

    # handles picking the young adult lifepath
    async def layer14(self):
        # hi we're here
        self.currentlayer = 14

    # handles picking an aptitude from young adulthood
    async def layer15(self):
        # hi we're here
        self.currentlayer = 15

        # makes the character for this layer
        self.characters.append(copy.deepcopy(self.characters[6]))

    # handles picking the first skill from young adulthood
    async def layer16(self):
        # hi we're here
        self.currentlayer = 11

        # makes the character for this layer
        self.characters.append(copy.deepcopy(self.characters[7]))

    # handles picking the second skill from young adulthood
    async def layer17(self):
        # hi we're here
        self.currentlayer = 12
        # makes the character for this layer
        self.characters.append(copy.deepcopy(self.characters[8]))

    # carry ooooooon carry on
    async def nextLayer(self, selection=None):

        # trappings
        if self.currentlayer == 0:
            await self.layer1()

        # birth location
        elif self.currentlayer == 1:
            # set the location for this layer
            if selection is None:
                await self.thread.send("Something has gone terribly wrong, please contact us.")
                raise Exception("Birth Lifepath Location Missing")
            self.location.append(selection)
            await self.layer2()

        # birth selection
        elif self.currentlayer == 2:
            # set the links for this layer
            if selection is None:
                await self.thread.send("Something has gone terribly wrong, please contact us.")
                raise Exception("Birth Lifepath Links Missing")
            self.links.append(selection)
            await self.layer3()

        # child location
        elif self.currentlayer == 3:
            # set the location for this layer
            if selection is None:
                await self.thread.send("Something has gone terribly wrong, please contact us.")
                raise Exception("Child Lifepath Location Missing")
            self.location.append(selection)
            await self.layer4()

        # child selection
        elif self.currentlayer == 4:
            # set the links for this layer
            if selection is None:
                await self.thread.send("Something has gone terribly wrong, please contact us.")
                raise Exception("Child Lifepath Links Missing")
            self.links.append(self.links[0] + "," + selection)
            await self.layer5()

        # child aptitude
        elif self.currentlayer == 5:
            await self.layer6()

        # child skill 1
        elif self.currentlayer == 6:
            await self.layer7()

        # child skill 2
        elif self.currentlayer == 7:
            await self.layer8()

        # teen location
        elif self.currentlayer == 8:
            # set the location for this layer
            if selection is None:
                await self.thread.send("Something has gone terribly wrong, please contact us.")
                raise Exception("Child Lifepath Location Missing")
            self.location.append(selection)
            await self.layer9()

        # teen selection
        elif self.currentlayer == 9:
            # set the links for this layer
            if selection is None:
                await self.thread.send("Something has gone terribly wrong, please contact us.")
                raise Exception("Lifepath Links Missing")
            self.links.append(self.links[1] + "," + selection)
            await self.layer10()

        # teen aptitude
        elif self.currentlayer == 10:
            await self.layer11()

        # teen skill 1
        elif self.currentlayer == 11:
            await self.layer12()

        # teen skill 2
        elif self.currentlayer == 12:
            await self.layer13()

        # ya location
        elif self.currentlayer == 13:
            # set the location for this layer
            if selection is None:
                await self.thread.send("Something has gone terribly wrong, please contact us.")
                raise Exception("Lifepath Location Missing")
            self.location.append(selection)
            await self.layer14()

        # ya selection
        elif self.currentlayer == 14:
            # set the links for this layer
            if selection is None:
                await self.thread.send("Something has gone terribly wrong, please contact us.")
                raise Exception("Lifepath Links Missing")
            self.links.append(self.links[2] + "," + selection)
            await self.layer15()

        # ya aptitude
        elif self.currentlayer == 15:
            await self.layer16()

        # ya skill 1
        elif self.currentlayer == 16:
            await self.layer17()

        # ya skill 2
        elif self.currentlayer == 17:
            await self.layer18()

    # as if nothing really matters
    async def prevLayer(self):
        # trappings
        if self.currentlayer == 0:
            self.characters.pop()
            await self.layer0()
        # birth location
        elif self.currentlayer == 1:
            self.characters.pop()
            await self.layer0()
        # birth selection
        elif self.currentlayer == 2:
            self.location.pop()
            await self.layer1()
        # child location
        elif self.currentlayer == 3:
            self.links.pop()
            await self.layer2()
        # child selection
        elif self.currentlayer == 4:
            self.location.pop()
            await self.layer3()
        # child aptitude
        elif self.currentlayer == 5:
            self.links.pop()
            await self.layer4()
        # child skill 1
        elif self.currentlayer == 6:
            self.characters.pop()
            await self.layer5()
        # child skill 2
        elif self.currentlayer == 7:
            self.characters.pop()
            await self.layer6()
        # teen location
        elif self.currentlayer == 8:
            self.characters.pop()
            await self.layer7()
        # teen selection
        elif self.currentlayer == 9:
            self.location.pop()
            await self.layer8()
        # teen aptitude
        elif self.currentlayer == 10:
            self.links.pop()
            await self.layer9()
        # teen skill 1
        elif self.currentlayer == 11:
            self.characters.pop()
            await self.layer10()
        # teen skill 2
        elif self.currentlayer == 12:
            self.characters.pop()
            await self.layer11()
        # ya location
        elif self.currentlayer == 13:
            self.characters.pop()
            await self.layer12()
        # ya selection
        elif self.currentlayer == 14:
            self.location.pop()
            await self.layer13()
        # ya aptitude
        elif self.currentlayer == 15:
            self.links.pop()
            await self.layer14()
        # ya skill 1
        elif self.currentlayer == 16:
            self.characters.pop()
            await self.layer15()
        # ya skill 2
        elif self.currentlayer == 17:
            self.characters.pop()
            await self.layer16()

    def getLayer(self):
        return self.currentlayer


# this class handles displaying the drop-down list of lifepaths
class selectLifepath(discord.ui.Select):

    # constructor needs the chargen to pass onto its buttons, the list of lifepaths, the position of the currently displayed lifepath to be removed from the list, and the placeholder text
    def __init__(self, chargen, lifepaths, position=None, placeholder=''):
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
        # get the index of the selected option
        self.position = int(self.values[0])

        # make the new embed
        embed = await makeembedlifepaths(title=self.lifepaths[self.position][0],
                                         description=self.lifepaths[self.position][17],
                                         aptitudes=None, skills=None, chargen=self.chargen)
        # make the new drop-down list
        select = selectLifepath(chargen=self.chargen, lifepaths=self.lifepaths, position=self.position,
                                placeholder=self.placeholder)
        # make the view with the two buttons
        view = ButtonView(select=select, chargen=self.chargen, selection=self.lifepaths[self.position][1])
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
            embed.set_footer(text="Use the green tick button to confirm your choice.")

    else:
        embed.set_footer(
            text="Browse through the lifepaths using the drop-down list and confirm your selection using the green tick button.")

    return embed


# makes a view with buttons and stuff
class ButtonView(discord.ui.View):

    def __init__(self, *, timeout=180, select, chargen, selection=None):
        super().__init__(timeout=timeout)
        self.add_item(select)
        if selection is not None:
            self.add_item(
                okButton(chargen=chargen, selection=selection))

        if chargen.getLayer() > 0:
            self.add_item(
                undoButton(chargen=chargen))


# button to progress the lifepath selection
class okButton(discord.ui.Button):

    # we need the chargen to take us to the next step and links
    def __init__(self, chargen, selection):
        self.chargen = chargen
        self.selection = selection
        super().__init__(emoji=discord.PartialEmoji.from_str("✅"), style=discord.ButtonStyle.green)

    # when pressed, the chargen takes over
    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
        await self.chargen.nextLayer(selection=self.selection)
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
