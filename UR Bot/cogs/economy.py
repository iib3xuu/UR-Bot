import discord
from discord.ext import commands
from discord import Embed
import json
import random
import os

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = 0x000001  # Hex color for embeds
        self.thumbnail_url = "https://cdn.discordapp.com/avatars/1290541182711103488/b66d2000a0eb1a23021750e89e44a9fe.png"  # Thumbnail URL
        self.data_file = "economy.json"  # Path to economy data file
        self.load_data()

    def create_embed(self, title, description):
        """Utility to create consistent embeds."""
        embed = Embed(title=title, description=description, color=self.embed_color)
        embed.set_thumbnail(url=self.thumbnail_url)
        return embed

    def load_data(self):
        """Load economy data from the JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                self.balance = json.load(file)
        else:
            self.balance = {}

    def save_data(self):
        """Save economy data to the JSON file."""
        with open(self.data_file, "w") as file:
            json.dump(self.balance, file, indent=4)

    def get_balance(self, user_id):
        """Retrieve a user's balance, defaulting to 0."""
        return self.balance.get(str(user_id), 0)

    def update_balance(self, user_id, amount):
        """Update a user's balance."""
        user_id = str(user_id)
        self.balance[user_id] = self.get_balance(user_id) + amount
        self.save_data()

    # 1. Balance Command
    @commands.command()
    async def balance(self, ctx):
        """Check your balance."""
        bal = self.get_balance(ctx.author.id)
        embed = self.create_embed("Balance", f"💰 {ctx.author.mention}, your balance is **{bal} coins**.")
        await ctx.send(embed=embed)

    # 2. Daily Reward
    @commands.command()
    async def daily(self, ctx):
        """Claim your daily reward."""
        reward = random.randint(50, 200)
        self.update_balance(ctx.author.id, reward)
        embed = self.create_embed("Daily Reward", f"🎉 You claimed **{reward} coins** as your daily reward!")
        await ctx.send(embed=embed)

    # 3. Work Command
    @commands.command()
    async def work(self, ctx):
        """Earn coins by working."""
        earnings = random.randint(20, 100)
        self.update_balance(ctx.author.id, earnings)
        embed = self.create_embed("Work", f"💼 You worked hard and earned **{earnings} coins**!")
        await ctx.send(embed=embed)

    # 4. Transfer Coins
    @commands.command()
    async def transfer(self, ctx, member: discord.Member, amount: int):
        """Transfer coins to another user."""
        if amount <= 0:
            await ctx.send("⛔ Transfer amount must be greater than zero.")
            return

        if self.get_balance(ctx.author.id) < amount:
            await ctx.send("⛔ You don't have enough coins to transfer.")
            return

        self.update_balance(ctx.author.id, -amount)
        self.update_balance(member.id, amount)
        embed = self.create_embed(
            "Transfer Successful",
            f"💸 {ctx.author.mention} transferred **{amount} coins** to {member.mention}."
        )
        await ctx.send(embed=embed)

    # 5. Leaderboard
    @commands.command()
    async def leaderboard(self, ctx):
        """Show the top 10 richest users."""
        sorted_balances = sorted(self.balance.items(), key=lambda x: x[1], reverse=True)[:10]
        leaderboard = "\n".join(
            f"{self.bot.get_user(int(user_id)).mention if self.bot.get_user(int(user_id)) else user_id}: {bal} coins"
            for user_id, bal in sorted_balances
        )
        embed = self.create_embed("Leaderboard", leaderboard or "No users found.")
        await ctx.send(embed=embed)

    # 6. Gamble
    @commands.command()
    async def gamble(self, ctx, amount: int):
        """Gamble your coins."""
        if amount <= 0:
            await ctx.send("⛔ You must gamble more than zero coins.")
            return

        if self.get_balance(ctx.author.id) < amount:
            await ctx.send("⛔ You don't have enough coins to gamble.")
            return

        if random.choice([True, False]):  # 50/50 chance
            self.update_balance(ctx.author.id, amount)
            embed = self.create_embed("Gamble", f"🎲 You won and doubled your bet! You gained **{amount} coins**!")
        else:
            self.update_balance(ctx.author.id, -amount)
            embed = self.create_embed("Gamble", f"🎲 You lost **{amount} coins**. Better luck next time!")
        await ctx.send(embed=embed)

    # 7. Rob
    @commands.command()
    async def rob(self, ctx, member: discord.Member):
        """Attempt to rob another user."""
        if ctx.author == member:
            await ctx.send("⛔ You can't rob yourself.")
            return

        if self.get_balance(member.id) < 50:
            await ctx.send("⛔ The target doesn't have enough coins to rob.")
            return

        success = random.choice([True, False])
        if success:
            stolen = random.randint(10, 50)
            self.update_balance(ctx.author.id, stolen)
            self.update_balance(member.id, -stolen)
            embed = self.create_embed("Robbery Successful", f"💰 You robbed {member.mention} and stole **{stolen} coins**!")
        else:
            fine = random.randint(10, 30)
            self.update_balance(ctx.author.id, -fine)
            embed = self.create_embed("Robbery Failed", f"🚓 You got caught! You lost **{fine} coins** as a fine.")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
