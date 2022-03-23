import json
from discord.ext import commands
import discord

class Variable(commands.Cog):
    def __intit__(self, client):
        self.client = client

    
    @commands.has_role("Bot Manager")
    @commands.command(aliases=["var"])
    async def variable(self, ctx, method = "show", variable =  None, value = None):

    

        with open("variables.json" , "r") as f:
            variables = json.load(f)


        if method == "show":

            variableEmbed = discord.Embed(
                title="Variables",
                color =0xb4ed09
            )

            for variable in variables:
                variableEmbed.add_field(name = variable, value=variables[variable])
            
            await ctx.send(embed=variableEmbed)
        
        if method == "set" or method == "edit":
            try:
                value = int(value)

                variables[variable] = value
                with open("variables.json" , "w") as f:
                    json.dump(variables, f, indent=4)

                await ctx.send(f"{variable} set to {variables[variable]}")
            except:
                await ctx.send("value is not a integer")
                pass
        
    













def setup(client):
    client.add_cog(Variable(Variable))