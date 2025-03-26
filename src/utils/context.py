import discord


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__(disable_on_timeout=True)
        self.value = None

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.message.interaction_metadata.user.id:
            embed = discord.Embed(
                color=0xE02B2B,
                description="You cannot interact with this message.",
            )
            await interaction.respond(embed=embed, ephemeral=True)
            return False
        return True

    async def process_response(self, value: bool):
        self.value = value
        self.stop()

        try:
            await self.message.edit(view=None)
        except discord.NotFound:
            pass

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.process_response(True)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, button: discord.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.process_response(False)


class Context(discord.ApplicationContext):
    async def confirm(self, prompt: str):
        view = Confirm()

        await self.respond(prompt, view=view)
        await view.wait()

        return view.value
