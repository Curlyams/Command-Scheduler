# views/response_view.py

class ResponseView:
    @staticmethod
    async def send_schedule_started(channel):
        await channel.send("Scheduled task started.")

    @staticmethod
    async def send_schedule_stopped(channel):
        await channel.send("Scheduled task stopped.")

    @staticmethod
    async def send_command_executed(channel, command):
        await channel.send(f"Executed command: {command}")
