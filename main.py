import discord
from discord import app_commands
import servmanager


class circbot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

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
            await channel.send(
                "Hello! Thank you for your interest in Circuits In the Deep! "
                "\nServer takeover has been initialized "
                "\n:smiley: "
                "\nPlease do not delete or rename Bot_Controls or its channels."
                "\nType /help to see available commands")
            # actually setting up the server
        await servmanager.create_channels(server)


client = circbot()
tree = app_commands.CommandTree(client)


@tree.command(name="help", description="See the Available Commands")
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("Hi! My commands are:"
                                            "\n**/create:** to begin character creation."
                                            "\n**/show:** to display your character sheet."
                                            "\n**/edit:** to change your character."
                                            "\n**/load:** to change your active character. "
                                            "\n**/roll:** to make a roll with your character."
                                            "\n**/setup:** to re-create the bot channels if they've been deleted.",
                                            ephemeral=True)


@tree.command(name="setup", description="Re-Create Deleted Bot Channels")
async def self(interaction: discord.Interaction):
    await servmanager.create_channels(interaction.guild)
    await interaction.response.send_message("Category and Channels have been remade, please don't delete or rename "
                                            "them next time. :)", ephemeral=True)


@tree.command(name="create", description="Begins Character Creation")
async def self(interaction: discord.Interaction):
    await servmanager.start_chargen(interaction)
    await interaction.response.send_message('ok')


client.run(open('config.ini').readline())  # get the bot token from a local config file
