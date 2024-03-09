import disnake
from disnake.ext import commands
from disnake.interactions.modal import ModalInteraction
from datetime import timedelta, datetime
from models.mod.models import Mute, MuteSettings, Warns
from core import db_helper
from asyncio import sleep
from sqlalchemy import select, insert
from config import MUTE_ROLE

sesion = db_helper.session_factory()


def check_time(duration: str) -> int:
        time_format = {
            'h': 3600,
            'm': 60,
            's': 1,
        }

        total_duration = 0
        current_num = ''

        for char in duration:
            if char.isdigit():
                current_num += char
            elif char.isalpha():
                if current_num:
                    num = int(current_num)
                    format_time = time_format.get(char)
                    if format_time:
                        total_duration += num * format_time
                    current_num = ''
        
        return total_duration


class MuteModal(disnake.ui.Modal):
    def __init__(self, member: disnake.Member):
        components = [
            disnake.ui.TextInput(label="Введите время", custom_id="time")
        ]
        self.member = member

        super().__init__(title="Команда мьют", components=components)
    
    async def callback(self, interaction: ModalInteraction):
        values = interaction.text_values
        seconds = check_time(values["time"])

        now = datetime.now()
        end_mute = now + timedelta(seconds=float(seconds))

        insert_query = insert(Mute).values(user_id=self.member.id, end_mute=round(end_mute.timestamp()))

        mute_role = interaction.guild.get_role(MUTE_ROLE)
        await sesion.execute(insert_query)
        await sesion.commit()
        await self.member.add_roles(mute_role)
        await interaction.response.send_message("Пользователь успешно замьючен")
        await sleep(seconds)
        await self.member.remove_roles(mute_role)


class ModButton(disnake.ui.View):
    def __init__(self, member: disnake.Member):
        self.member = member
        super().__init__(timeout=None)
    
    @disnake.ui.button(label="mute", style=disnake.ButtonStyle.green)
    async def mute(self, button, interaction: disnake.Interaction):
        if interaction.user != interaction.author:
            return await interaction.response.send_message("Это не ваша кнопка", ephemeral=True)

        return await interaction.response.send_modal(MuteModal(self.member))

    @disnake.ui.button(label="warn", style=disnake.ButtonStyle.green)
    async def warn(self, button, interaction: disnake.Interaction):
        if interaction.user != interaction.author:
            return await interaction.response.send_message("Это не ваша кнопка", ephemeral=True)

        warns = Warns()
        query = select(warns).where(warns.user_id == self.member.id)
        
            