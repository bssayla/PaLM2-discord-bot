# bot.py
import os
import google.generativeai as gemini
from discord.ext import commands
from dotenv import load_dotenv
import discord


chat_response = ""

load_dotenv()
# configure api
API_KEY = os.environ.get("API_Key")
gemini.configure(api_key=API_KEY)


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
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    print(f'Command error: {error}')

# Command to ask a question
@bot.command(name='ask' ,help="`!ask {Question}`: Ask a question\nthis command will return the answer to the current question but it doesn't remember the context of the chat(old questions).")
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
        response = gemini.generate_text(
        model="models/gemini-pro",
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


@bot.command(name='chat' ,help="`!chat {start chatting}`: Create a new chat with the bot that remembers the context of the chat(old questions).")
async def start_new_chat(ctx, *args):
    # Join the arguments to form the question
    question = ' '.join(args)
    print(f'Question: {question}')

    # Call the API to get the answer
    global chat_response 
    chat_response = get_answer_from_chat_api(question)

    # Send the answer back to the Discord channel
    await ctx.send(chat_response.last)

def get_answer_from_chat_api(question):
    try:
        response = gemini.chat(
            messages=[question],
        )
        

        # Return the answer from the API response
        return response
    except Exception as e:
        print(f'Error fetching answer from API: {e}')
        return 'Sorry, an error occurred while fetching the answer.'

@bot.command(name='reply' ,help="`!reply {your reply}`: Reply to the bot after using the `!chat` command.")
async def continue_chating(ctx, *args):
    # Join the arguments to form the question
    question = ' '.join(args)
    print(f'Question: {question}')

    # Call the API to get the answer
    answer = repying_to_chat(question)

    # Send the answer back to the Discord channel
    await ctx.send(answer)

def repying_to_chat(my_reply):
    try:
        global chat_response
        chat_response = chat_response.reply(my_reply)
        

        # Return the answer from the API response
        return chat_response.last
    except Exception as e:
        print(f'Error fetching answer from API: {e}')
        return 'Sorry, an error occurred while fetching the answer.'


#image generation
    

# Help command
@bot.command(name='commands', help='Show information about available commands.')
async def help(ctx):
    # Create an Embed message with command information
    help_embed = discord.Embed(title='Bot Commands', color=0x00ff00)
    help_embed.add_field(name='!ask', value='Ask a question and get an answer from the API.')
    help_embed.add_field(name='!chat', value='Start a new chat with the bot that remembers the context of the chat(old questions/data given earlier).')
    help_embed.add_field(name='!reply', value='Reply to the bot after using the `!chat` command.')
    help_embed.add_field(name='!help', value='Show information about available commands.')

    # Send the Embed message to the Discord channel
    await ctx.send(embed=help_embed)



@bot.command(name='history', help='Show the history of the chat.')
async def history(ctx):
    for message in chat_response.messages:
        await ctx.send("message: " + message["content"])
        await ctx.send("-"*50)
    

if __name__ == "__main__":
    # Run the bot with your bot token
    bot.run(TOKEN)