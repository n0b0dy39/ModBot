import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.commands import has_permissions, MissingPermissions, CheckFailure, BadArgument
load_dotenv(dotenv_path="config")

default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix="'", intents=default_intents)
bot = commands.Bot(help_command=None)


##################################################################################

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("'help"))
    print("Le bot est connecté.")


##################################################################################

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))


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
    if number > 5:
        await ctx.send(f'Tu ne peux pas dépasser 6 messages or tu a mis {number}')
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
    await member.kick(reason=reason)
    await ctx.send(f'{member} viens de se faire kick.')


@kick.error
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.send("Tu ne peux pas effectuer cette action")

##################################################################################

@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} viens de se faire ban.')

@ban.error
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.send("Tu ne peux pas effectuer cette action")

##################################################################################

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour=discord.Colour.blue()
    )

    embed = discord.Embed(title="-- Help --", description="Commandes bot", color=0x7289da)
    embed.add_field(name="del [nombre]", value="Supprime les messages", inline=False)
    embed.add_field(name="roles [@membre]", value="Montre les roles du membre mentionné", inline=False)
    embed.add_field(name="avatar [@membre]", value="Montre la photo de profile du membre mentionné", inline=False)
    embed.add_field(name="kick [@membre]", value="Kick le membre mentionné", inline=False)
    embed.add_field(name="ban [@membre]", value="Ban le membre mentionné", inline=False)
    embed.add_field(name="ping", value="Montre votre connexion au serveur", inline=False)
    embed.set_footer(text="ModBot | W⁷⁸#3422")

    await ctx.send(embed=embed)

##################################################################################

bot.run(os.getenv("TOKEN"))
