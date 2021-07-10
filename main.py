import os
import discord
from discord import message
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
@bot.command(description="del")
@has_permissions(administrator=True)
async def delete(ctx, number: int):
    messages = await ctx.channel.history(limit=number + 1).flatten()
    if number >= 11:
        embed = discord.Embed(title="Erreur :", description=f"Tu ne peux pas dépasser 10 or tu as mis {number}",
                              colour=discord.Colour.dark_blue())
        await ctx.send(embed=embed)
    else:
        for each_message in messages:
            await each_message.delete()
 
 
@delete.error
async def delete(ctx, number: int):
    embed = discord.Embed(title="Erreur :", description=f"Tu ne peux pas effectuer cette action",
                          colour=discord.Colour.dark_blue())
    await ctx.send(embed=embed)
 
 
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
                          colour=discord.Colour.dark_blue())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.send(f" tu viens d'être kick de : {guild.name} raison: {reason}")
 
 
@kick.error
async def kick(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(title="Erreur :", description=f"Tu ne peux pas effectuer cette action",
                          colour=discord.Colour.dark_blue())
    await ctx.send(embed=embed)
 
 
##################################################################################
 
 
@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    await member.ban(reason=reason)
    embed = discord.Embed(title="Ban", description=f"{member.mention} est ban ", colour=discord.Colour.dark_blue())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
 
 
@ban.error
async def ban(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(title="Erreur :", description=f"Tu ne peux pas effectuer cette action",
                          colour=discord.Colour.dark_blue())
    await ctx.send(embed=embed)
 
 
############################################################
 
@bot.command()
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
 
    for ban_entry in banned_users:
        user = ban_entry.user
 
    if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send(f"{user} have been unbanned sucessfully")
        return
 
 
@unban.error
async def unban(ctx, *, member):
    embed = discord.Embed(title="Erreur :", description=f"Tu ne peux pas effectuer cette action",
                          colour=discord.Colour.dark_blue())
    await ctx.send(embed=embed)
 
 
##################################################################################
 
@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour=discord.Colour.dark_blue()
    )
 
    embed = discord.Embed(title="-- Help --", description="Commandes bot | prefix : >", color=0x3498db)
    embed.add_field(name="ping", value="Montre votre connexion au serveur", inline=False)
    embed.add_field(name="del [nombre]", value="Supprime les messages", inline=False)
    embed.add_field(name="roles [@membre]", value="Montre les roles du membre mentionné", inline=False)
    embed.add_field(name="avatar [@membre]", value="Montre la photo de profile du membre mentionné", inline=False)
    embed.add_field(name="kick [@membre]", value="Kick le membre mentionné", inline=False)
    embed.add_field(name="ban [@membre]", value="Ban le membre mentionné", inline=False)
    embed.add_field(name="mute [@membre]", value="Mute le membre mentionné", inline=False)
    embed.add_field(name="unmute [@membre]", value="Unmute le membre mentionné", inline=False)
    embed.add_field(name="mod [@membre]", value="Donne le grade Modo pour le membre mentionné", inline=False)
    embed.add_field(name="unmod [@membre]", value="Supprime le grade Modo pour le membre mentionné", inline=False)
    embed.add_field(name="slm [temps en seconde]", value="Active le slow mode", inline=False)
    embed.add_field(name="ns [mess sondage]", value="Fais un sondage", inline=False)
 
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
 
    embed = discord.Embed(title="muted", description=f"{member.mention} est mute ", colour=discord.Colour.dark_blue())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" tu viens d'être mute de : {guild.name} raison: {reason}")
 
 
@mute.error
async def mute(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(title="Erreur :", description=f"Tu ne peux pas effectuer cette action",
                          colour=discord.Colour.dark_blue())
    await ctx.send(embed=embed)
 
 
############################################################
 
@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    memberr = get(guild.roles, name="Membre")
 
    await member.remove_roles(mutedRole)
    await member.add_roles(memberr)
    await member.send(f" tu viens d'être unmute de: {ctx.guild.name}")
    embed = discord.Embed(title="unmute", description=f" unmute-{member.mention}", colour=discord.Colour.dark_blue())
    await ctx.send(embed=embed)
 
 
@unmute.error
async def unmute(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(title="Erreur :", description=f"Tu ne peux pas effectuer cette action",
                          colour=discord.Colour.dark_blue())
    await ctx.send(embed=embed)
 
 
##################################################################################
 
@bot.command()
@commands.has_permissions(manage_messages=True)
async def slm(ctx, seconds: int):
    if seconds > 60:
        embed = discord.Embed(title="Erreur :",
                              description=f"La durée est trop élevée, elle ne peut pas dépasser 60 secondes or tu as mis : {seconds}",
                              colour=discord.Colour.dark_blue())
        await ctx.send(embed=embed)
    else:
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(title="Slow Mode", description=f"Le slow mode est maintenant actif : {seconds} secondes",
                              colour=discord.Colour.dark_blue())
        await ctx.send(embed=embed)
 
 
@slm.error
async def slm(ctx, seconds: int):
    embed = discord.Embed(title="Erreur :", description=f"Tu ne peux pas effectuer cette action",
                          colour=discord.Colour.dark_blue())
    await ctx.send(embed=embed)
 
 
##################################################################################
 
@bot.command()
@commands.has_role("Fondateur")
async def mod(ctx, member: discord.Member):
    guild = ctx.guild
    modRole = get(guild.roles, name="Modo")
 
    await member.add_roles(modRole)
    embed = discord.Embed(title="Modo", description=f"{member.mention} Viens d'être mis modo",
                          colour=discord.Colour.dark_blue())
    await ctx.send(embed=embed)
 
 
@mod.error
async def mod(ctx, member: discord.Member):
    embed = discord.Embed(title="Erreur :", description=f"Tu ne peux pas effectuer cette action",
                          colour=discord.Colour.dark_blue())
    await ctx.send(embed=embed)
 
 
############################################################
 
@bot.command(description="Unmod a specified user.")
@commands.has_role("Fondateur")
async def unmod(ctx, member: discord.Member):
    modoRole = discord.utils.get(ctx.guild.roles, name="Modo")
 
    await member.remove_roles(modoRole)
    embed = discord.Embed(title="Modo", description=f"{member.mention} n'as plus le rôle de modo",
                          colour=discord.Colour.dark_blue())
    await ctx.send(embed=embed)
 
 
@unmod.error
async def unmod(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(title="Erreur :", description=f"Tu ne peux pas effectuer cette action",
                          colour=discord.Colour.dark_blue())
    await ctx.send(embed=embed)
 
 
##################################################################################
@bot.command()
async def ns(ctx, *, mess):
 
    emoji = '✅'
    emojis = '❌'
 
    embed = discord.Embed(title=f"Nouveau Sondage", description=mess, colour=discord.Colour.dark_blue())
 
    emb = await ctx.send(embed=embed)
    await emb.add_reaction(emoji)
    await emb.add_reaction(emojis)
 
##################################################################################
@bot.command()
async def nd(ctx, *, debatchn:str):
  
  
  guild = ctx.message.guild
  
  name = 'Débats'
  category = discord.utils.get(ctx.guild.categories, name=name)
  await guild.create_text_channel(debatchn, category=category)
  channel = discord.utils.get(ctx.guild.channels, name=debatchn) 
  channel_id = channel.id
  channel = bot.get_channel(channel_id)
  embed = discord.Embed(title=f"Nouveau débat", description=debatchn, colour=discord.Colour.dark_blue())
  await channel.send(f'Nouveau débat')


bot.run(os.getenv("TOKENN"))
