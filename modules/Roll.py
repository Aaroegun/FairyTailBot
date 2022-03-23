from discord.ext import commands
import json
import random


class ticket(commands.Cog):
    def __init__(self, client):
        self.client  = client



    @commands.command()
    async def roll(self, ctx):
        with open("variables.json" , "r") as f:
            variables = json.load(f)
        
        with open("stats.json" , "r") as f:
            userStats = json.load(f)

        try:
            if userStats[str(ctx.author.id)]["keys"] <=0:
                await ctx.send("Sorry, but it seems like you don't have any keys 🤦")
            
            else:
                earnedCredits = random.randint(int(variables["minRollCredits"]) , int(variables["maxRollCredits"]))

                userStats[str(ctx.author.id)]["keys"] -=1
                userStats[str(ctx.author.id)]["credits"] += earnedCredits

                with open("stats.json" , "w") as f:
                    json.dump(userStats, f, indent=4)
                await ctx.send(f"Congratulations! You have won {earnedCredits} credits. 🎉🎉")
        except:
            await ctx.send("Sorry a Error has occuered, No keys deducted.")
        

        



        

        



def setup(client):
    client.add_cog(ticket(ticket))