from discord.ext import commands
import discord
import json
import time
import humanfriendly

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.has_role("Bot Manager")
    @commands.command()
    async def ban(self, ctx, user: discord.User):

        #-------------------------Opening Json Files-------------------------------
        with open("drained.json") as f:
            userDat=json.load(f)
        #-----------------------------------------------------------------------------



        if str(user.id) == str(ctx.author.id):

            await ctx.send("you can't ban yourself")
        
        else:

            if str(user.id) not in userDat["bannedUsers"]:

                try:

                    userDat["bannedUsers"].append(str(user.id))
                    await ctx.send(f"{user.mention} has been banned from bot")
                
                except:

                    await ctx.send("Failed to Ban the User")
            
            else:

                await ctx.send("User is already banned")


#-------------------------------------------------------------------------------------------------

        with open("drained.json" , "w") as f:
            json.dump(userDat, f, indent=4)
    







    @commands.has_role("Bot Manager")
    @commands.command()
    async def unban(self, ctx, user: discord.User):

#--------------------------------------------------Opening Json File-----------------------------------
        with open("drained.json") as f:
            userDat=json.load(f)
#-------------------------------------------------------------------------------------------------------


        if str(user.id) not in userDat["bannedUsers"]:

            await ctx.send("User is not Banned")
        
        else:

            try:

                userDat["bannedUsers"].remove(str(user.id))
                await ctx.send(f"{user.mention} has been unbanned from bot")

            except:

                await ctx.send("Failed to Unban User")
        
#--------------------------------------------------------------------------------------------------
        with open("drained.json" , "w") as f:
            json.dump(userDat, f, indent=4)




    @commands.has_role("Bot Manager")
    @commands.command()
    async def unbanall(self, ctx):
        with open("drained.json") as f:
            userDat=json.load(f)
        
        userDat["bannedUsers"] = []

        with open("drained.json" , "w") as f:
            json.dump(userDat, f, indent=4)
        
        await ctx.send("All the banned users have been unbanned")






    @commands.has_role("Bot Manager")
    @commands.command()
    async def user(self, ctx, user: discord.User, method="show", stats=None, value=0):

#-------------------------------------------Opening Json File-------------------------------------------
        with open("stats.json", "r") as f:
            userStats=json.load(f)
        
#-------------------------------------------------------------------------------------------------------

        if method == "show":
            
            try:
                userEmbed = discord.Embed(
                    title =f"{user.display_name}'s stats",
                    color=0xed0000
                )

                for userStat in userStats[str(user.id)]:
                    
                    userEmbed.add_field(name= userStat, value=userStats[str(user.id)][userStat], inline=True)
                
                await ctx.send(embed=userEmbed)
            except:
                await ctx.send("Unexpected Error Occured")
           
        
        elif method == "set" or method == "edit":
            try:
                value = int(value)
                userStats[str(user.id)][str(stats)] = value
                
                with open("stats.json","w") as f:
                    json.dump(userStats, f, indent=4)

                await ctx.send(f"**Changed Made for {user.mention} **: \n `{stats} : {value}`")
            
            except:
                await ctx.send("Failed to make changes")


    @commands.has_role("Bot Manager")
    @commands.command(aliases=["cd"])
    async def cooldown(self, ctx, method = "show", cooldown = None, value = 10):

        with open("cooldowns.json", "r") as f:
            cooldowns = json.load(f)
        
        if method == "show":
            
            cooldownEmbed = discord.Embed(
                title="Cooldowns",
                color=0xffffff
            )

            for Cooldown in cooldowns:

                cooldownEmbed.add_field(name= Cooldown, value=humanfriendly.format_timespan(round(int(cooldowns[Cooldown]) - time.time())), inline=False)
            
            await ctx.send(embed=cooldownEmbed)
        
        elif method == "set" or method == "edit":
            
         
                value = int(value)
                cooldowns[cooldown] = time.time() + value

                with open("cooldowns.json", "w") as f:
                    json.dump(cooldowns,f,indent=4)
                
                await ctx.send(f"Cooldown for {cooldown} has been set to {humanfriendly.format_timespan(round(int(cooldowns[cooldown]) - time.time()))} for now.")
            
            


        
            


        








def setup(client):
    client.add_cog(moderation(moderation))