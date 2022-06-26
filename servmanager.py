import discord
from discord.utils import get


# function to create text channel category and fill it up
def create_channels(server):
    category = get(server.categories, name='Bot Controls')  # get category

    if category is None:  # check if category exists before making it
        category = await server.create_category_channel('Bot Controls')

    if get(category.channels, name='character-creation') is None:  # character-creation channel gets made
        await server.create_text_channel('character-creation', category=category)

    if get(category.channels, name='rolls') is None:  # rolls channel gets made
        await server.create_text_channel('rolls', category=category)

    if get(category.channels, name='clocks') is None:  # clocks channel gets made
        await server.create_text_channel('clocks', category=category)

    return

