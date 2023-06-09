# CatchRouteMsgs.py
from disnake.ext import commands


class CatchRouteMsgs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx, *, question):
        openai_cog = self.bot.get_cog('OpenAIProcedures')
        response = await openai_cog.get_gpt3_response(question)
        await ctx.send(response)


def setup(bot):
    bot.add_cog(CatchRouteMsgs(bot))
