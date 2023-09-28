import asyncio
import discord
from discord import app_commands
import commands
import db


class circbot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    # connect to the discord api and start listenin', reminder to fill this up if the bot needs to remember stuff after restarting
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print('We have logged in as {0.user}'.format(client))

    # when the bot joins a server it creates a text channel category and text channels under it
    async def on_guild_join(self, server):

        # saying hello to my new server :)
        channel = server.system_channel
        if channel.permissions_for(server.me).send_messages:
            await channel.send("Hello! Thank you for your interest in Circuits In the Deep!")
            await channel.send("Please hold while we remodel your server.")
            await asyncio.sleep(1.5)
            await channel.send(":smiley:")
            await asyncio.sleep(2.5)
            await channel.send("Please do not delete or rename the bot controls category or its text channels.")
            await channel.send("Type /help to see available commands.")

        # actually setting stuff up
        await commands.create_channels(server)


# let's gooooooooo
client = circbot()
tree = app_commands.CommandTree(client)


# help command, lists all other commands
@tree.command(name="help", description="See the Available Commands")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("My commands are:"
                                            "\n>>> **/create:** to begin character creation."
                                            "\n**/show:** to display your character sheet."
                                            "\n**/edit:** to edit your character."
                                            "\n**/load:** to change your active character."
                                            "\n**/roll:** to make a roll with your character."
                                            "\n**/setup:** to re-create the bot channels if something happened to them.",
                                            ephemeral=True)


# setup command, fixes server channels if the mods broke them for whatever reason
@tree.command(name="setup", description="Re-Create Deleted Bot Channels")
async def self(interaction: discord.Interaction):
    await commands.create_channels(interaction.guild)
    await interaction.response.send_message("Category and Channels have been remade, please do not delete or rename "
                                            "them.", ephemeral=True)


# create command, starts up character creation
@tree.command(name="create", description="Begins Character Creation")
async def self(interaction: discord.Interaction):
    await commands.start_chargen(interaction)


# get the bot token from a local config file
client.run(open('config.ini').readline())
