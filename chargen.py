import discord
import db
import character


# this method handles initializing the character creation process
async def begin(thread, author):
    # pings the player otherwise they won't be added to the thread
    await thread.send(f"Hi {author.mention}, we'll make a character here.")
    # await asyncio.sleep(2.00)
    # explanation messages
    # await thread.send("Character creation in Circuits in the Deep uses a lifepath system.")
    # await asyncio.sleep(0.95)
    # await thread.send("This means that we'll go through the broad strokes of your backstory and you'll decide what you were doing at each stage of your life.")
    # await asyncio.sleep(0.95)
    # await thread.send("Your choices will grant you some stats and unlock different lifepaths later down the line.")
    # await asyncio.sleep(0.95)
    # await thread.send("Without further ado:")
    # await asyncio.sleep(0.95)
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
        self.messages = []
        self.lifepaths = []
        self.selectedskills = []

        # and some simple global ones
        self.thread = thread
        self.author = author
        self.currentlayer = None
        self.locations = db.queryLocations()
        if len(self.locations) == 0:
            self.thread.send("Something has gone terribly wrong, please contact us.")
            raise Exception("Locations query empty.")
        aptitudenamestemp = db.queryAptitudeNames()
        self.aptitudes = []
        for n in aptitudenamestemp:
            self.aptitudes.append(n[0])

    # handles picking trappings
    async def layer0(self):
        self.currentlayer = 0
        self.characters.append(character.Character(server=self.thread.guild, thread=self.thread, player=self.author))

        # first we get the trappings
        trappings = db.queryTrappings()

        # and check that we actually got them
        if len(trappings) == 0:
            await self.thread.send("Something has gone terribly wrong, please contact us.")
            raise Exception("Trappings query empty.")

        # we make the initial embed
        embed = discord.Embed(title='Trappings',
                              description='These will describe the role you\'ll end up filling within the crew, and offer you the core Aptitude and the Stuff you\'ll need to do that job.',
                              color=0x288830)
        embed.set_footer(
            text="Browse through the trappings using the drop-down list.")

        # then the drop-down menu
        select = selectTrappings(chargen=self, trappings=trappings, placeholder='Who are you?')

        # then the view which will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # GO! Message, I choose you!
        await self.thread.send(embed=embed, view=view)

    # handles picking a birth location
    async def layer1(self):
        # hi we're here
        self.currentlayer = 1

        # make the initial embed
        embed = discord.Embed(title='Birth',
                              description='OTHER LOCATIONS UNDER CONSTRUCTION :pensive:',
                              color=0x288830)
        embed.set_footer(text="Browse through the available locations using the drop-down list.")

        # then the drop-down menu
        select = selectLocation(chargen=self, locations=self.locations, placeholder='Where were you born?')

        # then the view which will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # GO! Message, I choose you!
        await self.thread.send(embed=embed, view=view)

    # handles picking a trapping aptitude in case that's necessary
    async def layerMinus1(self):

        # hi we're here
        self.currentlayer = -1

        # make the embed
        embed = discord.Embed(title='Trappings',
                              description='You\'ve picked Trappings that offer an Aptitude selection.',
                              color=0x288830)
        embed.set_footer(text='Browse through your options using the drop-down list.')

        select = selectAptitude(chargen=self, aptitudes=self.aptitudes,
                                placeholder='You get to pick only one of these.')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking a birth lifepath
    async def layer2(self):
        # hi we're here
        self.currentlayer = 2

        # first we get all the lifepaths for this age
        lifepaths = db.queryLifepaths(location=self.location[0], age="BIRTH")

        # and check that we actually got them
        if len(lifepaths) == 0:
            await self.thread.send("Something has gone terribly wrong, please contact us.")
            raise Exception("Lifepaths query empty.")

        # we make the initial embed
        embed = discord.Embed(title='Birth',
                              description='You don\'t remember much from your first few years on Earth, so you won\'t get any stats from this choice. Instead, this will tell us a little about who your parents were.',
                              color=0x288830)
        embed.set_footer(
            text="Browse through the lifepaths using the drop-down list.")

        # then the drop-down menu
        select = selectLifepath(chargen=self, lifepaths=lifepaths, placeholder='Who were you born to?')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking childhood location
    async def layer3(self):
        # hi we're here
        self.currentlayer = 3

        # make the initial embed
        embed = discord.Embed(title='Childhood',
                              description='OTHER LOCATIONS UNDER CONSTRUCTION :pensive:',
                              color=0x288830)
        embed.set_footer(text="Browse through the available locations using the drop-down list.")

        # then the drop-down menu
        select = selectLocation(chargen=self, locations=self.locations,
                                placeholder='Where were you during your childhood?')

        # then the view which will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # GO! Message, I choose you!
        await self.thread.send(embed=embed, view=view)

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

        # check if the conditions for them are fulfilled
        for x in range(len(lifepaths)):
            if x < len(lifepaths) and lifepaths[x][19] is not None and not await self.parseCondition(lifepaths[x][19]):
                lifepaths.pop(x)

        # we make the embed
        embed = discord.Embed(title='Childhood',
                              description='You can trace your affinity for certain skills all the way back here.',
                              color=0x288830)
        embed.set_footer(
            text='Browse through the lifepaths using the drop-down list.')

        # then the drop-down list
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

        # make the character for this layer
        self.characters.append(character.Character(aptitudes=self.characters[0].aptitudes,
                                                   skills=self.characters[0].skills,
                                                   server=self.characters[0].server, thread=self.characters[0].thread,
                                                   player=self.characters[0].player, name=self.characters[0].name,
                                                   stuff=self.characters[0].stuff, traits=self.characters[0].traits,
                                                   luck=self.characters[0].luck,
                                                   realization=self.characters[0].realization,
                                                   harm1=self.characters[0].harm1,
                                                   harm1clock=self.characters[0].harm1clock,
                                                   harm2=self.characters[0].harm2,
                                                   harm2clock=self.characters[0].harm2clock,
                                                   harm3=self.characters[0].harm3,
                                                   harm3clock=self.characters[0].harm3clock))

        # make the embed
        embed = discord.Embed(title='Childhood',
                              description='Which Aptitude did you develop throughout your childhood?',
                              color=0x288830)
        embed.set_footer(text='Browse through your options using the drop-down list.')

        # then the drop-down list
        aptitudes = []
        for x in range(2, 7):
            if self.lifepaths[len(self.lifepaths) - 1][x] is not None and self.characters[len(self.characters) - 1].getAptitude(self.lifepaths[len(self.lifepaths) - 1][x]) < 2:
                aptitudes.append(self.lifepaths[len(self.lifepaths) - 1][x])
        select = selectAptitude(chargen=self, aptitudes=aptitudes,
                                placeholder='You get to pick only one of these.')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking the first skill from childhood
    async def layer6(self):
        # hi we're here
        self.currentlayer = 6

        # makes the character for this layer
        self.characters.append(character.Character(aptitudes=self.characters[1].aptitudes,
                                                   skills=self.characters[1].skills,
                                                   server=self.characters[1].server, thread=self.characters[1].thread,
                                                   player=self.characters[1].player, name=self.characters[1].name,
                                                   stuff=self.characters[1].stuff, traits=self.characters[1].traits,
                                                   luck=self.characters[1].luck,
                                                   realization=self.characters[1].realization,
                                                   harm1=self.characters[1].harm1,
                                                   harm1clock=self.characters[1].harm1clock,
                                                   harm2=self.characters[1].harm2,
                                                   harm2clock=self.characters[1].harm2clock,
                                                   harm3=self.characters[1].harm3,
                                                   harm3clock=self.characters[1].harm3clock))

        # make the embed
        embed = discord.Embed(title='Childhood',
                              description='You developed two Skills during your childhood. This is the first.',
                              color=0x288830)
        embed.set_footer(text='Browse through your options using the drop-down list.')

        # then the drop-down list
        skills = []
        for x in range(7, 17):
            if self.lifepaths[len(self.lifepaths) - 1][x] is not None and self.characters[len(self.characters) - 1].getSkill(self.lifepaths[len(self.lifepaths) - 1][x]) < 2:
                skills.append(self.lifepaths[len(self.lifepaths) - 1][x])
        select = selectSkill(chargen=self, skills=skills, placeholder='You get to pick two of these.')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking the second skill from childhood
    async def layer7(self):
        # hi we're here
        self.currentlayer = 7

        # makes the character for this layer
        self.characters.append(character.Character(aptitudes=self.characters[2].aptitudes,
                                                   skills=self.characters[2].skills,
                                                   server=self.characters[2].server, thread=self.characters[2].thread,
                                                   player=self.characters[2].player, name=self.characters[2].name,
                                                   stuff=self.characters[2].stuff, traits=self.characters[2].traits,
                                                   luck=self.characters[2].luck,
                                                   realization=self.characters[2].realization,
                                                   harm1=self.characters[2].harm1,
                                                   harm1clock=self.characters[2].harm1clock,
                                                   harm2=self.characters[2].harm2,
                                                   harm2clock=self.characters[2].harm2clock,
                                                   harm3=self.characters[2].harm3,
                                                   harm3clock=self.characters[2].harm3clock))

        # make the embed
        embed = discord.Embed(title='Childhood',
                              description='You developed two Skills during your childhood. This is the second.',
                              color=0x288830)
        embed.set_footer(text='Browse through your options using the drop-down list.')

        # then the drop-down list
        skills = []
        for x in range(7, 17):
            if self.lifepaths[len(self.lifepaths) - 1][x] is not None and self.lifepaths[len(self.lifepaths) - 1][x] is not self.selectedskills[len(self.selectedskills) - 1] and self.characters[len(self.characters) - 1].getSkill(self.lifepaths[len(self.lifepaths) - 1][x]) < 2:
                skills.append(self.lifepaths[len(self.lifepaths) - 1][x])
        select = selectSkill(chargen=self, skills=skills, placeholder='This is your second pick from these.')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking a teen location
    async def layer8(self):
        # hi we're here
        self.currentlayer = 8

        # make the initial embed
        embed = discord.Embed(title='Teenage Years',
                              description='OTHER LOCATIONS UNDER CONSTRUCTION :pensive:',
                              color=0x288830)
        embed.set_footer(text="Browse through the available locations using the drop-down list.")

        # then the drop-down menu
        select = selectLocation(chargen=self, locations=self.locations,
                                placeholder='Where were you during your teenage years?')

        # then the view which will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # GO! Message, I choose you!
        await self.thread.send(embed=embed, view=view)

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

        # check if the conditions for them are fulfilled
        for x in range(len(lifepaths)):
            if lifepaths[x][19] is not None and not self.parseCondition(lifepaths[x][19]):
                del lifepaths[x]

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
        self.characters.append(character.Character(aptitudes=self.characters[3].aptitudes,
                                                   skills=self.characters[3].skills,
                                                   server=self.characters[3].server, thread=self.characters[3].thread,
                                                   player=self.characters[3].player, name=self.characters[3].name,
                                                   stuff=self.characters[3].stuff, traits=self.characters[3].traits,
                                                   luck=self.characters[3].luck,
                                                   realization=self.characters[3].realization,
                                                   harm1=self.characters[3].harm1,
                                                   harm1clock=self.characters[3].harm1clock,
                                                   harm2=self.characters[3].harm2,
                                                   harm2clock=self.characters[3].harm2clock,
                                                   harm3=self.characters[3].harm3,
                                                   harm3clock=self.characters[3].harm3clock))
        # make the embed
        embed = discord.Embed(title='Teenage Years',
                              description='What Aptitude made you stand out as a teen?',
                              color=0x288830)
        embed.set_footer(text='Browse through your options using the drop-down list.')

        # then the drop-down list
        aptitudes = []
        for x in range(2, 7):
            if self.lifepaths[len(self.lifepaths) - 1][x] is not None and self.characters[len(self.characters) - 1].getAptitude(self.lifepaths[len(self.lifepaths) - 1][x]) < 2:
                aptitudes.append(self.lifepaths[len(self.lifepaths) - 1][x])
        select = selectAptitude(chargen=self, aptitudes=aptitudes,
                                placeholder='You get to pick only one of these.')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking the first skill from the teenage years
    async def layer11(self):
        # hi we're here
        self.currentlayer = 11

        # makes the character for this layer
        self.characters.append(character.Character(aptitudes=self.characters[4].aptitudes,
                                                   skills=self.characters[4].skills,
                                                   server=self.characters[4].server, thread=self.characters[4].thread,
                                                   player=self.characters[4].player, name=self.characters[4].name,
                                                   stuff=self.characters[4].stuff, traits=self.characters[4].traits,
                                                   luck=self.characters[4].luck,
                                                   realization=self.characters[4].realization,
                                                   harm1=self.characters[4].harm1,
                                                   harm1clock=self.characters[4].harm1clock,
                                                   harm2=self.characters[4].harm2,
                                                   harm2clock=self.characters[4].harm2clock,
                                                   harm3=self.characters[4].harm3,
                                                   harm3clock=self.characters[4].harm3clock))

        # make the embed
        embed = discord.Embed(title='Teenage Years',
                              description='You developed two Skills during your teenage years. This is the first.',
                              color=0x288830)
        embed.set_footer(text='Browse through your options using the drop-down list.')

        # then the drop-down list
        skills = []
        for x in range(7, 17):
            if self.lifepaths[len(self.lifepaths) - 1][x] is not None and self.characters[len(self.characters) - 1].getSkill(self.lifepaths[len(self.lifepaths) - 1][x]) < 2:
                skills.append(self.lifepaths[len(self.lifepaths) - 1][x])
        select = selectSkill(chargen=self, skills=skills, placeholder='You get to pick two of these.')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking the second skill from the teenage years
    async def layer12(self):
        # hi we're here
        self.currentlayer = 12
        # makes the character for this layer
        self.characters.append(character.Character(aptitudes=self.characters[5].aptitudes,
                                                   skills=self.characters[5].skills,
                                                   server=self.characters[5].server, thread=self.characters[5].thread,
                                                   player=self.characters[5].player, name=self.characters[5].name,
                                                   stuff=self.characters[5].stuff, traits=self.characters[5].traits,
                                                   luck=self.characters[5].luck,
                                                   realization=self.characters[5].realization,
                                                   harm1=self.characters[5].harm1,
                                                   harm1clock=self.characters[5].harm1clock,
                                                   harm2=self.characters[5].harm2,
                                                   harm2clock=self.characters[5].harm2clock,
                                                   harm3=self.characters[5].harm3,
                                                   harm3clock=self.characters[5].harm3clock))

        # make the embed
        embed = discord.Embed(title='Childhood',
                              description='You developed two Skills during your childhood. This is the second.',
                              color=0x288830)
        embed.set_footer(text='Browse through your options using the drop-down list.')

        # then the drop-down list
        skills = []
        for x in range(7, 17):
            if self.lifepaths[len(self.lifepaths) - 1][x] is not None and self.lifepaths[len(self.lifepaths) - 1][x] is not self.selectedskills[len(self.selectedskills) - 1] and self.characters[len(self.characters) - 1].getSkill(self.lifepaths[len(self.lifepaths) - 1][x]) < 2:
                skills.append(self.lifepaths[len(self.lifepaths) - 1][x])
        select = selectSkill(chargen=self, skills=skills, placeholder='This is your second pick from these.')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

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
        self.characters.append(character.Character(aptitudes=self.characters[6].aptitudes,
                                                   skills=self.characters[6].skills,
                                                   server=self.characters[6].server, thread=self.characters[6].thread,
                                                   player=self.characters[6].player, name=self.characters[6].name,
                                                   stuff=self.characters[6].stuff, traits=self.characters[6].traits,
                                                   luck=self.characters[6].luck,
                                                   realization=self.characters[6].realization,
                                                   harm1=self.characters[6].harm1,
                                                   harm1clock=self.characters[6].harm1clock,
                                                   harm2=self.characters[6].harm2,
                                                   harm2clock=self.characters[6].harm2clock,
                                                   harm3=self.characters[6].harm3,
                                                   harm3clock=self.characters[6].harm3clock))

        # make the embed
        embed = discord.Embed(title='Childhood',
                              description='Which Aptitude did you develop throughout your childhood?',
                              color=0x288830)
        embed.set_footer(text='Browse through your options using the drop-down list.')

        # then the drop-down list
        aptitudes = []
        for x in range(2, 7):
            if self.lifepaths[len(self.lifepaths) - 1][x] is not None and self.characters[len(self.characters) - 1].getAptitude(self.lifepaths[len(self.lifepaths) - 1][x]) < 2:
                aptitudes.append(self.lifepaths[len(self.lifepaths) - 1][x])
        select = selectAptitude(chargen=self, aptitudes=aptitudes,
                                placeholder='You get to pick only one of these.')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking the first skill from young adulthood
    async def layer16(self):
        # hi we're here
        self.currentlayer = 11

        # makes the character for this layer
        self.characters.append(character.Character(aptitudes=self.characters[7].aptitudes,
                                                   skills=self.characters[7].skills,
                                                   server=self.characters[7].server, thread=self.characters[7].thread,
                                                   player=self.characters[7].player, name=self.characters[7].name,
                                                   stuff=self.characters[7].stuff, traits=self.characters[7].traits,
                                                   luck=self.characters[7].luck,
                                                   realization=self.characters[7].realization,
                                                   harm1=self.characters[7].harm1,
                                                   harm1clock=self.characters[7].harm1clock,
                                                   harm2=self.characters[7].harm2,
                                                   harm2clock=self.characters[7].harm2clock,
                                                   harm3=self.characters[7].harm3,
                                                   harm3clock=self.characters[7].harm3clock))

        # make the embed
        embed = discord.Embed(title='Childhood',
                              description='You developed two Skills during your childhood. This is the first.',
                              color=0x288830)
        embed.set_footer(text='Browse through your options using the drop-down list.')

        # then the drop-down list
        skills = []
        for x in range(7, 17):
            if self.lifepaths[len(self.lifepaths) - 1][x] is not None and self.characters[len(self.characters) - 1].getSkill(self.lifepaths[len(self.lifepaths) - 1][x]) < 2:
                skills.append(self.lifepaths[len(self.lifepaths) - 1][x])
        select = selectSkill(chargen=self, skills=skills, placeholder='You get to pick two of these.')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # handles picking the second skill from young adulthood
    async def layer17(self):
        # hi we're here
        self.currentlayer = 12
        # makes the character for this layer
        self.characters.append(character.Character(aptitudes=self.characters[8].aptitudes,
                                                   skills=self.characters[8].skills,
                                                   server=self.characters[8].server, thread=self.characters[8].thread,
                                                   player=self.characters[8].player, name=self.characters[8].name,
                                                   stuff=self.characters[8].stuff, traits=self.characters[8].traits,
                                                   luck=self.characters[8].luck,
                                                   realization=self.characters[8].realization,
                                                   harm1=self.characters[8].harm1,
                                                   harm1clock=self.characters[8].harm1clock,
                                                   harm2=self.characters[8].harm2,
                                                   harm2clock=self.characters[8].harm2clock,
                                                   harm3=self.characters[8].harm3,
                                                   harm3clock=self.characters[8].harm3clock))

        # make the embed
        embed = discord.Embed(title='Childhood',
                              description='You developed two Skills during your childhood. This is the second.',
                              color=0x288830)
        embed.set_footer(text='Browse through your options using the drop-down list.')

        # then the drop-down list
        skills = []
        for x in range(7, 17):
            if self.lifepaths[len(self.lifepaths) - 1][x] is not None and self.lifepaths[len(self.lifepaths) - 1][x] is not self.selectedskills[len(self.selectedskills) - 1] and self.characters[len(self.characters) - 1].getSkill(self.lifepaths[len(self.lifepaths) - 1][x]) < 2:
                skills.append(self.lifepaths[len(self.lifepaths) - 1][x])
        select = selectSkill(chargen=self, skills=skills, placeholder='This is your second pick from these.')

        # then the view that will house the drop-down list and the navigation buttons
        view = ButtonView(select=select, chargen=self)

        # go! be free my lil message! be displayed!
        await self.thread.send(embed=embed, view=view)

    # carry ooooooon carry on
    async def nextLayer(self, selection=None, selection1=None):

        # trappings
        if self.currentlayer == 0:
            if selection is None:
                await self.thread.send("Something has gone terribly wrong, please contact us.")
                raise Exception("Trappings Missing")

            for x in range(3, 9):
                if selection[x] is not None:
                    self.characters[len(self.characters) - 1].addStuff(selection[x])

            if selection[2] is not None:
                self.characters[len(self.characters) - 1].incrementAptitude(thread=self.thread, name=selection[2], x=1)
                await self.layer1()
            else:
                await self.layerMinus1()

        # optional trappings aptitude selection
        elif self.currentlayer == -1:
            if selection is None:
                await self.thread.send("Something has gone terribly wrong, please contact us.")
                raise Exception("Trappings Aptitude Selection Missing")
            self.characters[len(self.characters) - 1].incrementAptitude(thread=self.thread, name=selection, x=1)
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
            self.links.append(selection[1])
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
            self.lifepaths.append(selection)
            self.links.append(self.links[0] + "," + selection[1])
            await self.layer5()

        # child aptitude
        elif self.currentlayer == 5:
            # lock in the aptitude selection
            self.characters[len(self.characters) - 1].incrementAptitude(thread=self.thread, name=selection, x=1)
            await self.layer6()

        # child skill 1
        elif self.currentlayer == 6:
            self.characters[len(self.characters) - 1].incrementSkill(thread=self.thread, name=selection, x=1)
            self.selectedskills.append(selection)
            await self.layer7()

        # child skill 2
        elif self.currentlayer == 7:
            self.characters[len(self.characters) - 1].incrementSkill(thread=self.thread, name=selection, x=1)
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
                raise Exception("Child Lifepath Links Missing")
            self.lifepaths.append(selection)
            self.links.append(self.links[1] + "," + selection[1])
            await self.layer10()

        # teen aptitude
        elif self.currentlayer == 10:
            self.characters[len(self.characters) - 1].incrementAptitude(thread=self.thread, name=selection, x=1)
            await self.layer11()

        # teen skill 1
        elif self.currentlayer == 11:
            self.characters[len(self.characters) - 1].incrementSkill(thread=self.thread, name=selection, x=1)
            self.selectedskills.append(selection)
            await self.layer12()

        # teen skill 2
        elif self.currentlayer == 12:
            self.characters[len(self.characters) - 1].incrementSkill(thread=self.thread, name=selection, x=1)
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
                raise Exception("Child Lifepath Links Missing")
            self.lifepaths.append(selection)
            self.links.append(self.links[2] + "," + selection[1])
            await self.layer15()

        # ya aptitude
        elif self.currentlayer == 15:
            self.characters[len(self.characters) - 1].incrementAptitude(thread=self.thread, name=selection, x=1)
            await self.layer16()

        # ya skill 1
        elif self.currentlayer == 16:
            self.characters[len(self.characters) - 1].incrementSkill(thread=self.thread, name=selection, x=1)
            self.selectedskills.append(selection)
            await self.layer17()

        # ya skill 2
        elif self.currentlayer == 17:
            self.characters[len(self.characters) - 1].incrementSkill(thread=self.thread, name=selection, x=1)
            await self.layer18()

    # as if nothing really matters
    async def prevLayer(self):
        # trappings
        if self.currentlayer == 0:
            self.characters.pop()
            await self.layer0()
        # optional trappings aptitude selection
        if self.currentlayer == -1:
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
            self.lifepaths.pop()
            self.links.pop()
            await self.layer4()
        # child skill 1
        elif self.currentlayer == 6:
            self.characters.pop()
            await self.layer5()
        # child skill 2
        elif self.currentlayer == 7:
            self.characters.pop()
            self.selectedskills.pop()
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
            self.lifepaths.pop()
            self.links.pop()
            await self.layer9()
        # teen skill 1
        elif self.currentlayer == 11:
            self.characters.pop()
            await self.layer10()
        # teen skill 2
        elif self.currentlayer == 12:
            self.characters.pop()
            self.selectedskills.pop()
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
            self.lifepaths.pop()
            self.links.pop()
            await self.layer14()
        # ya skill 1
        elif self.currentlayer == 16:
            self.characters.pop()
            await self.layer15()
        # ya skill 2
        elif self.currentlayer == 17:
            self.characters.pop()
            self.selectedskills.pop()
            await self.layer16()

    def getLayer(self):
        return self.currentlayer

    # this function returns true if the condition of a lifepath is met
    async def parseCondition(self, condition):
        # split the condition into parts
        temptokens = condition.split(" ")
        # cleanup the input
        tokens = [token.strip() for token in temptokens]
        # go
        return await self.solveExpression(tokens, 0)

    # oh boy, takes a tokens list, a position in it, and does stuff to it
    async def solveExpression(self, tokens, x):

        # if there's only one element in the list, every operation has been completed and only the final result remains so we return it
        if len(tokens) == 1:
            return tokens[0]

        # before we do anything, prevent index errors
        if x >= len(tokens):
            x = 0

        # if the token is not an operator, move on, this is here for efficiency, the method will recur if a non-operator not on this list appears
        if tokens[x] in [True, False, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]:
            return await self.solveExpression(tokens, x + 1)

        # if the token refers to one of the misfits stats, replace the text with that stat score
        if tokens[x] in self.aptitudes:
            tokens[x] = self.characters[-1].getAptitude(tokens[x])
            return await self.solveExpression(tokens, x + 1)

        # if the token is opening parentheses, check if theres only one element inside them in order to delete them
        if tokens[x] == "(":
            if tokens[x + 2] == ")":
                del tokens[x]
                del tokens[x + 2]
            return await self.solveExpression(tokens, x + 1)

        # if the token is closing parentheses, check if theres only one element inside them in order to delete them otherwise go back to the first parentheses
        if tokens[x] == ")":
            if tokens[x - 2] == "(":
                del tokens[x]
                del tokens[x + 2]
            return await self.solveExpression(tokens, tokens.index("("))

        # if the token is multiplication, check that we aren't violating left to right or are trying to use it on parentheses and try to execute it, if there's an error, probably due to an aptitude conversion not having been completed, move on
        if tokens[x] == "*":
            if (not x <= 2 or x <= 2 and tokens[x - 2] not in ["*", "/"]) and (not x <= 1 or x <= 1 and tokens[x - 1] != ")") and (not x < len(tokens) - 1 or x < len(tokens) - 1 and tokens[x + 1] != "("):
                try:
                    tokens[x - 1] = int(tokens[x - 1]) * int(tokens[x + 1])
                    del tokens[x + 1:x + 3]
                except:
                    pass
            return await self.solveExpression(tokens, x + 1)

        # if the token is division, check that we aren't violating left to right or are trying to use it on parentheses and try to execute it, if there's an error, probably due to an aptitude conversion not having been completed, move on
        if tokens[x] == "/":
            if (not x <= 2 or x <= 2 and tokens[x - 2] not in ["*", "/"]) and (not x <= 1 or x <= 1 and tokens[x - 1] != ")") and (not x < len(tokens) - 1 or x < len(tokens) - 1 and tokens[x + 1] != "("):
                try:
                    tokens[x - 1] = int(tokens[x - 1]) / int(tokens[x + 1])
                    del tokens[x:x + 2]
                except:
                    pass
            return await self.solveExpression(tokens, x + 1)

        # if the token is addition, check that we aren't violating order of operations or are trying to use it on parentheses and try to execute it, if there's an error, probably due to an aptitude conversion not having been completed, move on
        if tokens[x] == "+":
            if (not x <= 2 or x <= 2 and tokens[x - 2] not in ["*", "/", "+", "-"]) and (not x <= 1 or x <= 1 and tokens[x - 1] != ")") and (not x < len(tokens) - 1 or x < len(tokens) - 1 and tokens[x + 1] != "(") and (not x < len(tokens) - 2 or x < len(tokens) - 2 and tokens[x + 2] not in ["*", "/"]):
                try:
                    tokens[x - 1] = int(tokens[x - 1]) + int(tokens[x + 1])
                    del tokens[x:x + 2]
                except:
                    pass
            return await self.solveExpression(tokens, x + 1)

        # if the token is subtraction, check that we aren't violating order of operations or are trying to use it on parentheses and try to execute it, if there's an error, probably due to an aptitude conversion not having been completed, move on
        if tokens[x] == "-":
            if (not x <= 2 or x <= 2 and tokens[x - 2] not in ["*", "/", "+", "-"]) and (not x <= 1 or x <= 1 and tokens[x - 1] != ")") and (not x < len(tokens) - 1 or x < len(tokens) - 1 and tokens[x + 1] != "(") and (not x < len(tokens) - 2 or x < len(tokens) - 2 and tokens[x + 2] not in ["*", "/"]):
                try:
                    tokens[x - 1] = int(tokens[x - 1]) - int(tokens[x + 1])
                    del tokens[x:x + 2]
                except:
                    pass
            return await self.solveExpression(tokens, x + 1)

        # if the token is less than, check that we aren't violating order of operations or are trying to use it on parentheses and try to execute it, if there's an error, probably due to an aptitude conversion not having been completed, move on
        if tokens[x] == "<":
            if (not x <= 2 or x <= 2 and tokens[x - 2] not in ["*", "/", "+", "-", "<", ">", "=", "==", "<=", "=<", ">=", "=<", "!=", "=/="]) and (not x <= 1 or x <= 1 and tokens[x - 1] != ")") and (not x < len(tokens) - 1 or x < len(tokens) - 1 and tokens[x + 1] != "(") and (not x < len(tokens) - 2 or x < len(tokens) - 2 and tokens[x + 2] not in ["*", "/", "+", "-"]):
                try:
                    tokens[x - 1] = int(tokens[x - 1]) < int(tokens[x + 1])
                    del tokens[x:x + 2]
                except:
                    pass
            return await self.solveExpression(tokens, x + 1)

        # if the token is greater than, check that we aren't violating order of operations or are trying to use it on parentheses and try to execute it, if there's an error, probably due to an aptitude conversion not having been completed, move on
        if tokens[x] == ">":
            if (not x <= 2 or x <= 2 and tokens[x - 2] not in ["*", "/", "+", "-", "<", ">", "=", "==", "<=", "=<", ">=", "=<", "!=", "=/="]) and (not x <= 1 or x <= 1 and tokens[x - 1] != ")") and (not x < len(tokens) - 1 or x < len(tokens) - 1 and tokens[x + 1] != "(") and (not x < len(tokens) - 2 or x < len(tokens) - 2 and tokens[x + 2] not in ["*", "/", "+", "-"]):
                try:
                    tokens[x - 1] = int(tokens[x - 1]) > int(tokens[x + 1])
                    del tokens[x:x + 2]
                except:
                    pass
            return await self.solveExpression(tokens, x + 1)

        # if the token is equals, check that we aren't violating order of operations or are trying to use it on parentheses and try to execute it, if there's an error, probably due to an aptitude conversion not having been completed, move on
        if tokens[x] == "=" or tokens[x] == "==":
            if (not x <= 2 or x <= 2 and tokens[x - 2] not in ["*", "/", "+", "-", "<", ">", "=", "==", "<=", "=<", ">=", "=<", "!=", "=/="]) and (not x <= 1 or x <= 1 and tokens[x - 1] != ")") and (not x < len(tokens) - 1 or x < len(tokens) - 1 and tokens[x + 1] != "(") and (not x < len(tokens) - 2 or x < len(tokens) - 2 and tokens[x + 2] not in ["*", "/", "+", "-"]):
                try:
                    tokens[x - 1] = int(tokens[x - 1]) == int(tokens[x + 1])
                    del tokens[x:x + 2]
                except:
                    pass
            return await self.solveExpression(tokens, x + 1)

        # if the token is less or equal than, check that we aren't violating order of operations or are trying to use it on parentheses and try to execute it, if there's an error, probably due to an aptitude conversion not having been completed, move on
        if tokens[x] == "<=" or tokens[x] == "=<":
            if (not x <= 2 or x <= 2 and tokens[x - 2] not in ["*", "/", "+", "-", "<", ">", "=", "==", "<=", "=<", ">=", "=<", "!=", "=/="]) and (not x <= 1 or x <= 1 and tokens[x - 1] != ")") and (not x < len(tokens) - 1 or x < len(tokens) - 1 and tokens[x + 1] != "(") and (not x < len(tokens) - 2 or x < len(tokens) - 2 and tokens[x + 2] not in ["*", "/", "+", "-"]):
                try:
                    tokens[x - 1] = int(tokens[x - 1]) <= int(tokens[x + 1])
                    del tokens[x:x + 2]
                except:
                    pass
            return await self.solveExpression(tokens, x + 1)

        # if the token is greater or equal than, check that we aren't violating order of operations or are trying to use it on parentheses and try to execute it, if there's an error, probably due to an aptitude conversion not having been completed, move on
        if tokens[x] == ">=" or tokens[x] == "=>":
            if (not x <= 2 or x <= 2 and tokens[x - 2] not in ["*", "/", "+", "-", "<", ">", "=", "==", "<=", "=<", ">=", "=<", "!=", "=/="]) and (not x <= 1 or x <= 1 and tokens[x - 1] != ")") and (not x < len(tokens) - 1 or x < len(tokens) - 1 and tokens[x + 1] != "(") and (not x < len(tokens) - 2 or x < len(tokens) - 2 and tokens[x + 2] not in ["*", "/", "+", "-"]):
                try:
                    tokens[x - 1] = int(tokens[x - 1]) >= int(tokens[x + 1])
                    del tokens[x:x + 2]
                except:
                    pass
            return await self.solveExpression(tokens, x + 1)

        # if the token is not equals, check that we aren't violating order of operations or are trying to use it on parentheses and try to execute it, if there's an error, probably due to an aptitude conversion not having been completed, move on
        if tokens[x] == "!=" or tokens[x] == "=/=":
            if (not x <= 2 or x <= 2 and tokens[x - 2] not in ["*", "/", "+", "-", "<", ">", "=", "==", "<=", "=<", ">=", "=<", "!=", "=/="]) and (not x <= 1 or x <= 1 and tokens[x - 1] != ")") and (not x < len(tokens) - 1 or x < len(tokens) - 1 and tokens[x + 1] != "(") and (not x < len(tokens) - 2 or x < len(tokens) - 2 and tokens[x + 2] not in ["*", "/", "+", "-"]):
                try:
                    tokens[x - 1] = int(tokens[x - 1]) != int(tokens[x + 1])
                    del tokens[x:x + 2]
                except:
                    pass
            return await self.solveExpression(tokens, x + 1)

        # if the token is NOT, then check that we're operating on a boolean before doing it
        if tokens[x] == "NOT":
            if tokens[x + 1] in [True, False]:
                tokens[x] = not tokens[x + 1]
                del tokens[x + 1]
            return await self.solveExpression(tokens, x + 1)

        # if the token is AND, check that we're not violating order of operations and that we're working on booleans before doing it
        if tokens[x] == "AND":
            if (not x <= 2 or x <= 2 and tokens[x - 2] not in ["NOT", "AND"]) and (not x <= 1 or x <= 1 and tokens[x - 1] in [True, False]) and (not x < len(tokens) - 1 or x < len(tokens) - 1 and tokens[x + 1] in [True, False]):
                tokens[x - 1] = tokens[x - 1] and tokens[x + 1]
                del tokens[x:x + 2]
            return await self.solveExpression(tokens, x + 1)

        # if the token is OR, check that we're not violating order of operations and that we're working on booleans before doing it
        if tokens[x] == "OR":
            if (not x <= 2 or (x <= 2 and tokens[x - 2] not in ["NOT", "AND", "OR"])) and (not x <= 1 or x <= 1 and tokens[x - 1] in [True, False]) and (not x < len(tokens) - 1 or x < len(tokens) - 1 and tokens[x + 1] in [True, False]) and (not x < len(tokens) - 2 or x < len(tokens) - 2 and tokens[x + 2] not in ["NOT", "AND"]):
                tokens[x - 1] = tokens[x - 1] or tokens[x + 1]
                del tokens[x:x + 2]
            return await self.solveExpression(tokens, x + 1)

        # love recursion, i said, lying through my teeth
        return await self.solveExpression(tokens, x + 1)


# this class handles displaying the drop-down list of lifepaths
class selectTrappings(discord.ui.Select):

    # constructor needs the chargen to pass onto its buttons, the list of lifepaths, the position of the currently displayed lifepath to be removed from the list, and the placeholder text
    def __init__(self, chargen, trappings, position=None, placeholder=''):
        self.chargen = chargen
        self.trappings = trappings
        self.position = position

        # the options list is constructed from the lifepaths list minus the one being currently displayed
        options = []
        for x in range(len(trappings)):
            if x != position:
                options.append(
                    discord.SelectOption(label=trappings[x][0].title(), description=trappings[x][1][:99], value=x,
                                         default=False))

        if not options:
            options.append(
                discord.SelectOption(label=trappings[position][0].title(), description=trappings[position][1][:99],
                                     value=x, default=False))

        super().__init__(placeholder=placeholder, max_values=1, options=options)

    # once the user picks an option the embed is updated to display what they chose and a new drop-down list is generated
    async def callback(self, interaction: discord.Interaction):
        # get the index of the selected option
        self.position = int(self.values[0])
        # make the new embed
        if self.trappings[self.position][2] is not None:
            embed = discord.Embed(title=self.trappings[self.position][0].title(),
                                  description=self.trappings[self.position][
                                                  1] + '\n You\'ll be in your element when you can {} your way out of trouble'.format(
                                      self.trappings[self.position][2].title()))
        else:
            embed = discord.Embed(title=self.trappings[self.position][0].title(),
                                  description=self.trappings[self.position][
                                                  1] + '\n You\'ll get an additional choice for the Aptitude you make use of the most')
        embed.set_footer(
            text='Browse through the trappings using the drop-down list and confirm your selection using the green tick button.')
        # make the new drop-down list
        select = selectTrappings(chargen=self.chargen, trappings=self.trappings, position=self.position,
                                 placeholder=self.placeholder)
        # make the view with the two buttons
        view = ButtonView(select=select, chargen=self.chargen, selection=self.trappings[self.position])
        # ship it
        await interaction.message.edit(embed=embed, view=view)
        try:
            await interaction.response.send_message(" ")
        except:
            pass


# this class handles displaying the drop-down list of lifepaths
class selectLocation(discord.ui.Select):

    # constructor needs the chargen to pass onto its buttons, the list of lifepaths, the position of the currently displayed lifepath to be removed from the list, and the placeholder text
    def __init__(self, chargen, locations, position=None, placeholder=''):
        self.chargen = chargen
        self.locations = locations
        self.position = position

        # the options list is constructed from the lifepaths list minus the one being currently displayed
        options = []
        for x in range(len(locations)):
            if x != position:
                options.append(
                    discord.SelectOption(label=locations[x][1], description=locations[x][2][:99], value=x,
                                         default=False))

        if not options:
            options.append(
                discord.SelectOption(label=locations[position][1], description=locations[position][2][:99],
                                     value=x, default=False))

        super().__init__(placeholder=placeholder, max_values=1, options=options)

    # once the user picks an option the embed is updated to display what they chose and a new drop-down list is generated
    async def callback(self, interaction: discord.Interaction):
        # get the index of the selected option
        self.position = int(self.values[0])
        # make the new embed
        embed = discord.Embed(title=self.locations[self.position][1], description=self.locations[self.position][2])
        embed.set_footer(
            text='Browse through the locations using the drop-down list and confirm your selection using the green tick button.')
        # make the new drop-down list
        select = selectLocation(chargen=self.chargen, locations=self.locations, position=self.position,
                                placeholder=self.placeholder)
        # make the view with the two buttons
        view = ButtonView(select=select, chargen=self.chargen, selection=self.locations[self.position][0])
        # ship it
        await interaction.message.edit(embed=embed, view=view)
        try:
            await interaction.response.send_message(" ")
        except:
            pass


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
                options.append(
                    discord.SelectOption(label=lifepaths[x][0], description=lifepaths[x][17][:99], value=x,
                                         default=False))

        super().__init__(placeholder=placeholder, max_values=1, options=options)

    # once the user picks an option the embed is updated to display what they chose and a new drop-down list is generated
    async def callback(self, interaction: discord.Interaction):
        # get the index of the selected option
        self.position = int(self.values[0])

        # make the new embed
        embed = discord.Embed(title=self.lifepaths[self.position][0],
                              description=self.lifepaths[self.position][17][:99], color=0x288830)

        if self.chargen.getLayer() > 0:
            embed.set_footer(
                text="Use the red undo button to go back, or the green tick button to confirm your choice.")
        else:
            embed.set_footer(text="Use the green tick button to confirm your choice.")

        # make the new drop-down list
        select = selectLifepath(chargen=self.chargen, lifepaths=self.lifepaths, position=self.position,
                                placeholder=self.placeholder)
        # make the view with the two buttons
        view = ButtonView(select=select, chargen=self.chargen, selection=self.lifepaths[self.position])
        # ship it
        await interaction.message.edit(embed=embed, view=view)
        try:
            await interaction.response.send_message(" ")
        except:
            pass


class selectAptitude(discord.ui.Select):

    # constructor needs the chargen to pass onto its buttons, the selected lifepath, the position of the currently displayed aptitude to be removed from the list, and the placeholder text
    def __init__(self, chargen, aptitudes, position=None, placeholder=''):
        self.chargen = chargen
        self.aptitudes = aptitudes
        self.position = position

        # the aptitude options
        options = []
        for x in range(len(aptitudes)):
            if x != self.position:
                printables = db.queryAptitudeToPrint(aptitudes[x])
                options.append(
                    discord.SelectOption(label=printables[0][0].title(), description=printables[0][1][:99], value=x,
                                         default=False))
        if not options:
            printables = db.queryAptitudeToPrint(aptitudes[self.position])
            options.append(
                discord.SelectOption(label=printables[0][0].title(), description=printables[0][1][:99], value=x,
                                     default=False))

        super().__init__(placeholder=placeholder, max_values=1, options=options)

    # once the user picks an option the embed is updated to display what they chose and a new drop-down list is generated
    async def callback(self, interaction: discord.Interaction):
        # get the index of the selected option
        self.position = int(self.values[0])

        # get the printables
        printables = db.queryAptitudeToPrint(self.aptitudes[self.position])
        # make the new embed
        embed = discord.Embed(title=printables[0][0].title(), description=printables[0][1][:99], color=0x288830)
        embed.set_footer(
            text='Browse through the Aptitudes using the drop-down list and confirm your selection using the green tick button.')
        # make the new drop-down list
        select = selectAptitude(chargen=self.chargen, aptitudes=self.aptitudes, position=self.position,
                                placeholder=self.placeholder)
        # make the view with the two buttons
        view = ButtonView(select=select, chargen=self.chargen, selection=self.aptitudes[self.position])
        # ship it
        await interaction.message.edit(embed=embed, view=view)
        try:
            await interaction.response.send_message(" ")
        except:
            pass


class selectSkill(discord.ui.Select):

    # constructor needs the chargen to pass onto its buttons, the selected skills, the position of the currently displayed aptitude to be removed from the list, and the placeholder text
    def __init__(self, chargen, skills, position=None, placeholder=''):
        self.chargen = chargen
        self.skills = skills
        self.position = position

        # the aptitude options
        options = []
        for x in range(len(skills)):
            if x != self.position:
                printables = db.querySkillToPrint(skills[x])
                options.append(
                    discord.SelectOption(label=printables[0][0].title(), description=printables[0][1][:99], value=x,
                                         default=False))
        if not options:
            printables = db.querySkillToPrint(skills[self.position])
            options.append(
                discord.SelectOption(label=printables[0][0].title(), description=printables[0][1][:99], value=x,
                                     default=False))

        super().__init__(placeholder=placeholder, max_values=1, options=options)

    # once the user picks an option the embed is updated to display what they chose and a new drop-down list is generated
    async def callback(self, interaction: discord.Interaction):
        # get the index of the selected option
        self.position = int(self.values[0])

        # get the printables
        printables = db.querySkillToPrint(self.skills[self.position])
        # make the new embed
        embed = discord.Embed(title=printables[0][0].title(), description=printables[0][1][:99], color=0x288830)
        embed.set_footer(
            text='Browse through the Skills using the drop-down list and confirm your selection using the green tick button.')
        # make the new drop-down list
        select = selectSkill(chargen=self.chargen, skills=self.skills, position=self.position,
                             placeholder=self.placeholder)
        # make the view with the two buttons
        view = ButtonView(select=select, chargen=self.chargen, selection=self.skills[self.position])
        # ship it
        await interaction.message.edit(embed=embed, view=view)
        try:
            await interaction.response.send_message(" ")
        except:
            pass


# makes a view with buttons and stuff
class ButtonView(discord.ui.View):

    def __init__(self, *, timeout=300, select, chargen, selection=None, selection1=None):
        super().__init__(timeout=timeout)

        self.add_item(select)
        if selection is not None:
            self.add_item(okButton(chargen=chargen, selection=selection, selection1=selection1))

        if chargen.getLayer() > 0:
            self.add_item(
                undoButton(chargen=chargen))


# button to progress the lifepath selection
class okButton(discord.ui.Button):

    # we need the chargen to take us to the next step and links
    def __init__(self, chargen, selection, selection1):
        self.chargen = chargen
        self.selection = selection
        self.selection1 = selection1

        super().__init__(emoji=discord.PartialEmoji.from_str("✅"), style=discord.ButtonStyle.green)

    # when pressed, the chargen takes over
    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
        await self.chargen.nextLayer(selection=self.selection, selection1=self.selection1)
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
