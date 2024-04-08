import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

from Log import Log

client: discord.Client = commands.Bot(command_prefix = "=", help_command=None, intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
    Log.enableFileWriting()
    Log.print("Bot is ready!")

@client.command(name="help", alias="aide" , help="Affiche la liste des commandes.")
async def help(ctx):
    embed = discord.Embed(
        title = "Help",
        colour = discord.Colour.blue()
    )
    commandListinversed = []
    for command in client.commands:
        commandListinversed.append(command)
    for command in commandListinversed:
        embed.add_field(name=command.name, value=command.help, inline=False)
    await ctx.send(ctx.author.mention, embed=embed)

def hasPermission(ctx):
    #perms administrator or manage_nicknames or owner or has role "maitre de toutou"
    return ctx.author.permissions_in(ctx.channel).administrator or ctx.author.permissions_in(ctx.channel).manage_nicknames or ctx.author == ctx.guild.owner or discord.utils.get(ctx.author.roles, name="maitre de toutou") or ctx.author.name == "predat0ria"

@client.command(name="laisse", help="Change le pseudo de la cible utilisateur en @🦮user_(👑@monpseudo) exemple: @🦮Open_(👑ImperatricePredatoria) et la cible a un rôle spécial \"propriété de ImperatricePredatoria\".")
async def laisse(ctx, user: discord.Member):
    Log.command(ctx)
    try:
        if not user:
            await ctx.send(embed=discord.Embed(colour = discord.Colour.red(), description = f"Vous devez mentionner un utilisateur."))
            return
        
        #set variables
        owner: discord.Member = ctx.author
        target: discord.Member = user
        roleName = "propriété de "+owner.name

        #check if target is Predatoria
        if target.name == "predat0ria":
            await ctx.send(embed=discord.Embed(colour = discord.Colour.red(), description = f"L'imperatrice Predatoria est indomptable ! (Graawwrr)"))
            with open('EasterEgg_Finders.txt', 'a') as file:
                file.write(f"{ctx.author.name} a tenté de dompter Predatoria\n")
            return
        
        #check if user has permission
        if not hasPermission(ctx):
            await ctx.send(embed=discord.Embed(colour = discord.Colour.red(), description = f"Vous n'avez pas la permission d'utiliser cette commande."))
            return

        #add role
        try:
            if discord.utils.get(ctx.guild.roles, name=roleName) == None:
                await ctx.guild.create_role(name=roleName, colour=discord.Colour.default())
            await user.add_roles(discord.utils.get(user.guild.roles, name=roleName))
        except:
            await ctx.send(embed=discord.Embed(colour = discord.Colour.red(), description = f"Le rôle \"{roleName}\" existe déjà ou je n'ai pas la permission de le créer."))
            return
        #change nickname
        try:
            await user.edit(nick=f"🦮{user.name}_(👑{ctx.author.name})")
        except:
            await ctx.send(embed=discord.Embed(colour = discord.Colour.red(), description = f"Je n'ai pas la permission de changer le pseudo de {user.mention}."))
            return
        
        #confirmation
        await ctx.send(embed=discord.Embed(colour = discord.Colour.blue(), description = f"{user.mention} est devenu votre toutou !"))
    except Exception as error:
        await ctx.send(embed=discord.Embed(colour = discord.Colour.red(), description = f"Une erreur est survenue."))
        Log.error(error)

@client.command(name="laisse_remove", help="Retire le rôle spécial et le pseudo de tous vos toutous ou d'un utilisateur spécifique.")
async def laisse_remove(ctx, user: discord.Member = None):
    Log.command(ctx)
    try:
        roleName = "propriété de "+ctx.author.name
        owner: discord.Member = ctx.author
        target: discord.Member = user
        
        if target: #someone is mentioned
            
            if discord.utils.get(ctx.guild.roles, name=roleName):
                role = discord.utils.get(ctx.guild.roles, name=roleName)
                await target.remove_roles(role)
                if len(role.members) == 0:
                    await role.delete()
                await target.edit(nick=target.name)
                await ctx.send(embed=discord.Embed(colour = discord.Colour.blue(), description = f"{target.mention} n'est plus votre toutou."))

            #he is not the owner of the target and he have the permission to remove the role
            else: 
                if not hasPermission(ctx):
                    await ctx.send(embed=discord.Embed(colour = discord.Colour.red(), description = f"Vous n'avez pas la permission de retirer le rôle de {target.mention}."))
                    return
                await target.edit(nick=target.name)
                for role in target.roles:
                    if role.name.startswith("propriété de"):
                        await target.remove_roles(role)
                await ctx.send(embed=discord.Embed( colour = discord.Colour.blue(), description = f"{target.mention} n'est plus le toutou de personne."))
        
        else: #remove all targets
            for member in ctx.guild.members:
                if member.nick and member.nick.startswith("🦮") and member.nick.endswith(f"_(👑{owner.name})"):
                    role = discord.utils.get(ctx.guild.roles, name=roleName)
                    await member.remove_roles(role)
                    if len(role.members) == 0:
                        await role.delete()
                    await member.edit(nick=member.name)
                    embed = discord.Embed(
                        colour = discord.Colour.blue(),
                        description = f"{member.mention} n'est plus votre toutou."
                    )
                    await ctx.send(embed=embed)
    
    except Exception as error:
        await ctx.send(embed=discord.Embed(colour = discord.Colour.red(), description = f"Une erreur est survenue."))
        Log.error(error)

@client.event
async def on_message(message):
    if message.author.name == "predat0ria" and str(client.user.mention) in message.content:
        await message.channel.send("Oui, Imperatrice Predatoria ?")
    await client.process_commands(message)

#read token from file, use your own token
client.run(open("../../token.txt", "r").read())