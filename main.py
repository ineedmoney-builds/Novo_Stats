import os
import asyncio
import tkinter as tk
from dotenv import load_dotenv
import discord
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot is ready')

async def update_channel_name():
    while True:
        # Fetch supply data from the API
        response = requests.get(
          'https://explorer.novochain.ovh/ext/getmoneysupply')
        data = response.json()

        # Convert the float to an integer and drop decimals
        supply_value = int(data)

        # Update the channel name with the new supply value
        channel = client.get_channel(1092934463190732880)
        try:
            await channel.edit(name="Supply: " + "{:,}".format(supply_value))
        except discord.Forbidden:
            print("Error updating channel name: Missing Permissions")
        except discord.HTTPException as e:
            print(f"Error updating channel name: {e}")

        # Fetch block data from the API
        response1 = requests.get(
          'https://explorer.novochain.ovh/api/getblockcount')
        data = response1.json()

        # Convert the float to an integer and drop decimals
        block_value = int(data)

        # Update the channel name with the new block value
        channel = client.get_channel(1092934657961639987)
        try:
            await channel.edit(name="Current Block: " + "{:,}".format(block_value))
        except discord.Forbidden:
            print("Error updating channel name: Missing Permissions")
        except discord.HTTPException as e:
            print(f"Error updating channel name: {e}")

        # Fetch hashrate data from the API
        response2 = requests.get(
          'https://explorer.novochain.ovh/api/getnetworkhashps')
        data = response2.json()

        # Convert the float to an integer and divide by 1 billion (1000000000)
        hashrate_value = int(float(data) / 1_000_000_000)

        # Update the channel name with the new hashrate value
        channel = client.get_channel(1092934738559377532)
        try:
            await channel.edit(name="Hashrate: " + "{:,}".format(hashrate_value) +
                             " (GH/s)")
        except discord.Forbidden:
            print("Error updating channel name: Missing Permissions")
        except discord.HTTPException as e:
            print(f"Error updating channel name: {e}")

        # Fetch price data from the Exeggex
        url_1 = 'https://xeggex.com/market/NOVO_USDT'
        response = requests.get(url_1)

        soup = BeautifulSoup(response.text, 'html.parser')
        price = soup.find('span', class_='marketlastprice').text

        # Update the channel name with the new price value
        channel = client.get_channel(1092946431041605754)
        try:
             await channel.edit(name="Price: $" + format(price))
        except discord.Forbidden:
            print("Error updating channel name: Missing Permissions")
        except discord.HTTPException as e:
            print(f"Error updating channel name: {e}")

        # Use supply and Price data to update MCAP Channel    
        MCAP1 = supply_value*float(price)
        MCAP = block_value = int(MCAP1)
            
        # Update the channel name with the new MCAP value
        channel = client.get_channel(1092955768443113583)
        try:
            await channel.edit(name="MarketCap: $" + "{:,}".format(MCAP))
        except discord.Forbidden:
            print("Error updating channel name: Missing Permissions")
        except discord.HTTPException as e:
            print(f"Error updating channel name: {e}") 

        # Wait for 300 seconds before updating the channel name again
        await asyncio.sleep(300)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    client.loop.create_task(update_channel_name())

load_dotenv()

client.run(os.getenv('TOKEN'))