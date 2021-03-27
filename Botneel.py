import discord
from discord.ext import commands
from discord.utils import get
import random


client = commands.Bot(command_prefix='>>')
TOKEN = 'NzUwNzUyNDg0NDYwMzMxMDY4.X0_GvA.WkUj86I6x3xmmNF0xmCF5qs7CRI'
client.remove_command('help')


@client.event
async def on_ready():
    print('\nBotneel is online')
    print('-----------------\n')
    await client.change_presence(activity=discord.Game('>>help'))


# error handling

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("`Invalid Command`")


    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("`Please pass the required argument`")


# chat commands

@client.command(aliases=['Hi', 'HI', 'hey', 'Hey'])
async def hi(ctx):
    reply = ['Hi', 'Hey', 'Hello peeps', "Yeah I'm online", 'Wassup!', "God! You're annoying", 'Stop disturbing me', 'Let me be at peace please', "I'm busy, what do you want?"]
    await ctx.send(random.choice(reply))

@client.command(aliases=['Q'])
async def q(ctx):
    reply = ['Yes', 'No']
    await ctx.send(random.choice(reply))

@client.command(aliases=['cls'])
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

@client.command()
async def help(ctx):
    em = discord.Embed(colour=discord.Colour.blue())

    em.set_author(name="Bot Commands")
    em.add_field(name='>>clear', value='clears the messages(no. of messages required)', inline=False)
    em.add_field(name='>>q', value='sends a random yes or no answer', inline=False)
    em.add_field(name='>>c_flip', value='flips a coin', inline=False)
    em.add_field(name='>>spam', value='spams the chat with whatever word you send', inline=False)
    em.add_field(name='>>tellme', value='helps you decide on things', inline=False)
    em.add_field(name='>>nick', value='changes nickname')
    em.add_field(name='>>rnick', value='resets nickname')
    em.add_field(name='>>mute', value='server mutes both in text and voice')
    em.add_field(name='>>unmute', value='server unmutes in text and voice')

    await ctx.send(embed=em)

@client.command()
async def c_flip(ctx):
    results = ['Heads', 'Tails']
    await ctx.send(random.choice(results))

@client.command()
async def spam(ctx, *,word):
    spam_msg = ['you got spammed.....', 'LMAO', 'LOL', 'haha', 'spamming feels good!', 'I will annoy everyone lol']
    for _ in range(25):
        await ctx.send(word)
    await ctx.send(random.choice(spam_msg))

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick()
    await ctx.send(f"{member} has been kicked out")

@client.command()
@commands.has_permissions(kick_members = True)
async def smute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} \nReason: {reason}")
    await member.send(f"You were muted in the server {guild.name} for reason {reason}")

@client.command()
@commands.has_permissions(kick_members = True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedRole = get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {guild.name}")

@client.command(aliases = ['tm', 'm8', 'magic8', 'tbh'])
async def tellme(ctx):
    reply = [
                "As I see it, yes.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don’t count on it.",
                "It is certain.",
                "It is decidedly so.",
                "Most likely.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Outlook good.",
                "Reply hazy, try again.",
                "Signs point to yes.",
                "Very doubtful.",
                "Without a doubt.",
                "Yes.",
                "Yes – definitely.",
                "You may rely on it."
            ]
    await ctx.send(random.choice(reply))

@client.command()
async def nick(ctx, member: discord.Member, *, nickname):
    reply = ['Done', 'Nickname changed']
    await member.edit(nick = nickname)
    await ctx.send(random.choice(reply))

@client.command(aliases = ['resetnick', 'Resetnick'])
async def rnick(ctx, member: discord.Member):
    await member.edit(nick = None)
    await ctx.send('Reset complete')


#voice commands

@client.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You have to be in a voice channel to run this command")

@client.command(pass_context=True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I am not in a voice channel")



client.run(TOKEN)