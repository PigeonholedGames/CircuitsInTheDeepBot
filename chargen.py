import asyncio
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
    await birth(thread, author)


# this method handles querying and messaging for birth lifepaths
async def birth(thread, author):
    charactermanager = ChargenManager(thread=thread, author=author)

    # first we get all the lifepaths for this age
    lifepaths = db.queryLifepaths(location="NEWATLANTIS", age="BIRTH")

    # and check that we actually got them
    if len(lifepaths) == 0:
        await thread.send("Something has gone terribly wrong, please contact us.")
        raise Exception("Lifepaths query empty.")

    # we make the embed to display the first lifepath
    embed = discord.Embed(title='Birth',
                          description='You don\'t remember much from your first few years on Earth, so you won\'t get any skills from this choice. Instead, this will tell us a little about who your parents were.',
                          color=0x288830)
    embed.set_footer(
        text="Browse through the lifepaths using the drop-down list and confirm your selection using the green button.")

    # then the drop-down menu with all the rest
    select = selectLifepath(charactermanager=charactermanager, lifepaths=lifepaths, placeholder='Who were you born to?', thingsillneedinthefuture='')

    # then the view that will house the drop-down list and the navigation buttons
    view = ButtonView(select=select, charactermanager=charactermanager, thingsillneedinthefuture='')

    # go! be free my lil message! be displayed!
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


# make an embed of lifepaths
async def makeembedlifepaths(title, description, aptitudes, skills):
    embed = discord.Embed(title=title, description=description, color=0x288830)

    if aptitudes is not None:
        embed.add_field(name=" ", value=aptitudes, inline=True)
        embed.add_field(name=" ", value=skills, inline=True)
        embed.set_footer(text="Use the red undo button to go back, or the green submit button to confirm your choice.")

    embed.set_footer(text="Browse through the lifepaths using the drop-down list and confirm your selection using the green button.")

    return embed


# this class handles displaying the drop-down list of lifepaths
class selectLifepath(discord.ui.Select):

    # constructor needs the charactermanager to pass onto its buttons, the list of lifepaths, the position of the currently displayed lifepath to be removed from the list, the placeholder text, and a miscellaneous thing thats there so its not a hassle adding it later
    def __init__(self, charactermanager, lifepaths, currentx='', placeholder='', thingsillneedinthefuture=''):
        self.charactermanager = charactermanager
        self.lifepaths = lifepaths
        self.currentx = currentx
        self.thingsillneedinthefuture = thingsillneedinthefuture

        # the options list is constructed from the lifepaths list minus the one being currently displayed
        options = []
        for x in range(len(lifepaths)):
            if x != currentx:
                options.append(discord.SelectOption(label=lifepaths[x][0], value=x, default=False))

        super().__init__(placeholder=placeholder, max_values=1, options=options)

    # once the user picks an option the embed is updated to display what they chose and a new drop-down list is generated
    async def callback(self, interaction: discord.Interaction):
        # get the index of the pressed option
        self.currentx = int(self.values[0])

        # make the new embed
        embed = await makeembedlifepaths(self.lifepaths[self.currentx][0], self.lifepaths[self.currentx][17],
                                         aptitudes=None, skills=None)
        # make the new drop-down list
        select = selectLifepath(charactermanager=self.charactermanager, lifepaths=self.lifepaths, currentx=self.currentx, placeholder=self.placeholder, thingsillneedinthefuture=self.thingsillneedinthefuture)
        # make the view with the two buttons
        view = ButtonView(select=select, charactermanager=self.charactermanager, thingsillneedinthefuture=self.thingsillneedinthefuture)
        # ship it
        await interaction.message.edit(embed=embed, view=view)
        try:
            await interaction.response.send_message(" ")
        except:
            pass


# button to progress the lifepath selection
class okButton(discord.ui.Button):

    # we need the chargenmanager to take us to the next step and also prob smth else in the future so yea, that
    def __init__(self, charactermanager, thingsillneedinthefuture):
        self.charactermanager = charactermanager
        self.thingsillneedinthefuture = thingsillneedinthefuture
        super().__init__(emoji=discord.PartialEmoji.from_str("✅"), style=discord.ButtonStyle.green)

    # when pressed, the chargenmanager takes over
    async def callback(self, interaction: discord.Interaction):
        await interaction.delete_original_response()
        self.charactermanager.nextLayer()
        return


# button to take us a step back
class undoButton(discord.ui.Button):
    # we need the chargenmanager to take us to the previous step and also prob smth else in the future so yea, that
    def __init__(self, charactermanager, thingsillneedinthefuture):
        self.charactermanager = charactermanager
        self.thingsillneedinthefuture = thingsillneedinthefuture
        super().__init__(emoji=discord.PartialEmoji.from_str("↩"), style=discord.ButtonStyle.red)

    # when pressed, the chargenmanager takes over
    async def callback(self, interaction: discord.Interaction):
        await interaction.delete_original_response()
        self.charactermanager.prevLayer()
        return


# makes a view with buttons and stuff
class ButtonView(discord.ui.View):

    def __init__(self, *, timeout=180, select, charactermanager, thingsillneedinthefuture):
        super().__init__(timeout=timeout)
        self.add_item(select)
        if charactermanager.getLayer() > 0:
            self.add_item(
                undoButton(charactermanager=charactermanager, thingsillneedinthefuture=thingsillneedinthefuture))

        self.add_item(
            okButton(charactermanager=charactermanager, thingsillneedinthefuture=thingsillneedinthefuture))


# oh boy here we go
class ChargenManager:

    def __init__(self, thread, author):
        self.thread = thread
        self.author = author
        self.currentlayer = 0
        self.character0 = character.Character(aptitudenames=db.queryAptitudeNames(),
                                              skillnames=db.querySkillNames(), server=self.thread.guild,
                                              thread=self.thread, player=self.author)

    # handles picking a birth lifepath
    async def layer0(self, thingsillneedinthefuture):
        self.currentlayer = 0

        # makes the character for this layer
        character0 = character(self.character0)

    # handles picking a childhood lifepath
    async def layer1(self, thingsillneedinthefuture):
        # hi we're here
        self.currentlayer = 1

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking an aptitude from childhood
    async def layer2(self, thingsillneedinthefuture):
        # hi we're here
        self.currentlayer = 1

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking skills from childhood
    async def layer3(self, thingsillneedinthefuture):
        # hi we're here
        self.currentlayer = 1

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking a teenage lifepath
    async def layer4(self, thingsillneedinthefuture):
        # hi we're here
        self.currentlayer = 1

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking an aptitude from teenage years
    async def layer5(self, thingsillneedinthefuture):
        # hi we're here
        self.currentlayer = 1

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking skills from teenage years
    async def layer6(self, thingsillneedinthefuture):
        # hi we're here
        self.currentlayer = 1

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking a young adult lifepath
    async def layer7(self, thingsillneedinthefuture):
        # hi we're here
        self.currentlayer = 1

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking an aptitude from young adulthood
    async def layer8(self, thingsillneedinthefuture):
        # hi we're here
        self.currentlayer = 1

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking skills from young adulthood
    async def layer9(self, thingsillneedinthefuture):
        # hi we're here
        self.currentlayer = 1

        # makes the character for this layer
        character1 = character(self.character0)

    # handles picking the first adult lifepath
    async def layer10(self, thingsillneedinthefuture):
        # hi we're here
        self.currentlayer = 1

        # makes the character for this layer
        character1 = character(self.character0)

    # moving ooooooon moving on
    async def nextLayer(self, thingsillneedinthefuture):
        if self.currentlayer == 0:
            self.layer1(thingsillneedinthefuture=thingsillneedinthefuture)
        elif self.currentlayer == 1:
            self.layer2()
        elif self.currentlayer == 2:
            self.layer3()
        elif self.currentlayer == 3:
            self.layer4()
        elif self.currentlayer == 4:
            self.layer5()
        elif self.currentlayer == 5:
            self.layer6()
        elif self.currentlayer == 6:
            self.layer7()
        elif self.currentlayer == 7:
            self.layer8()
        elif self.currentlayer == 8:
            self.layer9()
        elif self.currentlayer == 9:
            self.layer10()
        elif self.currentlayer == 10:
            self.layer11()
        elif self.currentlayer == 11:
            self.layer12()
        elif self.currentlayer == 12:
            self.layer13()
        elif self.currentlayer == 13:
            self.layer14()
        elif self.currentlayer == 14:
            self.layer15()

    # moving back moving baaaaaaaaaaaaaaaaack
    async def prevLayer(self, x):
        if self.currentlayer == 1:
            self.layer0()
        elif self.currentlayer == 2:
            self.layer1(x)
        elif self.currentlayer == 3:
            self.layer2()
        elif self.currentlayer == 4:
            self.layer3()
        elif self.currentlayer == 5:
            self.layer4()
        elif self.currentlayer == 6:
            self.layer5()
        elif self.currentlayer == 7:
            self.layer6()
        elif self.currentlayer == 8:
            self.layer7()
        elif self.currentlayer == 9:
            self.layer8()
        elif self.currentlayer == 10:
            self.layer9()
        elif self.currentlayer == 11:
            self.layer10()
        elif self.currentlayer == 12:
            self.layer11()
        elif self.currentlayer == 13:
            self.layer12()
        elif self.currentlayer == 14:
            self.layer13()

    def getLayer(self):
        return self.currentlayer
