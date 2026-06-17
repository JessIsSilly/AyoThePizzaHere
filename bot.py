import discord
from discord.ext import commands
import datetime
import pizzintApi as pizzInt
import config

token = config.token

if token == "insert token for bot here":
    print("Token is NOT set! Please try again with the correct bot token!")
    exit(1)

intents = discord.Intents.default()

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

doughconOneIconUrl = config.dcOne
doughconTwoIconUrl = config.dcTwo
doughconThreeIconUrl = config.dcThree
doughconFourIconUrl = config.dcFour
doughconFiveIconUrl = config.dcFive

@bot.tree.command(name="pizzacheck", description="Check the pizza levels for the pentagon")
async def pizzaCheck(interaction: discord.Interaction):
    returnImageUrl = None
    doughconLevel = pizzInt.getDoughconLevel()
    spikingPizzaPlaceInfo = None
    colourForEmbed = 0x04c164

    numOfSpikingPizzaPlaces = pizzInt.getActiveSpikingPizzaPlaces()

    match doughconLevel:
        case 1:
            returnImageUrl = doughconOneIconUrl
            colourForEmbed = 0xfc6366
        case 2:
            returnImageUrl = doughconTwoIconUrl
            colourForEmbed = 0xf58305
        case 3:
            returnImageUrl = doughconThreeIconUrl
            colourForEmbed = 0xfcc700
        case 4:
            returnImageUrl = doughconFourIconUrl
            colourForEmbed = 0x4993e9
        case 5:
            returnImageUrl = doughconFiveIconUrl
            colourForEmbed = 0x04c164

    if not numOfSpikingPizzaPlaces == 0:
        for pizzaPlace in numOfSpikingPizzaPlaces:
            if len(spikingPizzaPlaceInfo) == 0:
                spikingPizzaPlaceInfo = f"{pizzaPlace.split(":")[0].split(": current_popularity")[0]}, popularity: {pizzaPlace.split("current_popularity=")[1].split(",")[0]}, importance: {pizzaPlace.split("magnitude=")[1].split("'")[0]}\n"
            else:
                spikingPizzaPlaceInfo = spikingPizzaPlaceInfo + f"{pizzaPlace.split(":")[0].split(": current_popularity")[0]}, popularity: {pizzaPlace.split("current_popularity=")[1].split(",")[0]}, importance: {pizzaPlace.split("magnitude=")[1].split("'")[0]}\n"
    else:
        spikingPizzaPlaceInfo = "No spiking pizza places"

    embed = discord.Embed(title="Doughcon",
                          description=f"Doughcon level: ***{doughconLevel}***\nSpiking Pizza Places: \n{spikingPizzaPlaceInfo}",
                          colour=colourForEmbed,
                          timestamp=datetime.datetime.now())

    embed.set_author(name="PizzInt (Pentagon)",
                     url="https://www.pizzint.watch/")

    embed.set_thumbnail(
        url=returnImageUrl)

    embed.set_footer(text="Powered by PizzInt")

    await interaction.response.send_message(embed=embed, ephemeral=False)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()

        print(f"Synced {len(synced)} commands")

    except Exception as e:
        print(f"Sync Error: {e}")

bot.run(token)