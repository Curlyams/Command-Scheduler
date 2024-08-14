import asyncio
import discord
from discord.ext import commands, tasks
from discord import app_commands
from Models import Schedule
from Views import ResponseView

class CommandSelect(discord.ui.Select):
    def __init__(self, bot, placeholder="Select a command to run", min_values=1, max_values=1):
        options = [
            discord.SelectOption(label="/article", description="Run the article command from NFL Bot 3.0"),
            # Add more options here
        ]
        super().__init__(placeholder=placeholder, min_values=min_values, max_values=max_values, options=options)
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        command = self.values[0]  # Get the selected command
        await interaction.response.send_message(f"Selected command: {command}")

        # Pass the selected command to the scheduled task
        self.view.schedule.command = command
        await self.view.start_schedule(interaction)


class ScheduleView(discord.ui.View):
    def __init__(self, bot, schedule):
        super().__init__()
        self.schedule = schedule
        self.add_item(CommandSelect(bot))

    async def start_schedule(self, interaction: discord.Interaction):
        await ResponseView.send_schedule_started(interaction.channel)
        await interaction.response.send_message(f"Scheduled task started with the command {self.schedule.command}")


class ScheduleController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.schedule = Schedule(command="!otherbotcommand", interval=60)
        self.channel_id = None

    @tasks.loop(minutes=1)  # This is just an example; use self.schedule.get_interval()
    async def scheduled_task(self):
        if self.channel_id is None:
            return
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await ResponseView.send_command_executed(channel, self.schedule.get_command())
            await channel.send(self.schedule.get_command())

    @app_commands.command(name='start_schedule', description='Start the scheduled task')
    @app_commands.describe(channel='Select the channel where the schedule should run', interval='Set the interval', unit='Unit of time (minutes, hours, days)')
    async def start_schedule(self, interaction: discord.Interaction, channel: discord.TextChannel, interval: int, unit: str):
        self.channel_id = channel.id

        # Adjust interval based on the selected unit
        if unit == 'minutes':
            self.schedule.interval = interval
            self.scheduled_task.change_interval(minutes=interval)
        elif unit == 'hours':
            self.schedule.interval = interval * 60
            self.scheduled_task.change_interval(hours=interval)
        elif unit == 'days':
            self.schedule.interval = interval * 60 * 24
            self.scheduled_task.change_interval(days=interval)
        else:
            await interaction.response.send_message("Invalid unit. Please use 'minutes', 'hours', or 'days'.")
            return

        # Create the command selection view
        view = ScheduleView(self.bot, self.schedule)
        await interaction.response.send_message(f"Select the command to run in {channel.mention} every {interval} {unit}:", view=view)

    @app_commands.command(name='stop_schedule', description='Stop the scheduled task')
    async def stop_schedule(self, interaction: discord.Interaction):
        self.scheduled_task.stop()
        await ResponseView.send_schedule_stopped(interaction.channel)
        await interaction.response.send_message("Scheduled task stopped")

async def setup(bot):
    await bot.add_cog(ScheduleController(bot))
