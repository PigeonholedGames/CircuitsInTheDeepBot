import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(context):
    server = context
    rollschannel = await server.create_text_channel("Rolls")
    chargenchannel = await server.create_text_channel("Character_Creation")

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

client.run('OTg3NjM5OTc3MjA4ODQwMTky.GSukVJ.W9lkkQ6MN27XjnCj0Q6R2BZjUKR9pOzSQcbmKM')