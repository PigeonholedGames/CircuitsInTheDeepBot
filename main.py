import discord
from discord.utils import get

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# when the bot joins a server it creates a text channel category and text channels under it
@client.event
async def on_guild_join(server):
    category = get(server.categories, name='Bot Controls')  # get category

    if category is None:  # check if category exists before making it
        category = await server.create_category_channel('Bot Controls')

    if get(category.channels, name='character-creation') is None:  # character-creation channel gets made
        await server.create_text_channel('character-creation', category=category)

    if get(category.channels, name='rolls') is None:  # rolls channel gets made
        await server.create_text_channel('rolls', category=category)

    if get(category.channels, name='clocks') is None:  # clocks channel gets made
        await server.create_text_channel('clocks', category=category)


# listener for messages
@client.event
async def on_message(context):
    # ignore the message if sent by the bot itself
    if context.author == client.user:
        return

    # ignore all messages not starting with ">>"
    if context.content.startswith('>>'):

        # the roll command initiates a roll
        if context.content.startswith('>>roll'):
            print('roll works')

        # the clock command creates a clock
        elif context.content.startswith('>>clock'):
            print('clock works')

        # the show command outputs the active characters sheet
        elif context.content.startswith('>>show'):
            print('show works')

        # the create command creates a new thread and initializes a character creation sequence
        elif context.content.startswith('>>create'):
            print('create works')

        # the load command changes the users active character
        elif context.content.startswith('>>load'):
            print('load works')

        # the setup command remakes the category and channels that should have been created on join
        elif context.content.startswith('>>setup'):

            server = context.guild
            category = get(server.categories, name='Bot Controls')  # get the category

            if category is None:  # check if the category exists before making it
                category = await server.create_category_channel('Bot Controls')

            if get(category.channels, name='character-creation') is None:  # character-creation channel gets made
                await server.create_text_channel('character-creation', category=category)

            if get(category.channels, name='rolls') is None:  # rolls channel gets made
                await server.create_text_channel('rolls', category=category)

            if get(category.channels, name='clocks') is None:  # clocks channel gets made
                await server.create_text_channel('clocks', category=category)


client.run(open('config.ini').readline())  # get the bot token from a local config file
