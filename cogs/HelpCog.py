import disnake
from disnake.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = disnake.Embed(
            title="Help Menu",
            description=(
                "Source is the second prototype bot in the 'Capitophagist' series of bots. "
                "Source is currently a direct interface with ChatGPT through the !ask command.\n\n"
                "Here are the commands you can use:"
            ),
            color=disnake.Color.blue()
        )

        # Add a field for each command
        embed.add_field(name="!ask [question]", value="Ask a question to the GPT-3 model.", inline=False)
        # Add more fields as needed for other commands
        # embed.add_field(name="!command2", value="Description of command2.", inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpCog(bot))
