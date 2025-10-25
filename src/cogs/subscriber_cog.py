import discord
from discord import app_commands
from discord.ext import commands
from src.datalayer.subscriber_repository import SubscriberRepository
from src.datalayer.connection import Database


class SubscriberCog(commands.Cog):
    """Cog for managing subscribers via slash commands."""

    def __init__(self, bot: commands.Bot, db: Database):
        self.bot = bot
        self.subscriber_repository = SubscriberRepository(db)

    # --- Add subscriber ---
    @app_commands.command(
        name="addsubscriber", description="Add yourself to the subscriber list"
    )
    async def addsubscriber(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        try:
            self.subscriber_repository.add(user_id)
            await interaction.response.send_message(
                f"<@{user_id}> has been added to subscribers.", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Failed to add subscriber: {e}", ephemeral=True
            )

    # --- Remove subscriber ---
    @app_commands.command(
        name="removesubscriber", description="Remove yourself from the subscriber list"
    )
    async def removesubscriber(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        try:
            self.subscriber_repository.remove(user_id)
            await interaction.response.send_message(
                f"<@{user_id}> has been removed from subscribers.", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Failed to remove subscriber: {e}", ephemeral=True
            )
