import asyncio
import logging
import os
import sys
import traceback

import disnake
from disnake.ext import commands

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
print(BOT_TOKEN)

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logger = logging.getLogger(__name__)


def fancy_traceback(exc: Exception) -> str:
    """May not fit the message content limit"""
    text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    return f"```py\n{text[-4086:]}\n```"


class Source2Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",  # replace with your desired prefix
            intents=disnake.Intents.all(),
            help_command=None,
        )

    async def on_ready(self):
        print(
            f"\n"
            f"The bot is ready.\n"
            f"User: {self.user}\n"
            f"ID: {self.user.id}\n"
        )

    def add_cog(self, cog: commands.Cog, *, override: bool = False) -> None:
        logger.info(f"Loading cog {cog.qualified_name}.")
        return super().add_cog(cog, override=override)

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        msg = f"Command `{ctx.command}` failed due to `{error}`"
        logger.error(msg, exc_info=True)

        embed = disnake.Embed(
            title=msg,
            description=fancy_traceback(error),
            color=disnake.Color.red(),
        )
        await ctx.send(embed=embed)

    # Continue from the previous code...

    async def on_slash_command_error(self, inter: disnake.AppCmdInter, error: commands.CommandError) -> None:
        msg = f"Slash command `{inter.data.name}` failed due to `{error}`"
        logger.error(msg, exc_info=True)

        embed = disnake.Embed(
            title=msg,
            description=fancy_traceback(error),
            color=disnake.Color.red(),
        )
        if inter.response.is_done():
            send = inter.channel.send
        else:
            send = inter.response.send_message
        await send(embed=embed)

    async def on_user_command_error(self, inter: disnake.AppCmdInter, error: commands.CommandError) -> None:
        msg = f"User command `{inter.data.name}` failed due to `{error}`"
        logger.error(msg, exc_info=True)

        embed = disnake.Embed(
            title=msg,
            description=fancy_traceback(error),
            color=disnake.Color.red(),
        )
        if inter.response.is_done():
            send = inter.channel.send
        else:
            send = inter.response.send_message
        await send(embed=embed)

    async def on_message_command_error(self, inter: disnake.AppCmdInter, error: commands.CommandError) -> None:
        msg = f"Message command `{inter.data.name}` failed due to `{error}`"
        logger.error(msg, exc_info=True)

        embed = disnake.Embed(
            title=msg,
            description=fancy_traceback(error),
            color=disnake.Color.red(),
        )
        if inter.response.is_done():
            send = inter.channel.send
        else:
            send = inter.response.send_message
        await send(embed=embed)

    async def reload_cog(self, cog_name: str):
        try:
            self.reload_extension(f"cogs.{cog_name}")
            logger.info(f"Reloaded cog {cog_name}.")
        except Exception as e:
            logger.error(f"Failed to reload cog {cog_name}.", exc_info=True)
            raise e

    async def reload_all_cogs(self):
        error_occurred = False
        for cog in self.cogs:
            try:
                await self.reload_cog(cog)
            except Exception as e:
                error_occurred = True
                logger.error(f"Failed to reload all cogs due to error in {cog}.", exc_info=True)
        if not error_occurred:
            logger.info("Successfully reloaded all cogs.")
        else:
            raise Exception("Failed to reload all cogs. Check logs for details.")


# Continue with the rest of the code...


if __name__ == "__main__":
    bot = Source2Bot()

    # Load your cogs here
    cogs = [
        'CatchRouteMsgs',
        'OpenAIProcedures',
        'HelpCog'
        ]

#        'BotAdminUI',
#
#        'PersonaDBHandler',
#        'PersonaUI',
#        'PersonaWrap',
#        'WebHookHandler',
#    ]

    for cog in cogs:
        bot.load_extension(f"cogs.{cog}")  # assuming your cogs are in a directory named "cogs"

    bot.run(BOT_TOKEN)
