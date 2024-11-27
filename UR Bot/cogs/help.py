import discord
from discord.ext import commands
from discord import Embed, ui, Interaction
import math

class HelpPaginator(ui.View):
    def __init__(self, ctx, embeds):
        super().__init__(timeout=60)  # Timeout for the interaction
        self.ctx = ctx
        self.embeds = embeds
        self.current_page = 0
        self.update_buttons()

    def update_buttons(self):
        """Update button states based on the current page."""
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == len(self.embeds) - 1
        self.page_button.label = f"Page {self.current_page + 1}/{len(self.embeds)}"

    async def interaction_check(self, interaction: Interaction):
        """Ensure only the author can use the buttons."""
        return interaction.user.id == self.ctx.author.id

    @ui.button(label="◀️", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: Interaction, button: ui.Button):
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @ui.button(label="Page 1", style=discord.ButtonStyle.secondary, disabled=True)
    async def page_button(self, interaction: Interaction, button: ui.Button):
        pass  # This button is just for display

    @ui.button(label="▶️", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: Interaction, button: ui.Button):
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = 0x000001  # Hex color for embeds
        self.thumbnail_url = "https://cdn.discordapp.com/avatars/1290541182711103488/b66d2000a0eb1a23021750e89e44a9fe.png"  # Thumbnail URL

    def create_embed(self, title, description):
        """Utility to create a consistent embed."""
        embed = Embed(title=title, description=description, color=self.embed_color)
        embed.set_thumbnail(url=self.thumbnail_url)
        return embed

    @commands.command(name="help")
    async def help_command(self, ctx):
        """This shows you the commands available to use."""
        commands_per_page = 10
        embeds = []

        # Organize commands by cogs
        for cog_name, cog in self.bot.cogs.items():
            commands_list = cog.get_commands()
            command_strings = [
                f"`{ctx.prefix}{cmd.name}`: {cmd.help or 'No description available.'}"
                for cmd in commands_list if not cmd.hidden
            ]

            # Paginate commands within each cog
            for i in range(0, len(command_strings), commands_per_page):
                page_content = "\n".join(command_strings[i:i + commands_per_page])
                embed = self.create_embed(cog_name, page_content or "No commands available.")
                embeds.append(embed)

        # Handle empty help (no commands)
        if not embeds:
            embed = self.create_embed("Help", "No commands available.")
            embeds.append(embed)

        # Send the first page with navigation buttons
        view = HelpPaginator(ctx, embeds)
        await ctx.send(embed=embeds[0], view=view)

async def setup(bot):
    await bot.add_cog(CustomHelp(bot))
