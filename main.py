from cgitb import text
from discord.ext import commands
import discord
import os
import time
import json
import humanfriendly





intents =discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=",", intents=intents)


client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Streaming(name="osu!", url="https://www.twitch.tv/aaroegun"))



@client.event
async def on_message(message):



    Drained = discord.utils.get(message.guild.roles, name="Drained")

    #------------Opening Json files---------------------------------------

    with open("variables.json" , "r") as f:
        variables = json.load(f)

    with open("cooldowns.json", "r") as f:
        cooldowns=json.load(f)

    with open("stats.json", "r") as f:
        userStats = json.load(f)

    with open("drained.json", "r") as f:
        userDat = json.load(f)

    #----------------------------------------------------------------------------

    #----------------------Alaways Check-----------------------------------------


    if int(cooldowns["drainCooldown"]) < time.time():
        

        for users in userDat["drainedUsers"]:

            user = discord.utils.get(message.guild.members, id = int(users))
            userStats[str(user.id)]["messageUntilDrain"] = 0
            await user.remove_roles(Drained)


        userDat["drainedUsers"] = []
        cooldowns["drainCooldown"] = time.time() + int(variables["drainReset"])

    
    if int(cooldowns["dailyKeysCooldown"]) < time.time():

        for users in userStats:
            
            try:
                if userStats[users]["keys"] <6:
                    userStats[users]["keys"] += 1
            
            except:
                pass
        
        cooldowns["dailyKeysCooldown"] = int(variables["dailyKeysCooldown"]) + time.time()
    
    #-------------------------------------------------------------------------------

    #------------------------On Message---------------------------------------------

    if str(message.author.id) not in userStats:
        userStats[str(message.author.id)] ={}
        userStats[str(message.author.id)]["totalMessage"] = 0
        userStats[str(message.author.id)]["keys"] = 0
        userStats[str(message.author.id)]["messageUntilDrain"] = 0
        userStats[str(message.author.id)]["messageUntilKey"] = 0
        userStats[str(message.author.id)]["credits"] = 0
    

    userStats[str(message.author.id)]["totalMessage"] += 1

    if Drained not in message.author.roles:
        userStats[str(message.author.id)]["messageUntilDrain"] += 1
        userStats[str(message.author.id)]["messageUntilKey"] += 1

    
    if userStats[str(message.author.id)]["messageUntilKey"] > variables["messagesForKey"]  and  userStats[str(message.author.id)]["keys"] < variables["keysLimit"]:
        userStats[str(message.author.id)]["keys"] += 1
        userStats[str(message.author.id)]["messageUntilKey"] = 0

    if userStats[str(message.author.id)]["messageUntilDrain"] > variables["dailyMessageLimit"] and int(message.author.id) not in userDat["drainedUsers"]:
        userDat["drainedUsers"].append(str(message.author.id))
        await message.author.add_roles(Drained)
    
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    

    


    #----------Closing Json files--------------------------------------------------
    with open("cooldowns.json" , "w") as f:
        json.dump(cooldowns, f, indent=4)
    
    with open("stats.json" ,"w") as f:
        json.dump(userStats, f, indent=4)
    
    with open("drained.json" , "w") as f:
        json.dump(userDat, f, indent=4)
    

    #------------------command process-----------------------------------

    if str(message.author.id) in userDat["bannedUsers"]:
        await message.channel.send("You are banned from using any commands of this bot. ❎ ")
    
    else:
        await client.process_commands(message)

    




@client.command()
async def drain(ctx):

    with open("cooldowns.json" , "r") as f:
        cooldowns = json.load(f)
    
    duration = round(cooldowns["drainCooldown"] - time.time())

    await ctx.send(f"{humanfriendly.format_timespan(duration)} left until next Drain reset.  <:lector:849427691597463562> ") 



@commands.has_role("Bot Manager")
@client.command(aliases=["ext"])
async def extensions(ctx, method = "show" , extension = None):

    if method == "show":

        extensionEmbed = discord.Embed(
            title = "Available Extensions"
        )

        for files in os.listdir(".\modules"):

            if files.endswith(".py"):

                extensionEmbed.add_field(name = files[:-3], value=None, inline= False)
        
        await ctx.send(embed = extensionEmbed)
    
    elif method  == "load":
        
        try:
            client.load_extension(f"modules.{extension}")
            await ctx.send(f"{extension} loaded succesfully")

        except:
            await ctx.send(f"Sorry, extension could not be loaded")
    
    elif method == "unload":
        try:
            client.unload_extension(f"modules.{extension}")
            await ctx.send(f"{extension} unloaded succesfully")

        except:
            await ctx.send(f"Sorry, extension could not be unloaded")




@commands.has_role("Bot Manager")
@client.command()
async def backup(ctx):
    await ctx.send(file=discord.File(r".\modules\help.py"))
    time.sleep(5)
    await ctx.send(file=discord.File(r".\modules\Moderation.py"))
    time.sleep(5)
    await ctx.send(file=discord.File(r".\modules\Profile.py"))
    time.sleep(5)
    await ctx.send(file=discord.File(r".\modules\Roll.py"))
    time.sleep(5)
    await ctx.send(file=discord.File(r".\modules\Variables.py"))
    time.sleep(5)
    await ctx.send(file=discord.File(r".\cooldowns.json"))
    time.sleep(5)
    await ctx.send(file=discord.File(r".\drained.json"))
    time.sleep(5)
    await ctx.send(file=discord.File(r".\stats.json"))
    time.sleep(5)
    await ctx.send(file=discord.File(r".\variables.json"))
    time.sleep(5)
    await ctx.send(file=discord.File(r".\main.py"))



for files in os.listdir(".\modules"):
    if files.endswith(".py"):
        client.load_extension(f"modules.{files[:-3]}")
        print(f"{files[:-3]} loaded sucessfully")


client.run("OTUzNDk2MjM3OTA1MTY2MzQ2.YjFakg.YOAhNqg-6MiBTcdTXNITOZyZ8oo")


