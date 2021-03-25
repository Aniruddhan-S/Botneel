import discord
from discord.ext import commands
import random
import wikipedia
from PyDictionary import PyDictionary
import requests


dictionary = PyDictionary()
client = commands.Bot(command_prefix='>>')
TOKEN = 'NzUwNzUyNDg0NDYwMzMxMDY4.X0_GvA.WkUj86I6x3xmmNF0xmCF5qs7CRI'
client.remove_command('help')


@client.event
async def on_ready():
    print('\nBotneel is online\n')
    await client.change_presence(activity=discord.Game('>>cmds'))


# error handling

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("`Invalid Command`")


    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("`Please pass the required argument`")


# commands

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
async def cmds(ctx):
    em = discord.Embed(colour=discord.Colour.blue())

    em.set_author(name="Bot Commands")
    em.add_field(name='>>hi', value='sends Hey', inline=False)
    em.add_field(name='>>clear', value='clears the messages(no. of messages required)', inline=False)
    em.add_field(name='>>q', value='sends a random yes or no answer', inline=False)
    em.add_field(name='>>search', value='searches wikipedia', inline=False)
    em.add_field(name='>>c_flip', value='flips a coin', inline=False)
    em.add_field(name='>>define', value='searches the meaning')
    em.add_field(name='>>synonym', value='searches the synonym')
    em.add_field(name='>>antonym', value='searches the antonym')
    em.add_field(name='>>spam', value='spams the chat with whatever word you send', inline=False)
    em.add_field(name='>>tellme', value='helps you decide on things', inline=False)
    em.add_field(name='>>nick', value='changes nickname')
    em.add_field(name='>>rnick', value='resets nickname')

    await ctx.send(embed=em)

@client.command()
async def search(ctx, word):
    definition = wikipedia.summary(word, sentences=3)
    await ctx.send(definition)

@client.command()
async def c_flip(ctx):
    results = ['Heads', 'Tails']
    await ctx.send(random.choice(results))

@client.command()
async def define(ctx, word):
    meaning = dictionary.meaning(word)
    await ctx.send(meaning)

@client.command()
async def synonym(ctx, word):
    syn = dictionary.synonym(word)
    await ctx.send(syn)

@client.command()
async def antonym(ctx, word):
    ant = dictionary.antonym(word)
    await ctx.send(ant)

@client.command()
async def spam(ctx, *,word):
    spam_msg = ['you got spammed.....', 'LMAO', 'LOL', 'haha', 'spamming feels good!', 'I will annoy everyone lol']
    for _ in range(25):
        await ctx.send(word)
    await ctx.send(random.choice(spam_msg))

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send(member.display_name + " has been kicked out")

@client.command()
@commands.has_permissions(kick_members = True)
async def mute(ctx, member: discord.Member):
    muted = ctx.guild.get_role(781393780108427264)
    await member.add_roles(muted)
    await ctx.send(member.mention + " has been muted")

@client.command()
@commands.has_permissions(kick_members = True)
async def unmute(ctx, member: discord.Member):
    muted = ctx.guild.get_role(781393780108427264)
    await member.remove_roles(muted)
    await ctx.send(member.mention + " has been unmuted")

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

@client.command()
@commands.has_permissions(kick_members = True)
async def role(ctx, role_name, role_color):
    guild = ctx.guild
    await guild.create_role(name=role_name, colour=discord.Colour(role_color))
    await ctx.send("Role successfully created")
   

client.run(TOKEN)