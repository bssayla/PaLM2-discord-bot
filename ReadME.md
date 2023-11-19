# Introduction
This is a simple Discord bot that Uses [PaLM2 API](https://developers.generativeai.google/) to anwser questions.
# How to use
1. Create a discord bot and get the token
2. Get Your API Key from [Here](https://developers.generativeai.google/)
3. Create a file called `.env` and paste your API Key and Discord Bot Token in it
   ```bash
   API_Key={Your_API_Key}
   DISCORD_BOT_TOKEN={Your_Discord_Bot_Token}
   ```
4. Run the bot
   ```bash
    python3 bot.py
    ```
# Commands
For now there is only one command
- `!ask {Question}`: Ask a question
this command will return the answer to the current question but it doesn't remember the context of the chat(old questions).
## Demo
![Ask Command](./images/ask_command.png)

# TODO
- [x] Add `!chat` command to create a new chat with the bot and remember the context of the chat
- [x] Add `!reply` command to continue the chat with the bot
- [ ] Add `!help` command to show the commands


