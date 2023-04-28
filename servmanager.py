from discord.utils import get

import charmaker


# function to create text channel category and fill it up
async def create_channels(server):
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


# function to start a thread for character creation
async def start_chargen(interaction):
    category = get(interaction.guild.categories, name='Bot Controls')  # get category

    # if the category hasn't been setup, inform the user and exit the process
    if category is None:
        channel = interaction.channel
        await interaction.response.send_message(
            'This server has not been properly setup or the bot channels have been deleted. Please use the "/setup" command before trying again.',
            ephemeral=True)
        return

    channel = get(category.channels, name='character-creation')  # get the channel

    # if the channel hasn't been setup, inform the user and exit the process
    if channel is None:
        channel = interaction.channel
        await interaction.response.send_message(
            'This server has not been properly setup or the bot channels have been deleted. Please use the "/setup" command before trying again.',
            ephemeral=True)
        return

    # get the user who is creating the character
    author = interaction.user

    # make a thread around the ping
    thread = await channel.create_thread(name="{}\'s Character".format(author.name),
                                         auto_archive_duration=60,
                                         reason="Character Creation Thread for {}".format(author.name))

    # now that we've collected all the relevant info from the interaction we can close it
    await interaction.response.send_message(f"Head over to {thread.mention} to begin.")

    # begin the character creation process
    await charmaker.chargen(thread, author)
    return
