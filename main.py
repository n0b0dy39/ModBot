import os
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from discord.ext.commands import has_permissions, MissingPermissions, CheckFailure, BadArgument

load_dotenv(dotenv_path="config")

default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix=">", intents=default_intents)
bot.remove_command("help")

##################################################################################

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(">help"))
    print("Le bot est connecté.")

##################################################################################

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency * 1000)))

##################################################################################

@bot.command()
async def hello(ctx):
    await ctx.send('Hello {0.mention}.'.format(ctx.author))

##################################################################################

# Delete un message (!del [nmb de mess a del])
@bot.command(name="del")
@has_permissions(administrator=True)
async def delete(ctx, number: int):
    messages = await ctx.channel.history(limit=number + 1).flatten()
    if number >= 11:
        await ctx.send(f'Tu ne peux pas dépasser 10 messages or tu a mis {number}')
    else:
        for each_message in messages:
            await each_message.delete()


@delete.error
async def delete(ctx, number: int):
    await ctx.send('Tu ne peux pas effectuer cette action')

##################################################################################

# Savoir le role de qqun ('roles [@personne])
class MemberRoles(commands.MemberConverter):
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        return [role.name for role in member.roles[1:]]


@bot.command()
async def roles(ctx, *, member: MemberRoles):
    await ctx.send('Roles : ' + ', '.join(member))

##################################################################################

@bot.command()
async def avatar(ctx, *, member: discord.Member = None):
    userAvatar = member.avatar_url
    await ctx.send(userAvatar)

##################################################################################

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    await member.kick(reason=reason)
    embed = discord.Embed(title="Kick", description=f"{member.mention} viens de se faire kick ",
                          colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.send(f" tu viens d'être kick de : {guild.name} raison: {reason}")

@kick.error
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.send('Tu ne peux pas effectuer cette action')



##################################################################################

@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    await member.ban(reason=reason)
    embed = discord.Embed(title="Ban", description=f"{member.mention} est ban ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)

@ban.error
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.send('Tu ne peux pas effectuer cette action')

##################################################################################

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour=discord.Colour.blue()
    )

    embed = discord.Embed(title="-- Help --", description="Commandes bot", color=0x7289da)
    embed.add_field(name="ping", value="Montre votre connexion au serveur", inline=False)
    embed.add_field(name="del [nombre]", value="Supprime les messages", inline=False)
    embed.add_field(name="roles [@membre]", value="Montre les roles du membre mentionné", inline=False)
    embed.add_field(name="avatar [@membre]", value="Montre la photo de profile du membre mentionné", inline=False)
    embed.add_field(name="kick [@membre]", value="Kick le membre mentionné", inline=False)
    embed.add_field(name="ban [@membre]", value="Ban le membre mentionné", inline=False)
    embed.add_field(name="mute [@membre]", value="Mute le membre mentionné", inline=False)
    embed.add_field(name="unmute [@membre]", value="Unute le membre mentionné", inline=False)
    embed.add_field(name="slm [temps en seconde]", value="Active le slow mode", inline=False)

    embed.set_footer(text="ModBot | W⁷⁸#3422")

    await ctx.send(embed=embed)

##################################################################################

@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = get(guild.roles, name="Muted")
    memberr = get(guild.roles, name="Membre")
    await member.remove_roles(memberr)

    embed = discord.Embed(title="muted", description=f"{member.mention} est mute ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" tu viens d'être mute de : {guild.name} raison: {reason}")

@mute.error
async def mute(ctx, member: discord.Member, *, reason=None):
    await ctx.send('Tu ne peux pas effectuer cette action')

@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    memberr = get(guild.roles, name="Membre")

    await member.remove_roles(mutedRole)
    await member.add_roles(memberr)
    await member.send(f" tu viens d'être unmute de: {ctx.guild.name}")
    embed = discord.Embed(title="unmute", description=f" unmute-{member.mention}", colour=discord.Colour.light_gray())
    await ctx.send(embed=embed)
    
@unmute.error
async def unmute(ctx, member: discord.Member, *, reason=None):
    await ctx.send('Tu ne peux pas effectuer cette action')

##################################################################################

@bot.command()
async def slm(ctx, seconds: int):
    if seconds > 60:
        await ctx.send("La durée est trop élevée")
    else:
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Le slow mode est actif : {seconds} seconds!")

##################################################################################

bot.run(os.getenv("TOKEN"))
