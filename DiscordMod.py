import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked.')

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned.')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} has been unbanned.')
            return

@client.command()
async def mute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(ROLE_ID_HERE)
    await member.add_roles(muted_role)
    await ctx.send(f'{member.mention} has been muted.')

@client.command()
async def unmute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(ROLE_ID_HERE)
    await member.remove_roles(muted_role)
    await ctx.send(f'{member.mention} has been unmuted.')

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def tempmute(ctx, member : discord.Member, time, *, reason=None):
    muted_role = ctx.guild.get_role(ROLE_ID_HERE)
    await member.add_roles(muted_role)
    await ctx.send(f'{member.mention} has been muted for {time}.')
    await asyncio.sleep(time)
    await member.remove_roles(muted_role)
    await ctx.send(f'{member.mention} has been unmuted.')

client.run('TOKEN_HERE')
