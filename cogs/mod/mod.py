from disnake import Member
from disnake.ext import commands
from components.buttons.mod_buttons import ModButton


class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.slash_command(name='action')
    async def action(self, interaction, member: Member):
        if interaction.author.guild_permissions < member.guild_permissions or member == interaction.author:
            return await interaction.send("У вас нет прав на выполнение этой команды")
        return await interaction.send(view=ModButton(member))


def setup(bot):
    bot.add_cog(Mod(bot))