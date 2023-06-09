import openai
from disnake.ext import commands


class OpenAIProcedures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_gpt3_response(self, message):
        openai.api_key = 'your-api-key'  # replace with your actual API key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ]
        )

        return response['choices'][0]['message']['content']


def setup(bot):
    bot.add_cog(OpenAIProcedures(bot))
