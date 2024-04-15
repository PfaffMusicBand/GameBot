from discord.ext import commands
from discord.ext.commands import Context
import Botloader

class Admin(commands.cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="clear", help=f"Suprimé les n dernier messages dans le channel.\nSyntaxe: `{Botloader.Bot.Prefix}clear <argument(int)>`")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: Context, amount):
        try:
            await ctx.channel.purge(limit=int(amount))
        except ValueError:
            await ctx.send('Please enter a valid integer as amount.')