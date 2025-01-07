import discord
from fflogs_utils import generate_report_summary

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

with open('config.conf', 'r') as file:
    lines = file.readlines()
    bot_token = lines[0].strip().split('=')[1] 
    client_id = lines[1].strip().split('=')[1]
    client_secret = lines[2].strip().split('=')[1]

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} - {client.user.id}')
    print('Client is connected and ready!')

@client.event
async def on_message(message):
    if message.content.startswith('https://www.fflogs.com/reports/'):
        summary = generate_report_summary(message.content, client_id, client_secret)
        await message.channel.send(f"```{summary}```")

# Run the client with the token
if __name__ == '__main__':
    client.run(bot_token)