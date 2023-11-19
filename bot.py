# bot.py
import os
import google.generativeai as palm
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# configure api
API_KEY = os.environ.get("API_Key")
palm.configure(api_key=API_KEY)


# Create a bot instance with a command prefix
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
bot = commands.Bot(command_prefix='!')

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    print(f'Received message: {message.content}')

    # Add this line to process commands
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    print(f'Command error: {error}')

# Command to ask a question
@bot.command(name='ask')
async def ask_question(ctx, *args):
    # Join the arguments to form the question
    question = ' '.join(args)
    print(f'Question: {question}')

    # Call the API to get the answer
    answer = get_answer_from_api(question)

    # Send the answer back to the Discord channel
    await ctx.send(answer)

def get_answer_from_api(question):
    try:
        # Replace 'YOUR_API_ENDPOINT' with the actual API endpoint
        response = palm.generate_text(
        model="models/text-bison-001",
        prompt=question,
        temperature=0.5,
        # The maximum length of the response
        max_output_tokens=800,
        )
        

        # Return the answer from the API response
        return response.result
    except Exception as e:
        print(f'Error fetching answer from API: {e}')
        return 'Sorry, an error occurred while fetching the answer.'



if __name__ == "__main__":
    # Run the bot with your bot token
    bot.run(TOKEN)