import discord
from discord.ext import commands
from discord import Embed
import asyncio

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = 0x000001  # Hex color for embeds
        self.thumbnail_url = "https://cdn.discordapp.com/embed/avatars/0.png"  # Set your bot's thumbnail URL here

    def create_embed(self, title, description):
        """Utility to create consistent embeds."""
        embed = Embed(title=title, description=description, color=self.embed_color)
        embed.set_thumbnail(url=self.thumbnail_url)
        return embed

    # 1. Kick a Member
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from the server."""
        await member.kick(reason=reason)
        embed = self.create_embed(
            "Member Kicked",
            f"🚨 {member.mention} has been kicked.\n**Reason:** {reason or 'No reason provided.'}"
        )
        await ctx.send(embed=embed)

    # 2. Ban a Member
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member from the server."""
        await member.ban(reason=reason)
        embed = self.create_embed(
            "Member Banned",
            f"🔨 {member.mention} has been banned.\n**Reason:** {reason or 'No reason provided.'}"
        )
        await ctx.send(embed=embed)

    # 3. Unban a Member
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member_name):
        """Unban a member by name."""
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name == member_name:
                await ctx.guild.unban(user)
                embed = self.create_embed(
                    "Member Unbanned",
                    f"✅ {user.mention} has been unbanned."
                )
                await ctx.send(embed=embed)
                return
        await ctx.send(f"No user named `{member_name}` found in banned list.")

    # 4. Clear Messages
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        """Clear a number of messages."""
        await ctx.channel.purge(limit=amount)
        embed = self.create_embed("Messages Cleared", f"🧹 Cleared {amount} messages.")
        await ctx.send(embed=embed)

    # 5. Mute a Member
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        """Mute a member."""
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            await ctx.send("Muted role not found. Please create one.")
            return
        await member.add_roles(mute_role, reason=reason)
        embed = self.create_embed(
            "Member Muted",
            f"🔇 {member.mention} has been muted.\n**Reason:** {reason or 'No reason provided.'}"
        )
        await ctx.send(embed=embed)

    # 6. Unmute a Member
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a member."""
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            await ctx.send("Muted role not found.")
            return
        await member.remove_roles(mute_role)
        embed = self.create_embed("Member Unmuted", f"🔊 {member.mention} has been unmuted.")
        await ctx.send(embed=embed)

    # 7. Lock Channel
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        """Lock the current channel."""
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = self.create_embed("Channel Locked", "🔒 This channel is now locked.")
        await ctx.send(embed=embed)

    # 8. Unlock Channel
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        """Unlock the current channel."""
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = self.create_embed("Channel Unlocked", "🔓 This channel is now unlocked.")
        await ctx.send(embed=embed)

    # 9. Slow Mode
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        """Set slow mode for the current channel."""
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = self.create_embed(
            "Slow Mode Set",
            f"🐢 Slow mode has been set to {seconds} seconds."
        )
        await ctx.send(embed=embed)

    # 10. Create Role
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def create_role(self, ctx, *, name):
        """Create a role."""
        role = await ctx.guild.create_role(name=name)
        embed = self.create_embed("Role Created", f"✅ Role `{role.name}` has been created.")
        await ctx.send(embed=embed)

    # 11. Delete Role
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def delete_role(self, ctx, *, name):
        """Delete a role."""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if not role:
            await ctx.send(f"Role `{name}` not found.")
            return
        await role.delete()
        embed = self.create_embed("Role Deleted", f"❌ Role `{name}` has been deleted.")
        await ctx.send(embed=embed)

    # 12. Add Role
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def add_role(self, ctx, member: discord.Member, *, role_name):
        """Add a role to a member."""
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"Role `{role_name}` not found.")
            return
        await member.add_roles(role)
        embed = self.create_embed(
            "Role Added",
            f"✅ Role `{role.name}` has been added to {member.mention}."
        )
        await ctx.send(embed=embed)

    # 13. Remove Role
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx, member: discord.Member, *, role_name):
        """Remove a role from a member."""
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"Role `{role_name}` not found.")
            return
        await member.remove_roles(role)
        embed = self.create_embed(
            "Role Removed",
            f"❌ Role `{role.name}` has been removed from {member.mention}."
        )
        await ctx.send(embed=embed)

    # 14. Change Nickname
    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, nickname):
        """Change a member's nickname."""
        await member.edit(nick=nickname)
        embed = self.create_embed(
            "Nickname Changed",
            f"✅ {member.mention}'s nickname has been changed to `{nickname}`."
        )
        await ctx.send(embed=embed)

    # 15. Create Text Channel
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def create_text_channel(self, ctx, *, name):
        """Create a text channel."""
        channel = await ctx.guild.create_text_channel(name)
        embed = self.create_embed(
            "Text Channel Created",
            f"✅ Text channel `{channel.name}` has been created."
        )
        await ctx.send(embed=embed)

    # 16. Delete Text Channel
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def delete_text_channel(self, ctx, *, name):
        """Delete a text channel."""
        channel = discord.utils.get(ctx.guild.text_channels, name=name)
        if not channel:
            await ctx.send(f"Text channel `{name}` not found.")
            return
        await channel.delete()
        embed = self.create_embed(
            "Text Channel Deleted",
            f"❌ Text channel `{name}` has been deleted."
        )
        await ctx.send(embed=embed)

    # 17. Announce
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def announce(self, ctx, *, message):
        """Make an announcement."""
        embed = self.create_embed("Announcement", message)
        await ctx.send(embed=embed)

    # 18. Shutdown Bot
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shut down the bot."""
        embed = self.create_embed("Shutdown", "🛑 Bot is shutting down.")
        await ctx.send(embed=embed)
        await self.bot.close()

    # 19. Change Server Name
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def rename_server(self, ctx, *, name):
        """Change the server's name."""
        await ctx.guild.edit(name=name)
        embed = self.create_embed("Server Renamed", f"✅ Server name has been changed to `{name}`.")
        await ctx.send(embed=embed)

    # 20. Server Icon
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def server_icon(self, ctx, url):
        """Change the server's icon."""
        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.read()
                await ctx.guild.edit(icon=data)
                embed = self.create_embed("Server Icon Changed", "✅ Server icon has been updated.")
                await ctx.send(embed=embed)
            else:
                await ctx.send("Invalid URL or failed to fetch the image.")

async def setup(bot):
    await bot.add_cog(Admin(bot))
