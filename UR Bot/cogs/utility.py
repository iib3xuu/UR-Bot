import discord
from discord.ext import commands
from discord import Embed
import random
import datetime
import asyncio
import platform

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = 0x000001  # Hex color for embeds
        self.thumbnail_url = "https://cdn.discordapp.com/avatars/1290541182711103488/b66d2000a0eb1a23021750e89e44a9fe.png"  # Thumbnail URL

    def create_embed(self, title, description):
        """Utility to create consistent embeds."""
        embed = Embed(title=title, description=description, color=self.embed_color)
        embed.set_thumbnail(url=self.thumbnail_url)
        return embed

    # 1. Bot Info
    @commands.command()
    async def botinfo(self, ctx):
        """Display information about the bot."""
        embed = self.create_embed(
            "Bot Information",
            f"**Name:** {self.bot.user.name}\n"
            f"**ID:** {self.bot.user.id}\n"
            f"**Library:** discord.py\n"
            f"**Python Version:** {platform.python_version()}\n"
            f"**Bot Version:** 1.0.0\n"
            f"**Uptime:** Coming soon!"
        )
        await ctx.send(embed=embed)

    # 3. Channel List
    @commands.command()
    async def channels(self, ctx):
        """List all text channels in the server."""
        channels = [channel.name for channel in ctx.guild.text_channels]
        embed = self.create_embed(
            "Channel List",
            "\n".join(f"• {channel}" for channel in channels) or "No channels found."
        )
        await ctx.send(embed=embed)

    # 4. Role List
    @commands.command()
    async def roles(self, ctx):
        """List all roles in the server."""
        roles = [role.name for role in ctx.guild.roles if role.name != "@everyone"]
        embed = self.create_embed(
            "Role List",
            "\n".join(f"• {role}" for role in roles) or "No roles found."
        )
        await ctx.send(embed=embed)

    # 5. Emoji List
    @commands.command()
    async def emojis(self, ctx):
        """List all emojis in the server."""
        emojis = ctx.guild.emojis
        embed = self.create_embed(
            "Emoji List",
            " ".join(str(emoji) for emoji in emojis) or "No emojis found."
        )
        await ctx.send(embed=embed)

    # 6. Server Icon
    @commands.command()
    async def servericon(self, ctx):
        """Display the server's icon."""
        if ctx.guild.icon:
            embed = self.create_embed("Server Icon", "")
            embed.set_image(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("This server has no icon.")

    # 8. Server Age
    @commands.command()
    async def serverage(self, ctx):
        """Show how old the server is."""
        delta = datetime.datetime.utcnow() - ctx.guild.created_at
        embed = self.create_embed("Server Age", f"This server is {delta.days} days old!")
        await ctx.send(embed=embed)

    # 9. User Since
    @commands.command()
    async def usersince(self, ctx, member: discord.Member = None):
        """Show when a user joined the server."""
        member = member or ctx.author
        embed = self.create_embed(
            "User Since",
            f"{member.mention} joined the server on {member.joined_at.strftime('%Y-%m-%d')}."
        )
        await ctx.send(embed=embed)

    # 11. Say
    @commands.command()
    async def say(self, ctx, *, message: str):
        """Repeat the user's message."""
        embed = self.create_embed("Bot Says", message)
        await ctx.send(embed=embed)

    # 12. Count Roles
    @commands.command()
    async def countroles(self, ctx):
        """Show the number of roles in the server."""
        roles = len(ctx.guild.roles) - 1  # Exclude @everyone
        embed = self.create_embed("Role Count", f"This server has {roles} roles.")
        await ctx.send(embed=embed)

    # 13. Boost Count
    @commands.command()
    async def boostcount(self, ctx):
        """Show the number of boosts for the server."""
        boost_count = ctx.guild.premium_subscription_count
        embed = self.create_embed("Boost Count", f"🚀 This server has {boost_count} boosts.")
        await ctx.send(embed=embed)

    # 14. Check Invite
    @commands.command()
    async def checkinvite(self, ctx, invite: str):
        """Check the details of a Discord invite link."""
        try:
            invite_obj = await self.bot.fetch_invite(invite)
            embed = self.create_embed(
                "Invite Details",
                f"**Server Name:** {invite_obj.guild.name}\n"
                f"**Channel:** {invite_obj.channel.name}\n"
                f"**Inviter:** {invite_obj.inviter}\n"
                f"**Uses:** {invite_obj.uses}"
            )
            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send("Invalid invite link.")

    # 15. Role Members
    @commands.command()
    async def rolemembers(self, ctx, *, role: discord.Role):
        """Show the members with a specific role."""
        members = [member.mention for member in role.members]
        embed = self.create_embed(
            f"Members with {role.name}",
            "\n".join(members) or "No members have this role."
        )
        await ctx.send(embed=embed)

    # 16. Bot Latency
    @commands.command()
    async def latency(self, ctx):
        """Check the bot's latency."""
        latency = round(self.bot.latency * 1000)  # Convert to ms
        embed = self.create_embed("Bot Latency", f"🏓 Pong! Latency: {latency}ms")
        await ctx.send(embed=embed)

    # 19. Count Channels
    @commands.command()
    async def countchannels(self, ctx):
        """Show the number of channels in the server."""
        total_channels = len(ctx.guild.channels)
        embed = self.create_embed("Channel Count", f"This server has {total_channels} channels.")
        await ctx.send(embed=embed)

    # 20. Random Color
    @commands.command()
    async def randomcolor(self, ctx):
        """Generate a random color."""
        random_color = random.randint(0, 0xFFFFFF)
        embed = self.create_embed(
            "Random Color",
            f"Here's a random color: #{random_color:06X}"
        )
        embed.color = random_color
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
