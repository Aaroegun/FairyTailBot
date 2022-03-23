from discord.ext import commands
import discord
import json


class profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    


    @commands.command(aliases=["pf", "p"])
    async def profile(self, ctx, user: discord.User =  None):

        if user is None:
            user = ctx.author

        #---------------------------Opening Json Files-------------------------------------------
        with open("variables.json" , "r") as f:
             variables = json.load(f)

        with open("stats.json", "r") as f:
            userStats = json.load(f)
        #-----------------------------------------------------------------------------------------

        if str(user.id) not in userStats:
            userStats[str(user.id)] ={}
            userStats[str(user.id)]["totalMessage"] = 0
            userStats[str(user.id)]["keys"] = 0
            userStats[str(user.id)]["messageUntilDrain"] = 0
            userStats[str(user.id)]["messageUntilKey"] = 0
            userStats[str(user.id)]["credits"] = 0
        

        
        profileEmbed = discord.Embed(
            color =  0x8c03fc
        )

        profileEmbed.set_author(name=f"{user.display_name}'s Profile", icon_url=user.avatar_url)
        profileEmbed.set_image(url = user.avatar_url)
        
        profileEmbed.add_field(name = "Total Messages Sent 📧 : ",  value = f"`{userStats[str(user.id)]['totalMessage']}`" ,  inline=False)
        profileEmbed.add_field(name = "Total Keys 🔑 : ",  value= f"`{userStats[str(user.id)]['keys']}`" ,  inline=False)
        profileEmbed.add_field(name = "Messages Until Next Key 🔑 :",  value= f"`{ int(variables['messagesForKey']) - userStats[str(user.id)]['messageUntilKey']  }`" , inline=False)
        profileEmbed.add_field(name = "Messages Until Drain 💀 :", value= f"`{int(variables['dailyMessageLimit']) - userStats[str(user.id)]['messageUntilDrain']  }`" ,  inline=False)
        profileEmbed.add_field(name = "Total Credits 🪙 : ", value=f"`{userStats[str(user.id)]['credits']}`" , inline=False)


        await ctx.send(embed=profileEmbed)
    

    @commands.command(aliases=["credits" , "credit" , "bal" ])
    async def balance(self, ctx, user: discord.User = None):
        with open("stats.json" , "r") as f:
            userStats=json.load(f)
        
        if user is None:
            user = ctx.author
        if str(user.id) not in userStats:
            await ctx.send("Sorry but it seems like user hasn't came active yet")
        else:
            await ctx.send(f"{user.mention} currently has **{userStats[str(user.id)]['credits']} credits.**")
    

    @commands.command(aliases=["key"])
    async def keys(self, ctx, user: discord.User = None):
        with open("stats.json" , "r") as f:
            userStats=json.load(f)
        
        if user is None:
            user = ctx.author
        if str(user.id) not in userStats:
            await ctx.send("Sorry but it seems like user hasn't came active yet")
        else:
            await ctx.send(f"{user.mention} currently has **{userStats[str(user.id)]['keys']} keys.**")
    

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx, page = 1):
        with open("stats.json" , "r") as f:
            userStats = json.load(f)

        leaderboardEmbed = discord.Embed(
            title = "**LEADERBOARD ** 🏆",
            description = f"Page {page}",
            color = 0x00058a
        )
        
        creditDict = {}
        for users in userStats:
            creditDict[userStats[users]["credits"]] = users
        creditList = sorted(creditDict, reverse=True)
        
        newCreditDict = {}
        for data in creditList:
            newCreditDict[creditDict[data]] = data
        
        dataList = []
        for data in newCreditDict:
            dataList.append(str(newCreditDict[data])+"#"+str(data))
        

        for index in range(int(page-1)*10, int(page*10)-1):
            try:
                data = dataList[index]
                credit, userId = data.split("#")
                user = discord.utils.get(ctx.guild.members, id=int(userId))
                leaderboardEmbed.add_field(name ="#" + str(index+1)+" " + user.display_name, value="`"+credit+" credits `", inline=False)
            
            except:
                pass

        
        await ctx.send(embed=leaderboardEmbed)





  
        


def setup(client):
    client.add_cog(profile(profile))