import discord

TOKEN = "%YOUR TOKEN HERE%"

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, Welcome to the server!")

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    userMessage = str(message.content).lower()
    channel = str(message.channel.name)
    if message.author == client.user:
        return

    if message.channel.name == "commands":
        if userMessage == "hi" or userMessage == "hello":
            await message.channel.send(f"Hello {username}")
            return
        if userMessage == "bye" or userMessage == "goodbye":
            await message.channel.send(f"Goodbye {username}")
            return


client.run(TOKEN)