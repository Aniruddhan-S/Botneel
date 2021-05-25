import discord
from discord.ext import commands
from discord.utils import get
import random
import json

f = open('config.json', 'r')
token = json.load(f)

client = commands.Bot(command_prefix='>>')
TOKEN = token["token"]
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
        await ctx.send("`Command incomplete`")


# help command embed

@client.command()
async def help(ctx):
    em = discord.Embed(colour=discord.Colour.light_grey(), title="Botneel Commands", description="The parameters enclosed in the < > brackets are required and the ones in the ( ) are optional")

    em.add_field(name='General Text Commands', value='>>hi\n>>q <question>\n>>clear <value>\n>>tellme <question>\n>>spam <word/line>', inline=False)
    em.add_field(name='Moderator Commands', value='>>kick <@person> (reason)\n>>ban <@person> (reason)\n>>unban <name#number> (reason)\n>>mute <@person> <server/text/voice> (reason)\n>>unmute <@person>\n>>nick <@person> <nickname>\n>>rnick <@person>', inline=False)
    em.add_field(name='Voice Commands', value='>>join\n>>leave\n>>pull <@person>\n>>push <@person> <vc name>', inline=False)

    await ctx.send(embed=em)


# text commands

@client.command(aliases=['hey'])
async def hi(ctx):
    reply = ['Hi', 'Hey', 'Hello peeps', "Yeah I'm here", 'Wassup!', "God! You're annoying",
            'Stop disturbing me','Let me be at peace please', "I'm busy, what do you want?"]
    await ctx.send(random.choice(reply))

@client.command(aliases=['Q'])
async def q(ctx):
    reply = ['Yes', 'No']
    await ctx.send(random.choice(reply))

@client.command(aliases=['cls'])
async def clear(ctx, amount=1):
    if amount <= 30:
        await ctx.channel.purge(limit=amount+1)
    else:
        await ctx.send("`You can't delete more than 30 messages at a time`")

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
async def spam(ctx, *,word):
    spam_msg = ['you got spammed.....', 'LMAO', 'LOL', 'haha', 'spamming feels good!', 'I will annoy everyone lol']
    for _ in range(25):
        await ctx.send(word)
    await ctx.send(random.choice(spam_msg))


# text commands - Moderation

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason=None):
    async with ctx.typing():
        await member.kick()
        await ctx.send(f"{member} has been kicked out")

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member):
    async with ctx.typing():
        await member.ban()
        await ctx.send(f"{member} has been banned from the server")

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    async with ctx.typing():
        bannedUsers = await ctx.guild.bans()
        name, discriminator = member.split("#")

        for ban in bannedUsers:
            user = ban.user
            if((user.name, user.discriminator) == (name, discriminator)):
                await ctx.guild.unban(user)
                await ctx.send(f"{member} has been unbanned")
                return

@client.command()
@commands.has_permissions(kick_members = True)
async def mute(ctx, member: discord.Member, choice,  *, reason=None):
    async with ctx.typing():
        guild = ctx.guild
        if choice == "server":
            smutedRole = get(guild.roles, name="ServerMuted")

            if not smutedRole:
                smutedRole = await guild.create_role(name="ServerMuted")

                for channel in guild.channels:
                    await channel.set_permissions(smutedRole, speak=False, send_messages=False)

            await member.add_roles(smutedRole, reason=reason)
            await ctx.send(f"Server Muted {member.mention} \nReason: {reason}")
            await member.send(f"You were server muted in the server {guild.name} for reason {reason}")
        
        elif choice == "text":
            tmutedRole = get(guild.roles, name="TextMuted")

            if not tmutedRole:
                tmutedRole = await guild.create_role(name="TextMuted")

                for channel in guild.channels:
                    await channel.set_permissions(tmutedRole, send_messages=False)

            await member.add_roles(tmutedRole, reason=reason)
            await ctx.send(f"Text Muted {member.mention} \nReason: {reason}")
            await member.send(f"You were text muted in the server {guild.name} for reason {reason}")

        elif choice == "voice":
            vmutedRole = get(guild.roles, name="VoiceMuted")

            if not vmutedRole:
                vmutedRole = await guild.create_role(name="VoiceMuted")

                for channel in guild.channels:
                    await channel.set_permissions(vmutedRole, speak=False)

            await member.add_roles(vmutedRole, reason=reason)
            await ctx.send(f"Voice Muted {member.mention} \nReason: {reason}")
            await member.send(f"You were voice muted in the server {guild.name} for reason {reason}")

        else:
            await ctx.send("`Please specify where to be muted`")

@client.command()
@commands.has_permissions(kick_members = True)
async def unmute(ctx, member: discord.Member):
    async with ctx.typing():
        guild = ctx.guild
        smutedRole =  get(guild.roles, name="ServerMuted")
        tmutedRole =  get(guild.roles, name="TextMuted")
        vmutedRole =  get(guild.roles, name="VoiceMuted")

        if(get(ctx.guild.roles, name="ServerMuted")):
            await member.remove_roles(smutedRole)

        if(get(ctx.guild.roles, name="TextMuted")):
            await member.remove_roles(tmutedRole)
        
        if(get(ctx.guild.roles, name="VoiceMuted")):
            await member.remove_roles(vmutedRole)

        await ctx.send(f"Unmuted {member.mention}")


@client.command()
@commands.has_permissions(change_nickname = True)
async def nick(ctx, member: discord.Member, *, nickname):
    async with ctx.typing():
        reply = ['Done', 'Nickname changed']
        await member.edit(nick = nickname)
        await ctx.send(random.choice(reply))

@client.command(aliases = ['resetnick', 'Resetnick'])
@commands.has_permissions(change_nickname = True)
async def rnick(ctx, member: discord.Member):
    async with ctx.typing():
        await member.edit(nick = None)
        await ctx.send('Reset complete')


# voice commands

@client.command(pass_context=True)
async def pull(ctx, member: discord.Member):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await member.move_to(channel)
    else:
        await ctx.send("`You have to be in a voice channel to run this command`")

@client.command(pass_context=True)
async def push(ctx, member: discord.Member, *, vc_name=None):
    for channel in ctx.guild.voice_channels:
        if channel.name == vc_name:
            await member.move_to(channel)



client.run(TOKEN)