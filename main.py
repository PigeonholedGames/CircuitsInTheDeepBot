import discord
from discord.utils import get

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(server):

    category = get(server.categories, name='Bot Controls')

    if category is None:
        category = await server.create_category_channel('Bot Controls')

    if get(category.channels, name='character-creation') is None:
        await server.create_text_channel('character-creation', category=category)

    if get(category.channels, name='rolls') is None:
        await server.create_text_channel('rolls', category=category)

    if get(category.channels, name='clocks') is None:
        await server.create_text_channel('clocks', category=category)

@client.event
async def on_message(context):
    if context.author == client.user:
        return

    if context.content.startswith('>>'):

        if context.content.startswith('>>create'):
            print('create works')

        if context.content.startswith('>>load'):
            print('load works')

        if context.content.startswith('>>show'):
            print('show works')

        if context.content.startswith('>>roll'):
            print('roll works')

        if context.content.startswith('>>clock'):
            print('clock works')

        if context.content.startswith('>>setup'):

            server = context.guild
            category = get(server.categories, name='Bot Controls')

            if category is None:
                category = await server.create_category_channel('Bot Controls')

            if get(category.channels, name='character-creation') is None:
                await server.create_text_channel('character-creation', category=category)

            if get(category.channels, name='rolls') is None:
                await server.create_text_channel('rolls', category=category)

            if get(category.channels, name='clocks') is None:
                await server.create_text_channel('clocks', category=category)


client.run(open('config.ini').readline())