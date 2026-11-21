import discord
from discord import app_commands
from discord.ext import commands
import requests
import random
import time
import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

with (ROOT / "settings.json").open(encoding="utf-8") as settings_file:
    settings = json.load(settings_file)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix = "/", intents = intents)

guild_id = settings["guild_id"]
rarity_roles = settings["rarity_roles"]
bloxlink_api = f"https://api.blox.link/v4/public/guilds/{guild_id}/discord-to-roblox/USERID"
bloxlink_headers = {"Authorization": os.environ["BLOXLINK_API_KEY"]}
webhook_api = os.getenv("DISCORD_WEBHOOK_URL")
roblox_api = f"https://inventory.roblox.com/v1/users/ROBLOXID/items/GamePass/{settings['gamepass_id']}"

rarities = {
    "Snow": [
        ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
        ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
        ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
        ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
        ["Snow", rarity_roles["Snow"],  1.8*200000/10000000, "1 in 50"],
        ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
        ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
        ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
        ["Auris", rarity_roles["Auris"], 1.8*20000/10000000, "1 in 500"],
        ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
        ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
        ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
        ["Destroyer", rarity_roles["Destroyer"], 1.8*2000/10000000, "1 in 5,000"],
        ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
        ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
        ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
        ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
        ["Hazardous", rarity_roles["Hazardous"], 1.8*200/10000000, "1 in 50,000"],
        ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
        ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
        ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
        ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
        ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
        ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
        ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
        ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
        ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"]
    ],
    "Rainy Snow": [
        ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
        ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
        ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
        ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
        ["Snow", rarity_roles["Snow"],  1.8*200000/10000000, "1 in 50"],
        ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
        ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
        ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
        ["Rainfall", rarity_roles["Rainfall"],  1.8*20000/10000000, "1 in 500"],
        ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
        ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
        ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
        ["Hail", rarity_roles["Hail"],  1.8*2000/10000000, "1 in 5,000"],
        ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
        ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
        ["Blitz", rarity_roles["Blitz"],  1.8*500/10000000, "1 in 20,000"],
        ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
        ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
        ["Hazardous", rarity_roles["Hazardous"], 1.8*200/10000000, "1 in 50,000"],
        ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
        ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
        ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
        ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
        ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
        ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
        ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
        ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
        ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"]
    ],
    "Cloudy Snow": [
        ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
        ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
        ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
        ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
        ["Snow", rarity_roles["Snow"],  1.8*200000/10000000, "1 in 50"],
        ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
        ["Blockage", rarity_roles["Blockage"],  1.8*50000/10000000, "1 in 200"],
        ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
        ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
        ["Auris", rarity_roles["Auris"], 1.8*20000/10000000, "1 in 500"],
        ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
        ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
        ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
        ["Destroyer", rarity_roles["Destroyer"], 1.8*2000/10000000, "1 in 5,000"],
        ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
        ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
        ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
        ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
        ["Hazardous", rarity_roles["Hazardous"], 1.8*200/10000000, "1 in 50,000"],
        ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
        ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
        ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
        ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
        ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
        ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
        ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
        ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
        ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"]
    ],
    "Cloudy": [
        ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
        ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
        ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
        ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
        ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
        ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
        ["Blockage", rarity_roles["Blockage"],  1.8*50000/10000000, "1 in 200"],
        ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
        ["Auris", rarity_roles["Auris"], 1.8*20000/10000000, "1 in 500"],
        ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
        ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
        ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
        ["Destroyer", rarity_roles["Destroyer"], 1.8*2000/10000000, "1 in 5,000"],
        ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
        ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
        ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
        ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
        ["Toxic", rarity_roles["Toxic"], 1.8*200/10000000, "1 in 50,000"],
        ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
        ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
        ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
        ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
        ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
        ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
        ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
        ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
        ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"],
    ],
    "Cloudy Rain": [
        ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
        ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
        ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
        ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
        ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
        ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
        ["Blockage", rarity_roles["Blockage"],  1.8*50000/10000000, "1 in 200"],
        ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
        ["Rainfall", rarity_roles["Rainfall"],  1.8*20000/10000000, "1 in 500"],
        ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
        ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
        ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
        ["Hail", rarity_roles["Hail"],  1.8*2000/10000000, "1 in 5,000"],
        ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
        ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
        ["Blitz", rarity_roles["Blitz"],  1.8*500/10000000, "1 in 20,000"],
        ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
        ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
        ["Toxic", rarity_roles["Toxic"], 1.8*200/10000000, "1 in 50,000"],
        ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
        ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
        ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
        ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
        ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
        ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
        ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
        ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
        ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"]
    ],
    "Rain": [
        ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
        ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
        ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
        ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
        ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
        ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
        ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
        ["Rainfall", rarity_roles["Rainfall"],  1.8*20000/10000000, "1 in 500"],
        ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
        ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
        ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
        ["Hail", rarity_roles["Hail"],  1.8*2000/10000000, "1 in 5,000"],
        ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
        ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
        ["Blitz", rarity_roles["Blitz"],  1.8*500/10000000, "1 in 20,000"],
        ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
        ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
        ["Toxic", rarity_roles["Toxic"], 1.8*200/10000000, "1 in 50,000"],
        ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
        ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
        ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
        ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
        ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
        ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
        ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
        ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
        ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"]
    ],
    "Normal": [
        ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
        ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
        ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
        ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
        ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
        ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
        ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
        ["Auris", rarity_roles["Auris"], 1.8*20000/10000000, "1 in 500"],
        ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
        ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
        ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
        ["Destroyer", rarity_roles["Destroyer"], 1.8*2000/10000000, "1 in 5,000"],
        ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
        ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
        ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
        ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
        ["Toxic", rarity_roles["Toxic"], 1.8*200/10000000, "1 in 50,000"],
        ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
        ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
        ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
        ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
        ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
        ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
        ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
        ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
        ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"]
    ]
}
roblox_users = []
guild = None
prevBiomeEmoji = ""
biome = [0, []]
fat_role = 0
fat_messages = [
    "Yeah you don't have to tell us, it doesn't take much to notice.",
    "Where's your cheeseburger buddy? Oh right, McDonalds are closed today.",
    "They say that weight is just a number, but how can a number morph you into a ball?!",
    "WAS THAT AN EARTHQUAKE?! Oh... It was just you.",
    "Everyone knows already, and no one will say the opposite.",
    "Then why don’t you go to the gym, porky?",
    "You just gained +1000 pounds! Nice going you fat fuck."
]
luck_channels = settings["luck_channel_ids"]
roll_channels = settings["roll_channel_ids"]
staff_chat = None
prev_luck = [0, 0, False, ["-1", 0]]

class LuckView(discord.ui.View):
    def __init__(self):
        super().__init__()
    @discord.ui.button(label = "CLAIM", style = discord.ButtonStyle.green, emoji = "🧪")
    async def CLAIM(self, interaction, button):
        global prev_luck

        user = interaction.user
        message = interaction.message
        if message.id != prev_luck[1] or prev_luck[2]: return
        await message.edit(content = f"🧪 {user.mention} successfully claimed claimed a 20 minute luck potion!", view = None)
        prev_luck[2] = False
        prev_luck[3][0] = str(user.id)
        prev_luck[3][1] = int(time.time()) + 1200
        rarities[str(user.id)] = {
            "Snow": [
                ["Common", rarity_roles["Common"], 3*5000000/10000000, "1 in 2"],
                ["Uncommon", rarity_roles["Uncommon"], 3*2500000/10000000, "1 in 4"],
                ["Rare", rarity_roles["Rare"], 3*1250000/10000000, "1 in 8"],
                ["Epic", rarity_roles["Epic"], 3*310000/10000000, "1 in 32"],
                ["Snow", rarity_roles["Snow"],  3*200000/10000000, "1 in 50"],
                ["Legendary", rarity_roles["Legendary"], 3*80000/10000000, "1 in 125"],
                ["Enraged", rarity_roles["Enraged"], 3*66660/10000000, "1 in 150"],
                ["Flame", rarity_roles["Flame"], 3*28570/10000000, "1 in 350"],
                ["Auris", rarity_roles["Auris"], 3*20000/10000000, "1 in 500"],
                ["Emerald", rarity_roles["Emerald"], 3*13330/10000000, "1 in 750"],
                ["Barrier", rarity_roles["Barrier"], 3*10000/10000000, "1 in 1,000"],
                ["Crown", rarity_roles["Crown"], 3*6660/10000000, "1 in 1,500"],
                ["Destroyer", rarity_roles["Destroyer"], 3*2000/10000000, "1 in 5,000"],
                ["Devilish", rarity_roles["Devilish"], 3*1500/10000000, "1 in 6,666"],
                ["Holy", rarity_roles["Holy"], 3*660/10000000, "1 in 15,000"],
                ["Ink", rarity_roles["Ink"], 3*400/10000000, "1 in 25,000"],
                ["Digitality", rarity_roles["Digitality"], 3*280/10000000, "1 in 35,000"],
                ["Hazardous", rarity_roles["Hazardous"], 3*200/10000000, "1 in 50,000"],
                ["Unknown", rarity_roles["Unknown"], 3*110/10000000, "1 in 99,999"],
                ["Bewitchment", rarity_roles["Bewitchment"], 3*100/10000000, "1 in 100,000"],
                ["Ion", rarity_roles["Ion"], 3*66/10000000, "1 in 150,000"],
                ["Ash", rarity_roles["Ash"], 3*50/10000000, "1 in 200,000"],
                ["Menace", rarity_roles["Menace"], 3*22/10000000, "1 in 450,000"],
                ["Blizzard", rarity_roles["Blizzard"], 3*20/10000000, "1 in 500,000"],
                ["Acidic", rarity_roles["Acidic"], 3*15/10000000, "1 in 650,000"],
                ["Arcane", rarity_roles["Arcane"], 3*12/10000000, "1 in 800,000"],
                ["Telekenesis", rarity_roles["Telekenesis"], 3*10/10000000, "1 in 1,000,000"]
            ],
            "Rainy Snow": [
                ["Common", rarity_roles["Common"], 3*5000000/10000000, "1 in 2"],
                ["Uncommon", rarity_roles["Uncommon"], 3*2500000/10000000, "1 in 4"],
                ["Rare", rarity_roles["Rare"], 3*1250000/10000000, "1 in 8"],
                ["Epic", rarity_roles["Epic"], 3*310000/10000000, "1 in 32"],
                ["Snow", rarity_roles["Snow"],  3*200000/10000000, "1 in 50"],
                ["Legendary", rarity_roles["Legendary"], 3*80000/10000000, "1 in 125"],
                ["Enraged", rarity_roles["Enraged"], 3*66660/10000000, "1 in 150"],
                ["Flame", rarity_roles["Flame"], 3*28570/10000000, "1 in 350"],
                ["Rainfall", rarity_roles["Rainfall"],  3*20000/10000000, "1 in 500"],
                ["Emerald", rarity_roles["Emerald"], 3*13330/10000000, "1 in 750"],
                ["Barrier", rarity_roles["Barrier"], 3*10000/10000000, "1 in 1,000"],
                ["Crown", rarity_roles["Crown"], 3*6660/10000000, "1 in 1,500"],
                ["Hail", rarity_roles["Hail"],  3*2000/10000000, "1 in 5,000"],
                ["Devilish", rarity_roles["Devilish"], 3*1500/10000000, "1 in 6,666"],
                ["Holy", rarity_roles["Holy"], 3*660/10000000, "1 in 15,000"],
                ["Blitz", rarity_roles["Blitz"],  3*500/10000000, "1 in 20,000"],
                ["Ink", rarity_roles["Ink"], 3*400/10000000, "1 in 25,000"],
                ["Digitality", rarity_roles["Digitality"], 3*280/10000000, "1 in 35,000"],
                ["Hazardous", rarity_roles["Hazardous"], 3*200/10000000, "1 in 50,000"],
                ["Unknown", rarity_roles["Unknown"], 3*110/10000000, "1 in 99,999"],
                ["Bewitchment", rarity_roles["Bewitchment"], 3*100/10000000, "1 in 100,000"],
                ["Ion", rarity_roles["Ion"], 3*66/10000000, "1 in 150,000"],
                ["Ash", rarity_roles["Ash"], 3*50/10000000, "1 in 200,000"],
                ["Menace", rarity_roles["Menace"], 3*22/10000000, "1 in 450,000"],
                ["Blizzard", rarity_roles["Blizzard"], 3*20/10000000, "1 in 500,000"],
                ["Acidic", rarity_roles["Acidic"], 3*15/10000000, "1 in 650,000"],
                ["Arcane", rarity_roles["Arcane"], 3*12/10000000, "1 in 800,000"],
                ["Telekenesis", rarity_roles["Telekenesis"], 3*10/10000000, "1 in 1,000,000"]
            ],
            "Cloudy Snow": [
                ["Common", rarity_roles["Common"], 3*5000000/10000000, "1 in 2"],
                ["Uncommon", rarity_roles["Uncommon"], 3*2500000/10000000, "1 in 4"],
                ["Rare", rarity_roles["Rare"], 3*1250000/10000000, "1 in 8"],
                ["Epic", rarity_roles["Epic"], 3*310000/10000000, "1 in 32"],
                ["Snow", rarity_roles["Snow"],  3*200000/10000000, "1 in 50"],
                ["Legendary", rarity_roles["Legendary"], 3*80000/10000000, "1 in 125"],
                ["Blockage", rarity_roles["Blockage"],  3*50000/10000000, "1 in 200"],
                ["Enraged", rarity_roles["Enraged"], 3*66660/10000000, "1 in 150"],
                ["Flame", rarity_roles["Flame"], 3*28570/10000000, "1 in 350"],
                ["Auris", rarity_roles["Auris"], 3*20000/10000000, "1 in 500"],
                ["Emerald", rarity_roles["Emerald"], 3*13330/10000000, "1 in 750"],
                ["Barrier", rarity_roles["Barrier"], 3*10000/10000000, "1 in 1,000"],
                ["Crown", rarity_roles["Crown"], 3*6660/10000000, "1 in 1,500"],
                ["Destroyer", rarity_roles["Destroyer"], 3*2000/10000000, "1 in 5,000"],
                ["Devilish", rarity_roles["Devilish"], 3*1500/10000000, "1 in 6,666"],
                ["Holy", rarity_roles["Holy"], 3*660/10000000, "1 in 15,000"],
                ["Ink", rarity_roles["Ink"], 3*400/10000000, "1 in 25,000"],
                ["Digitality", rarity_roles["Digitality"], 3*280/10000000, "1 in 35,000"],
                ["Hazardous", rarity_roles["Hazardous"], 3*200/10000000, "1 in 50,000"],
                ["Unknown", rarity_roles["Unknown"], 3*110/10000000, "1 in 99,999"],
                ["Bewitchment", rarity_roles["Bewitchment"], 3*100/10000000, "1 in 100,000"],
                ["Ion", rarity_roles["Ion"], 3*66/10000000, "1 in 150,000"],
                ["Ash", rarity_roles["Ash"], 3*50/10000000, "1 in 200,000"],
                ["Menace", rarity_roles["Menace"], 3*22/10000000, "1 in 450,000"],
                ["Blizzard", rarity_roles["Blizzard"], 3*20/10000000, "1 in 500,000"],
                ["Acidic", rarity_roles["Acidic"], 3*15/10000000, "1 in 650,000"],
                ["Arcane", rarity_roles["Arcane"], 3*12/10000000, "1 in 800,000"],
                ["Telekenesis", rarity_roles["Telekenesis"], 3*10/10000000, "1 in 1,000,000"]
            ],
            "Cloudy": [
                ["Common", rarity_roles["Common"], 3*5000000/10000000, "1 in 2"],
                ["Uncommon", rarity_roles["Uncommon"], 3*2500000/10000000, "1 in 4"],
                ["Rare", rarity_roles["Rare"], 3*1250000/10000000, "1 in 8"],
                ["Epic", rarity_roles["Epic"], 3*310000/10000000, "1 in 32"],
                ["Legendary", rarity_roles["Legendary"], 3*80000/10000000, "1 in 125"],
                ["Enraged", rarity_roles["Enraged"], 3*66660/10000000, "1 in 150"],
                ["Blockage", rarity_roles["Blockage"],  3*50000/10000000, "1 in 200"],
                ["Flame", rarity_roles["Flame"], 3*28570/10000000, "1 in 350"],
                ["Auris", rarity_roles["Auris"], 3*20000/10000000, "1 in 500"],
                ["Emerald", rarity_roles["Emerald"], 3*13330/10000000, "1 in 750"],
                ["Barrier", rarity_roles["Barrier"], 3*10000/10000000, "1 in 1,000"],
                ["Crown", rarity_roles["Crown"], 3*6660/10000000, "1 in 1,500"],
                ["Destroyer", rarity_roles["Destroyer"], 3*2000/10000000, "1 in 5,000"],
                ["Devilish", rarity_roles["Devilish"], 3*1500/10000000, "1 in 6,666"],
                ["Holy", rarity_roles["Holy"], 3*660/10000000, "1 in 15,000"],
                ["Ink", rarity_roles["Ink"], 3*400/10000000, "1 in 25,000"],
                ["Digitality", rarity_roles["Digitality"], 3*280/10000000, "1 in 35,000"],
                ["Toxic", rarity_roles["Toxic"], 3*200/10000000, "1 in 50,000"],
                ["Unknown", rarity_roles["Unknown"], 3*110/10000000, "1 in 99,999"],
                ["Bewitchment", rarity_roles["Bewitchment"], 3*100/10000000, "1 in 100,000"],
                ["Ion", rarity_roles["Ion"], 3*66/10000000, "1 in 150,000"],
                ["Ash", rarity_roles["Ash"], 3*50/10000000, "1 in 200,000"],
                ["Menace", rarity_roles["Menace"], 3*22/10000000, "1 in 450,000"],
                ["Blizzard", rarity_roles["Blizzard"], 3*20/10000000, "1 in 500,000"],
                ["Acidic", rarity_roles["Acidic"], 3*15/10000000, "1 in 650,000"],
                ["Arcane", rarity_roles["Arcane"], 3*12/10000000, "1 in 800,000"],
                ["Telekenesis", rarity_roles["Telekenesis"], 3*10/10000000, "1 in 1,000,000"],
            ],
            "Cloudy Rain": [
                ["Common", rarity_roles["Common"], 3*5000000/10000000, "1 in 2"],
                ["Uncommon", rarity_roles["Uncommon"], 3*2500000/10000000, "1 in 4"],
                ["Rare", rarity_roles["Rare"], 3*1250000/10000000, "1 in 8"],
                ["Epic", rarity_roles["Epic"], 3*310000/10000000, "1 in 32"],
                ["Legendary", rarity_roles["Legendary"], 3*80000/10000000, "1 in 125"],
                ["Enraged", rarity_roles["Enraged"], 3*66660/10000000, "1 in 150"],
                ["Blockage", rarity_roles["Blockage"],  3*50000/10000000, "1 in 200"],
                ["Flame", rarity_roles["Flame"], 3*28570/10000000, "1 in 350"],
                ["Rainfall", rarity_roles["Rainfall"],  3*20000/10000000, "1 in 500"],
                ["Emerald", rarity_roles["Emerald"], 3*13330/10000000, "1 in 750"],
                ["Barrier", rarity_roles["Barrier"], 3*10000/10000000, "1 in 1,000"],
                ["Crown", rarity_roles["Crown"], 3*6660/10000000, "1 in 1,500"],
                ["Hail", rarity_roles["Hail"],  3*2000/10000000, "1 in 5,000"],
                ["Devilish", rarity_roles["Devilish"], 3*1500/10000000, "1 in 6,666"],
                ["Holy", rarity_roles["Holy"], 3*660/10000000, "1 in 15,000"],
                ["Blitz", rarity_roles["Blitz"],  3*500/10000000, "1 in 20,000"],
                ["Ink", rarity_roles["Ink"], 3*400/10000000, "1 in 25,000"],
                ["Digitality", rarity_roles["Digitality"], 3*280/10000000, "1 in 35,000"],
                ["Toxic", rarity_roles["Toxic"], 3*200/10000000, "1 in 50,000"],
                ["Unknown", rarity_roles["Unknown"], 3*110/10000000, "1 in 99,999"],
                ["Bewitchment", rarity_roles["Bewitchment"], 3*100/10000000, "1 in 100,000"],
                ["Ion", rarity_roles["Ion"], 3*66/10000000, "1 in 150,000"],
                ["Ash", rarity_roles["Ash"], 3*50/10000000, "1 in 200,000"],
                ["Menace", rarity_roles["Menace"], 3*22/10000000, "1 in 450,000"],
                ["Blizzard", rarity_roles["Blizzard"], 3*20/10000000, "1 in 500,000"],
                ["Acidic", rarity_roles["Acidic"], 3*15/10000000, "1 in 650,000"],
                ["Arcane", rarity_roles["Arcane"], 3*12/10000000, "1 in 800,000"],
                ["Telekenesis", rarity_roles["Telekenesis"], 3*10/10000000, "1 in 1,000,000"]
            ],
            "Rain": [
                ["Common", rarity_roles["Common"], 3*5000000/10000000, "1 in 2"],
                ["Uncommon", rarity_roles["Uncommon"], 3*2500000/10000000, "1 in 4"],
                ["Rare", rarity_roles["Rare"], 3*1250000/10000000, "1 in 8"],
                ["Epic", rarity_roles["Epic"], 3*310000/10000000, "1 in 32"],
                ["Legendary", rarity_roles["Legendary"], 3*80000/10000000, "1 in 125"],
                ["Enraged", rarity_roles["Enraged"], 3*66660/10000000, "1 in 150"],
                ["Flame", rarity_roles["Flame"], 3*28570/10000000, "1 in 350"],
                ["Rainfall", rarity_roles["Rainfall"],  3*20000/10000000, "1 in 500"],
                ["Emerald", rarity_roles["Emerald"], 3*13330/10000000, "1 in 750"],
                ["Barrier", rarity_roles["Barrier"], 3*10000/10000000, "1 in 1,000"],
                ["Crown", rarity_roles["Crown"], 3*6660/10000000, "1 in 1,500"],
                ["Hail", rarity_roles["Hail"],  3*2000/10000000, "1 in 5,000"],
                ["Devilish", rarity_roles["Devilish"], 3*1500/10000000, "1 in 6,666"],
                ["Holy", rarity_roles["Holy"], 3*660/10000000, "1 in 15,000"],
                ["Blitz", rarity_roles["Blitz"],  3*500/10000000, "1 in 20,000"],
                ["Ink", rarity_roles["Ink"], 3*400/10000000, "1 in 25,000"],
                ["Digitality", rarity_roles["Digitality"], 3*280/10000000, "1 in 35,000"],
                ["Toxic", rarity_roles["Toxic"], 3*200/10000000, "1 in 50,000"],
                ["Unknown", rarity_roles["Unknown"], 3*110/10000000, "1 in 99,999"],
                ["Bewitchment", rarity_roles["Bewitchment"], 3*100/10000000, "1 in 100,000"],
                ["Ion", rarity_roles["Ion"], 3*66/10000000, "1 in 150,000"],
                ["Ash", rarity_roles["Ash"], 3*50/10000000, "1 in 200,000"],
                ["Menace", rarity_roles["Menace"], 3*22/10000000, "1 in 450,000"],
                ["Blizzard", rarity_roles["Blizzard"], 3*20/10000000, "1 in 500,000"],
                ["Acidic", rarity_roles["Acidic"], 3*15/10000000, "1 in 650,000"],
                ["Arcane", rarity_roles["Arcane"], 3*12/10000000, "1 in 800,000"],
                ["Telekenesis", rarity_roles["Telekenesis"], 3*10/10000000, "1 in 1,000,000"]
            ],
            "Normal": [
                ["Common", rarity_roles["Common"], 3*5000000/10000000, "1 in 2"],
                ["Uncommon", rarity_roles["Uncommon"], 3*2500000/10000000, "1 in 4"],
                ["Rare", rarity_roles["Rare"], 3*1250000/10000000, "1 in 8"],
                ["Epic", rarity_roles["Epic"], 3*310000/10000000, "1 in 32"],
                ["Legendary", rarity_roles["Legendary"], 3*80000/10000000, "1 in 125"],
                ["Enraged", rarity_roles["Enraged"], 3*66660/10000000, "1 in 150"],
                ["Flame", rarity_roles["Flame"], 3*28570/10000000, "1 in 350"],
                ["Auris", rarity_roles["Auris"], 3*20000/10000000, "1 in 500"],
                ["Emerald", rarity_roles["Emerald"], 3*13330/10000000, "1 in 750"],
                ["Barrier", rarity_roles["Barrier"], 3*10000/10000000, "1 in 1,000"],
                ["Crown", rarity_roles["Crown"], 3*6660/10000000, "1 in 1,500"],
                ["Destroyer", rarity_roles["Destroyer"], 3*2000/10000000, "1 in 5,000"],
                ["Devilish", rarity_roles["Devilish"], 3*1500/10000000, "1 in 6,666"],
                ["Holy", rarity_roles["Holy"], 3*660/10000000, "1 in 15,000"],
                ["Ink", rarity_roles["Ink"], 3*400/10000000, "1 in 25,000"],
                ["Digitality", rarity_roles["Digitality"], 3*280/10000000, "1 in 35,000"],
                ["Toxic", rarity_roles["Toxic"], 3*200/10000000, "1 in 50,000"],
                ["Unknown", rarity_roles["Unknown"], 3*110/10000000, "1 in 99,999"],
                ["Bewitchment", rarity_roles["Bewitchment"], 3*100/10000000, "1 in 100,000"],
                ["Ion", rarity_roles["Ion"], 3*66/10000000, "1 in 150,000"],
                ["Ash", rarity_roles["Ash"], 3*50/10000000, "1 in 200,000"],
                ["Menace", rarity_roles["Menace"], 3*22/10000000, "1 in 450,000"],
                ["Blizzard", rarity_roles["Blizzard"], 3*20/10000000, "1 in 500,000"],
                ["Acidic", rarity_roles["Acidic"], 3*15/10000000, "1 in 650,000"],
                ["Arcane", rarity_roles["Arcane"], 3*12/10000000, "1 in 800,000"],
                ["Telekenesis", rarity_roles["Telekenesis"], 3*10/10000000, "1 in 1,000,000"]
            ]
        }

def anounce(message):
    payload = {"content": message}
    headers = {"Content-Type": 'application/json'}
    response = requests.post(webhook_api, json = payload, headers = headers)

def generate_biome(timeEmoji):
    random_biome_number = random.randint(0, 80)
    if random_biome_number <= 5:
        return ["Snow", f"{timeEmoji}❄️"]
    elif random_biome_number <= 11 and random_biome_number > 5:
        return ["Rain", f"{timeEmoji}🌧️"]
    elif random_biome_number <= 22 and random_biome_number > 11:
        return ["Cloudy", f"{timeEmoji}☁️"]
    elif random_biome_number <= 28 and random_biome_number > 22:
        return ["Cloudy Snow", f"{timeEmoji}☁️❄️"]
    elif random_biome_number <= 34 and random_biome_number > 28:
        return ["Cloudy Rain", f"{timeEmoji}☁️🌧️"]
    elif random_biome_number <= 37 and random_biome_number > 34:
        return ["Rainy Snow", f"{timeEmoji}🌧️❄️"]
    else:
        return ["Normal", timeEmoji]

async def on_connected():
    global guild, biome, fat_role, staff_chat, prevBiomeEmoji

    await bot.tree.sync()
    guild = bot.get_guild(guild_id)
    if guild is None:
        raise RuntimeError("The bot cannot see the guild in settings.json")
    biome[0] = guild.get_channel(settings["biome_channel_id"])
    fat_role = guild.get_role(settings["message_role_id"])
    staff_chat = guild.get_channel(settings["staff_channel_id"])

    await biome[0].edit(name = biome[0].name.replace("\N{SNOWFLAKE}", "").replace("\N{CLOUD WITH RAIN}", "").replace("\N{CLOUD}", ""))

    while True:
        print("test2")
        biomeEmoji = None
        if biome[1] == []:
            biomeEmoji = "🏙️"
            biome_weather = generate_biome(biomeEmoji)
            await staff_chat.send(f"Biome is {biome_weather[0]} {biome_weather[1]}")
            message = await biome[0].send(f"{biome_weather[1]} It's currently a {biome_weather[0]} day!")
            biome = [biome[0], [message, "day", biome_weather]]
        else:
            message = biome[1][0]
            biomeTime = biome[1][1]
            if biomeTime == "day":
                biomeTime = "night"
                biomeEmoji = "🌆"
            else:
                biomeTime = "day"
                biomeEmoji = "🏙️"
            biome_weather = generate_biome(biomeEmoji)
            await staff_chat.send(f"Biome is {biome_weather[0]} {biome_weather[1]}")
            biome = [biome[0], [message, biomeTime, biome_weather]]
            messageContent = f"{biome_weather[1]} It's currently a {biome_weather[0]} {biomeTime}!"
            if message:
                await message.edit(content = messageContent)
            else:
                await biome[0].send(messageContent)

        channel_emoji = ""
        print(list(biome_weather[1]))
        if len(list(biome_weather[1])) == 4 or len(list(biome_weather[1])) == 6:
            channel_emoji = list(biome_weather[1])[2]
        elif len(list(biome_weather[1])) == 2 or len(list(biome_weather[1])) == 5 or len(list(biome_weather[1])) == 3:
            channel_emoji = list(biome_weather[1])[1]
        if prevBiomeEmoji != "":
            await biome[0].edit(name = biome[0].name.replace(prevBiomeEmoji, channel_emoji))
        else:
            await biome[0].edit(name = channel_emoji+biome[0].name)
        prevBiomeEmoji = channel_emoji
        await asyncio.sleep(random.randint(180, 360))

@bot.tree.command(name = "boost", description = "Boost the luck for higher chances.")
@app_commands.default_permissions(administrator = True)
@app_commands.checks.has_permissions(administrator=True)
@app_commands.guild_only()
@app_commands.describe(multiplier = "The boost multiplier, 1x resets to normal.")
async def boost(interaction: discord.Interaction, multiplier: int):
    global rarities

    rarities = {
        "Snow": [
            ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
            ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
            ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
            ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
            ["Snow", rarity_roles["Snow"],  1.8*200000/10000000, "1 in 50"],
            ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
            ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
            ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
            ["Auris", rarity_roles["Auris"], 1.8*20000/10000000, "1 in 500"],
            ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
            ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
            ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
            ["Destroyer", rarity_roles["Destroyer"], 1.8*2000/10000000, "1 in 5,000"],
            ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
            ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
            ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
            ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
            ["Hazardous", rarity_roles["Hazardous"], 1.8*200/10000000, "1 in 50,000"],
            ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
            ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
            ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
            ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
            ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
            ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
            ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
            ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
            ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"]
        ],
        "Rainy Snow": [
            ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
            ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
            ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
            ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
            ["Snow", rarity_roles["Snow"],  1.8*200000/10000000, "1 in 50"],
            ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
            ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
            ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
            ["Rainfall", rarity_roles["Rainfall"],  1.8*20000/10000000, "1 in 500"],
            ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
            ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
            ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
            ["Hail", rarity_roles["Hail"],  1.8*2000/10000000, "1 in 5,000"],
            ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
            ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
            ["Blitz", rarity_roles["Blitz"],  1.8*500/10000000, "1 in 20,000"],
            ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
            ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
            ["Hazardous", rarity_roles["Hazardous"], 1.8*200/10000000, "1 in 50,000"],
            ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
            ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
            ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
            ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
            ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
            ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
            ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
            ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
            ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"]
        ],
        "Cloudy Snow": [
            ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
            ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
            ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
            ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
            ["Snow", rarity_roles["Snow"],  1.8*200000/10000000, "1 in 50"],
            ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
            ["Blockage", rarity_roles["Blockage"],  1.8*50000/10000000, "1 in 200"],
            ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
            ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
            ["Auris", rarity_roles["Auris"], 1.8*20000/10000000, "1 in 500"],
            ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
            ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
            ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
            ["Destroyer", rarity_roles["Destroyer"], 1.8*2000/10000000, "1 in 5,000"],
            ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
            ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
            ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
            ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
            ["Hazardous", rarity_roles["Hazardous"], 1.8*200/10000000, "1 in 50,000"],
            ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
            ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
            ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
            ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
            ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
            ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
            ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
            ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
            ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"]
        ],
        "Cloudy": [
            ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
            ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
            ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
            ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
            ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
            ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
            ["Blockage", rarity_roles["Blockage"],  1.8*50000/10000000, "1 in 200"],
            ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
            ["Auris", rarity_roles["Auris"], 1.8*20000/10000000, "1 in 500"],
            ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
            ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
            ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
            ["Destroyer", rarity_roles["Destroyer"], 1.8*2000/10000000, "1 in 5,000"],
            ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
            ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
            ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
            ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
            ["Toxic", rarity_roles["Toxic"], 1.8*200/10000000, "1 in 50,000"],
            ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
            ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
            ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
            ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
            ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
            ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
            ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
            ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
            ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"],
        ],
        "Cloudy Rain": [
            ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
            ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
            ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
            ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
            ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
            ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
            ["Blockage", rarity_roles["Blockage"],  1.8*50000/10000000, "1 in 200"],
            ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
            ["Rainfall", rarity_roles["Rainfall"],  1.8*20000/10000000, "1 in 500"],
            ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
            ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
            ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
            ["Hail", rarity_roles["Hail"],  1.8*2000/10000000, "1 in 5,000"],
            ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
            ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
            ["Blitz", rarity_roles["Blitz"],  1.8*500/10000000, "1 in 20,000"],
            ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
            ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
            ["Toxic", rarity_roles["Toxic"], 1.8*200/10000000, "1 in 50,000"],
            ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
            ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
            ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
            ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
            ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
            ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
            ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
            ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
            ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"]
        ],
        "Rain": [
            ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
            ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
            ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
            ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
            ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
            ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
            ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
            ["Rainfall", rarity_roles["Rainfall"],  1.8*20000/10000000, "1 in 500"],
            ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
            ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
            ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
            ["Hail", rarity_roles["Hail"],  1.8*2000/10000000, "1 in 5,000"],
            ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
            ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
            ["Blitz", rarity_roles["Blitz"],  1.8*500/10000000, "1 in 20,000"],
            ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
            ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
            ["Toxic", rarity_roles["Toxic"], 1.8*200/10000000, "1 in 50,000"],
            ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
            ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
            ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
            ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
            ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
            ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
            ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
            ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
            ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"]
        ],
        "Normal": [
            ["Common", rarity_roles["Common"], 1.8*5000000/10000000, "1 in 2"],
            ["Uncommon", rarity_roles["Uncommon"], 1.8*2500000/10000000, "1 in 4"],
            ["Rare", rarity_roles["Rare"], 1.8*1250000/10000000, "1 in 8"],
            ["Epic", rarity_roles["Epic"], 1.8*310000/10000000, "1 in 32"],
            ["Legendary", rarity_roles["Legendary"], 1.8*80000/10000000, "1 in 125"],
            ["Enraged", rarity_roles["Enraged"], 1.8*66660/10000000, "1 in 150"],
            ["Flame", rarity_roles["Flame"], 1.8*28570/10000000, "1 in 350"],
            ["Auris", rarity_roles["Auris"], 1.8*20000/10000000, "1 in 500"],
            ["Emerald", rarity_roles["Emerald"], 1.8*13330/10000000, "1 in 750"],
            ["Barrier", rarity_roles["Barrier"], 1.8*10000/10000000, "1 in 1,000"],
            ["Crown", rarity_roles["Crown"], 1.8*6660/10000000, "1 in 1,500"],
            ["Destroyer", rarity_roles["Destroyer"], 1.8*2000/10000000, "1 in 5,000"],
            ["Devilish", rarity_roles["Devilish"], 1.8*1500/10000000, "1 in 6,666"],
            ["Holy", rarity_roles["Holy"], 1.8*660/10000000, "1 in 15,000"],
            ["Ink", rarity_roles["Ink"], 1.8*400/10000000, "1 in 25,000"],
            ["Digitality", rarity_roles["Digitality"], 1.8*280/10000000, "1 in 35,000"],
            ["Toxic", rarity_roles["Toxic"], 1.8*200/10000000, "1 in 50,000"],
            ["Unknown", rarity_roles["Unknown"], 1.8*110/10000000, "1 in 99,999"],
            ["Bewitchment", rarity_roles["Bewitchment"], 1.8*100/10000000, "1 in 100,000"],
            ["Ion", rarity_roles["Ion"], 1.8*66/10000000, "1 in 150,000"],
            ["Ash", rarity_roles["Ash"], 1.8*50/10000000, "1 in 200,000"],
            ["Menace", rarity_roles["Menace"], 1.8*22/10000000, "1 in 450,000"],
            ["Blizzard", rarity_roles["Blizzard"], 1.8*20/10000000, "1 in 500,000"],
            ["Acidic", rarity_roles["Acidic"], 1.8*15/10000000, "1 in 650,000"],
            ["Arcane", rarity_roles["Arcane"], 1.8*12/10000000, "1 in 800,000"],
            ["Telekenesis", rarity_roles["Telekenesis"], 1.8*10/10000000, "1 in 1,000,000"]
        ]
    }
    if multiplier != 1:
        for i, biome in enumerate(rarities):
            for ii, rarity in enumerate(rarities[biome]):
                if ii >= 0 and ii < 5:
                    rarity[2] *= multiplier
                else:
                    rarity[2] *= multiplier*2

    await interaction.response.send_message(f"👍 A luck boost of `{multiplier}x` has been applied.")

weather_task = None

@bot.event
async def on_ready():
    global weather_task
    if weather_task is None or weather_task.done():
        weather_task = asyncio.create_task(on_connected())

@bot.event
async def on_message(message):
    global fat_role, luck_channels, prev_luck

    author = message.author
    guild = message.guild
    channel = message.channel
    if author.bot or guild is None or guild.id != guild_id or not biome[1]:
        return

    if fat_role and message.content.startswith("im fat"):
        fat_roleFound = False
        for role in author.roles:
            if role.id == fat_role.id:
                fat_roleFound = True
                break
        if not fat_roleFound:
            await author.add_roles(fat_role)
        await message.reply(random.choice(fat_messages))

    currentEpoch = int(time.time())
    if currentEpoch > prev_luck[3][1] and prev_luck[3][0] != "-1":
        rarities[prev_luck[3][0]] = None
        prev_luck[3][0] = "-1"
    if currentEpoch > prev_luck[0]:
        print("pass")
        prev_luck[0] = currentEpoch+random.randint(2400, 3600)
        luck_channel = guild.get_channel(random.choice(luck_channels))
        print(luck_channel)
        luck_message = await luck_channel.send("A luck boost has spawned! Claiming first will give you approximately 20 minutes of RNG luck!", view = LuckView())
        prev_luck[1] = luck_message.id
        prev_luck[2] = False
    if channel.id not in roll_channels: return
    eligible = False
    robloxID = None
    for user in roblox_users:
        if user[0] == author.id:
            robloxID = user[1]
    if robloxID == None:
        bloxlink_request = requests.get(bloxlink_api.replace("USERID", str(author.id)), headers = bloxlink_headers)
        if bloxlink_request.status_code == 200 and bloxlink_request.json():
            robloxID = bloxlink_request.json()["robloxID"]
            roblox_users.append([author.id, robloxID])
    if robloxID == None and author.id not in settings["exempt_user_ids"]: return
    userOwnsGamepass = False
    gamepassRole = guild.get_role(settings["gamepass_role_id"])
    roleFound = False
    for role in author.roles:
        if role.id == gamepassRole.id:
            roleFound = True
            break
    if not roleFound and author.id not in settings["exempt_user_ids"]:
        gamepass_request = requests.get(roblox_api.replace("ROBLOXID", str(robloxID)))
        if gamepass_request.status_code == 200 and gamepass_request.json():
            userOwnsGamepass = (gamepass_request.json()["data"] != [])
    if userOwnsGamepass and not roleFound:
        await author.add_roles(gamepassRole)
    rarityNumber = random.randint(1, 10000000)/10000000
    rarity = None
    announcement = False
    ping = False
    if biome[1] == []: return
    biomeTable = rarities[biome[1][2][0]]
    try:
        biomeTable = rarities[str(author.id)][biome[1][2][0]]
    except Exception:
        biomeTable = rarities[biome[1][2][0]]
    for i in range(len(biomeTable)):
        if i != 0:
            if rarityNumber > biomeTable[i][2] and rarityNumber < biomeTable[i-1][2]:
                rarity = biomeTable[i]
                if rarityNumber <= 1.8*1000/10000000:
                    print("good")
                    announcement = True
                elif rarityNumber <= 1.8*110/10000000:
                    ping = True
        else:
            rarity = biomeTable[i]
    if rarity:
        roleExists = False
        rarityRole = None
        for role in author.roles:
            if role.id == rarity[1]:
                rarityRole = role
                roleExists = True
                break
        if not roleExists:
            rarityRole = guild.get_role(rarity[1])
            await author.add_roles(rarityRole)
        await message.reply(f"🥳 You've just unlocked a {rarityRole.mention} rarity.")
        if announcement and ping and webhook_api:
            anounce(f"{author.mention} has achieved a {rarityRole.mention} rarity!")
        elif announcement:
            announcement_channel = guild.get_channel(settings["announcement_channel_id"])
            await announcement_channel.send(f"{author.mention} has achieved a {rarityRole.mention} rarity!")

if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
