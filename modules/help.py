from discord.ext import commands
import discord



class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.command()
    async def help(self, ctx, command = None):

        helpEmbed  = discord.Embed(
            title="**Help Page**",
            color = 0xce00f2
        )

        if command is None:
            helpEmbed.add_field(name="drain", value = "`Returns duration until next Drain reset.`", inline=False)
            helpEmbed.add_field(name="profile" , value="`Shows Profile of a User.`", inline=False)
            helpEmbed.add_field(name="leaderboard" , value="`Shows Leaderboard`", inline=False)
            helpEmbed.add_field(name="roll" , value="`Uses a key to roll for credits.`", inline=False)
            helpEmbed.add_field(name = "balance" , value="`Shows credits of a User`", inline=False)
            helpEmbed.add_field(name = "keys" , value="`Shows keys of a User`", inline=False)
            helpEmbed.set_footer(text="Type help <command name> for more info related to command")
            await ctx.send(embed=helpEmbed)

        elif command == "drain":
            helpEmbed.add_field(name="drain, dr", value="Usage \n `,drain`", inline=False)
            await ctx.send(embed=helpEmbed)
        
        elif command == "profile":
            helpEmbed.add_field(name = "profile, pf, p" , value= "Usage \n `,profile (user)`" , inline=False)
            helpEmbed.set_footer(text= "() Optional, <> Mandatory")
            await ctx.send(embed=helpEmbed)
        
        elif command == "leaderboard":
            helpEmbed.add_field(name="leaderboard, lb" , value="Usage \n `,leaderboard (page)`",inline=False)
            helpEmbed.set_footer(text= "() Optional, <> Mandatory")
            await ctx.send(embed=helpEmbed)
        
        elif command == "roll":
            helpEmbed.add_field(name="roll" , value="Usage \n `,roll`", inline=False)
            await ctx.send(embed=helpEmbed)
        
        elif command == "balance":
            helpEmbed.add_field(name="balance, bal, credits, credit", value="Usage \n `,balance (user)`" , inline=False)
            helpEmbed.set_footer(text= "() Optional, <> Mandatory")
            await ctx.send(embed=helpEmbed)
        
        elif command == "keys":
            helpEmbed.add_field(name="keys", value="Usage \n `,keys (User)`" , inline=False)
            helpEmbed.set_footer(text= "() Optional, <> Mandatory")
            await ctx.send(embed=helpEmbed)
        
        else:
            await ctx.send("No command found.")
        




def setup(client):
    client.add_cog(help(help))