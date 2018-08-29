from twitchio import commands as tcommands
import discord
import asyncio
from discord.ext import commands
import secrets

loop = asyncio.get_event_loop()
discord_bot = commands.Bot(command_prefix="!@#$%^&*()", self_bot=False)
discord_is_ready = False
users = []
messages = []

@discord_bot.event
async def on_ready():
    global discord_is_ready
    discord_is_ready = True
    print("DISCORD READY")
    await discord_bot.change_presence(game=discord.Game(name=secrets.drp_name, url=secrets.drp_url, type=1))


class Botto(tcommands.TwitchBot):
    def __init__(self):
        super().__init__(prefix=['!'], token=secrets.twitch_oauth, client_id=secrets.twitch_clientid,
                         nick=secrets.twitch_nick, initial_channels=[secrets.twitch_channel])

    async def event_ready(self):
        print('TWITCH READY!')

    @tcommands.twitch_command(aliases=['say'])
    async def say_command(self, ctx):
        global discord_bot, discord_is_ready
        if discord_is_ready is False: return
        if len(ctx.message.content[5:]) == 0: return
        txt = "`{}:` {}".format(ctx.message.author.name, ctx.message.content[5:])
        await discord_bot.send_message(discord_bot.get_server(secrets.discord_server).get_channel(secrets.discord_channel), txt)


loop.create_task(discord_bot.start(secrets.discord_token, bot=True))

bot = Botto()
loop.create_task(bot.run())

try:
    loop.run_forever()
finally:
    loop.stop()