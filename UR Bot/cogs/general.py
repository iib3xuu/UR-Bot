from discord.ext import commands
from discord import Embed
import random
import datetime
import asyncio

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_color = 0x000001  # Hex color for all embeds
        self.thumbnail_url = "https://cdn.discordapp.com/avatars/1290541182711103488/b66d2000a0eb1a23021750e89e44a9fe.png"  # Set your bot's thumbnail URL here

    def create_embed(self, title, description):
        """Utility to create consistent embeds."""
        embed = Embed(title=title, description=description, color=self.embed_color)
        embed.set_thumbnail(url=self.thumbnail_url)
        return embed

    # 1. Ping Command
    @commands.command()
    async def ping(self, ctx):
        """Check bot's latency."""
        latency = round(self.bot.latency * 1000)  # Convert to ms
        embed = self.create_embed("Ping!", f"🏓 Pong! Latency: {latency}ms")
        await ctx.send(embed=embed)

    # 2. Server Info
    @commands.command()
    async def serverinfo(self, ctx):
        """Display information about the server."""
        guild = ctx.guild
        embed = self.create_embed(
            "Server Information",
            f"**Name:** {guild.name}\n"
            f"**Members:** {guild.member_count}\n"
            f"**Owner:** {guild.owner}\n"
            f"**Created On:** {guild.created_at.strftime('%Y-%m-%d')}"
        )
        await ctx.send(embed=embed)

    # 3. User Info
    @commands.command()
    async def userinfo(self, ctx, member: commands.MemberConverter = None):
        """Display information about a user."""
        member = member or ctx.author
        embed = self.create_embed(
            "User Information",
            f"**Username:** {member}\n"
            f"**ID:** {member.id}\n"
            f"**Joined On:** {member.joined_at.strftime('%Y-%m-%d')}\n"
            f"**Created On:** {member.created_at.strftime('%Y-%m-%d')}"
        )
        await ctx.send(embed=embed)

    # 4. Roll Dice
    @commands.command()
    async def roll(self, ctx, sides: int = 6):
        """Roll a dice with the specified number of sides."""
        result = random.randint(1, sides)
        embed = self.create_embed("Roll Dice", f"🎲 You rolled a {result} on a {sides}-sided dice.")
        await ctx.send(embed=embed)

    # 5. Flip Coin
    @commands.command()
    async def flip(self, ctx):
        """Flip a coin."""
        result = random.choice(["Heads", "Tails"])
        embed = self.create_embed("Flip Coin", f"🪙 The coin landed on {result}.")
        await ctx.send(embed=embed)

    # 6. Avatar
    @commands.command()
    async def avatar(self, ctx, member: commands.MemberConverter = None):
        """Get a user's avatar."""
        member = member or ctx.author
        embed = self.create_embed("Avatar", f"Here's the avatar for {member.mention}")
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    # 7. Random Fact
    @commands.command()
    async def fact(self, ctx):
        """Send a random fact."""
        facts = [
            "Honey never spoils.",
            "Bananas are berries, but strawberries aren't.",
            "Octopuses have three hearts.",
            "Wombat poop is cube-shaped.",
            "Sharks existed before trees."
        ]
        fact = random.choice(facts)
        embed = self.create_embed("Random Fact", fact)
        await ctx.send(embed=embed)

    # 8. Uptime
    @commands.command()
    async def uptime(self, ctx):
        """Show the bot's uptime."""
        now = datetime.datetime.utcnow()
        delta = now - self.bot.start_time
        embed = self.create_embed("Uptime", f"⏳ The bot has been running for {delta}.")
        await ctx.send(embed=embed)

    # 9. Repeat
    @commands.command()
    async def repeat(self, ctx, *, message: str):
        """Repeat a message."""
        embed = self.create_embed("Repeat", message)
        await ctx.send(embed=embed)

    # 10. Joke
    @commands.command()
    async def joke(self, ctx):
        """Tell a random joke."""
        jokes = [
            "Why don't skeletons fight each other? They don't have the guts.",
            "Why don't programmers like nature? It has too many bugs.",
            "What do you call fake spaghetti? An impasta."
        ]
        joke = random.choice(jokes)
        embed = self.create_embed("Joke", joke)
        await ctx.send(embed=embed)

    # 11. Choose
    @commands.command()
    async def choose(self, ctx, *choices):
        """Randomly choose between options."""
        if not choices:
            await ctx.send("Please provide some options to choose from.")
            return
        choice = random.choice(choices)
        embed = self.create_embed("Choose", f"I choose: {choice}")
        await ctx.send(embed=embed)

    # 12. About Bot
    @commands.command()
    async def about(self, ctx):
        """Display information about the bot."""
        embed = self.create_embed(
            "About This Bot",
            "I'm UR, a helpful bot created by **iib3xu** and I am a fun Discord bot that makes running your server easier. It helps with moderation and has fun games and tools!"
        )
        await ctx.send(embed=embed)

    # 14. Current Time
    @commands.command()
    async def time(self, ctx):
        """Show the current UTC time."""
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        embed = self.create_embed("Current Time", f"The current UTC time is {now}.")
        await ctx.send(embed=embed)

    # 15. Random Number
    @commands.command()
    async def randnum(self, ctx, start: int = 1, end: int = 100):
        """Generate a random number between two numbers."""
        number = random.randint(start, end)
        embed = self.create_embed("Random Number", f"🎲 Your random number is: {number}")
        await ctx.send(embed=embed)

    # 16. Invite
    @commands.command()
    async def invite(self, ctx):
        """Get the bot's invite link."""
        embed = self.create_embed(
            "Invite Me",
            "Click [here](https://discord.com/oauth2/authorize?client_id=1290541182711103488&scope=bot&permissions=8) to invite me!"
        )
        await ctx.send(embed=embed)

    # 17. Say Hello
    @commands.command()
    async def hello(self, ctx):
        """Say hello."""
        embed = self.create_embed("Hello!", "👋 Hi there! Hope you're having a great day!")
        await ctx.send(embed=embed)

    @commands.command()
    async def countdown(self, ctx, seconds: int):
        """Countdown from a specified number of seconds."""
        if seconds <= 0:
            await ctx.send("⛔ Time must be greater than zero!")
            return

        # Initial embed to start the countdown
        embed = self.create_embed(
            "Countdown",
            f"⏳ Countdown: {seconds} seconds remaining..."
        )
        message = await ctx.send(embed=embed)

        # Update the embed every second
        for i in range(seconds, 0, -1):
            embed.description = f"⏳ Countdown: {i} seconds remaining..."
            await message.edit(embed=embed)
            await asyncio.sleep(1)

        # Final embed when the countdown ends
        embed.title = "Countdown Complete"
        embed.description = f"🎉 Time's up! {ctx.author.mention}"
        await message.edit(embed=embed)

    # 19. Member Count
    @commands.command()
    async def membercount(self, ctx):
        """Show the number of members in the server."""
        count = ctx.guild.member_count
        embed = self.create_embed("Member Count", f"👥 This server has {count} members.")
        await ctx.send(embed=embed)

    # 20. Motivation
    @commands.command()
    async def motivate(self, ctx):
        """Send a motivational quote."""
        quotes = [
            "Believe you can and you're halfway there. –Theodore Roosevelt",
            "Don't watch the clock; do what it does. Keep going. –Sam Levenson",
            "Act as if what you do makes a difference. It does. –William James"
        ]
        quote = random.choice(quotes)
        embed = self.create_embed("Motivational Quote", quote)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
