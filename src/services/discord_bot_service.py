"""
discord bot for communicating messages
"""

import discord
from discord import TextChannel
from discord.ext import commands

from src.datalayer.connection import Database
from src.datalayer.subscriber_repository import SubscriberRepository


class DiscordBotService(commands.Bot):
    """Discord bot implementation that pings specified users on startup."""

    def __init__(self, db: Database, channel_id: int, command_prefix="!", intents=None):
        """constructor"""
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.messages = True
            intents.guilds = True
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.db = db
        self.subscriber_repository = SubscriberRepository(db)
        self.channel_id = channel_id

    async def on_ready(self):
        print("NewsTrackerBot mounted")
        try:
            user_ids = self.subscriber_repository.get_all()
            channel = self.get_channel(self.channel_id)
            if isinstance(channel, TextChannel):
                mentions = " ".join(f"<@{user_id}>" for user_id in user_ids)
                await channel.send(f"{mentions} Bot is now online!")
            else:
                print(f"Could not find channel with ID {self.channel_id}")
        except Exception as e:
            print(f"Failed to send message to channel: {e}")

    async def ping_users(self, message: str):
        """Ping configured users in the channel with a message."""
        try:
            user_ids = self.subscriber_repository.get_all()
            channel = self.get_channel(self.channel_id)
            if isinstance(channel, TextChannel):
                mentions = " ".join(f"<@{user_id}>" for user_id in user_ids)
                await channel.send(f"{mentions} {message}")
            else:
                print(f"Could not find channel with ID {self.channel_id}")
        except Exception as e:
            print(f"Failed to send message to channel: {e}")
