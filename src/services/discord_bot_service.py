import discord
from discord import TextChannel
from src.datalayer.connection import Database
from src.datalayer.subscriber_repository import SubscriberRepository


class DiscordBotService(discord.Bot):
    """Discord bot that pings users and supports slash commands."""

    def __init__(self, db: Database, channel_id: int, guild_id: int):
        intents = discord.Intents.all()
        super().__init__(intents=intents)

        self.db = db
        self.subscriber_repository = SubscriberRepository(db)
        self.channel_id = channel_id
        self.guild_id = guild_id
        self._register_commands()

    async def on_ready(self):
        print(f"Bot online as {self.user}")
        await self.ping_users("Bot is now online!")

    async def ping_users(self, message: str):
        """Ping all subscribers."""
        user_ids = self.subscriber_repository.get_all()
        channel = self.get_channel(self.channel_id)
        if isinstance(channel, TextChannel):
            mentions = " ".join(f"<@{uid}>" for uid in user_ids)
            await channel.send(f"{mentions} {message}")

    def _register_commands(self):
        """Define all slash commands here."""

        @self.command(description="Add yourself to the subscribers list")
        async def addsubscriber(ctx):
            user_id = ctx.author.id
            # example DB call
            if self.subscriber_repository:
                self.subscriber_repository.add(user_id)
            await ctx.respond(f"<@{user_id}> added!", ephemeral=True)

        @self.command(description="Remove yourself from the subscribers list")
        async def removesubscriber(ctx):
            user_id = ctx.author.id
            if self.subscriber_repository:
                self.subscriber_repository.remove(user_id)
            await ctx.respond(f"<@{user_id}> removed!", ephemeral=True)
