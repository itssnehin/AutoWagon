import discord
from discord.ext import commands
import os
import asyncpraw, random
from keep_alive import keep_alive
from datetime import datetime
import telegram
from telegram.ext import *
import logging
import requests
#pings the server
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from mcstatus import MinecraftServer
from mcrcon import MCRcon

def getBannedList():
    
    file = open("banned.txt", 'r')
    banned = []
    for line in file:
        user = line.rstrip()
        banned.append(user)
    
    file.close()
    print(banned)

    return banned

def sendMCCommand(command):
    mcr = MCRcon("102.135.162.37", "HrvhsN6+")
    mcr.connect()
    resp = mcr.command(command)
    mcr.disconnect()

    return str(resp)

def queryPlayers():
    
    try:
        server = MinecraftServer.lookup("inversesmp.mc-srv.com")
        
        query = server.query()
        return ("The server has the following players online: {0}".format(", ".join(query.players.names)))

    except:
        return "Error Server might be down"    

def checkMCServer():

    try:
        server = MinecraftServer.lookup("inversesmp.mc-srv.com")
        # 'status' is supported by all Minecraft servers that are version 1.7 or higher.
        status = server.status()
        print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))

        # 'ping' is supported by all Minecraft servers that are version 1.7 or higher.
        # It is included in a 'status' call, but is exposed separate if you do not require the additional info.
        latency = server.ping()
        print("The server replied in {0} ms".format(latency))

        # 'query' has to be enabled in a servers' server.properties file.
        # It may give more information than a ping, such as a full player list or mod information.
        #query = server.query()
        #print("The server has the following players online: {0}".format(", ".join(query.players.names)))

        return status
    except:
        return "Error Server might be down"


def telegram(text, author):

  #format text to include author name 
    text = text + "\n     - " + str(author)
    token = str("1768484191:AAGDpiqAgiRxny79Di7Qv9m9zJ8UhTgz21Q")
    chat_id = '1452774608'
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
    results = requests.get(url_req)
  #print(results.json())


###################################################################################################################
client = discord.Client()
r = asyncpraw.Reddit( #reddit instance
    client_id = "W725iAZ0XOGuf9H4mcXPNw",
    client_secret = "HEv60EHOk6ijX5NXxGzM-zaf09F3dw",
    user_agent = "wagontestbot:example:v0.0"
)

print("Reddit status Read-only?")
print(r.read_only)

async def checkAdmin(message):
    admin = discord.utils.find(lambda r: r.name == 'Head Admins', message.guild.roles)
    mod = discord.utils.find(lambda r: r.name == 'Discord Moderators', message.guild.roles)
    print(admin)

    if admin in message.author.roles:
        return True

    if mod in message.author.roles:
        return True
    return False


async def redditMeme(sr):
  
    url = 'https://imgur.com/gallery/kehYigq'
    title = 'Error Idk if this is a subreddit...'
    subreddit = await r.subreddit(sr)
    print(subreddit)
    rng = random.randint(0,49)
    counter = 0

    try:

        async for submission in subreddit.hot(limit=50):
            if counter == rng:
                url = submission.url
                title = submission.title
                return title, url
            else:
                counter += 1
    except:
        url = 'https://imgur.com/gallery/kehYigq'
        title = 'Error Idk if this is a subreddit...'
    
    return title, url

async def mcMeme():
    url = 'Coming soonTM'
    title = 'none'
    subreddit = await r.subreddit('MinecraftMemes')
    rng = random.randint(0,49)
    counter = 0
    async for submission in subreddit.hot(limit=50):
        if counter == rng:
            url = submission.url
            title = submission.title
            return title, url
        else:
            counter += 1
  
    return title, url

async def chessMeme():
    url = "Coming soon!"
    title = "none"
    subreddit = await r.subreddit('AnarchyChess')
    rng = random.randint(0,49)
    counter = 0
    async for submission in subreddit.hot(limit=50):
        if counter == rng:
            url = submission.url
            title = submission.title
            return title, url
        else:
            counter += 1
    return title, url

async def amongUsMeme():
    url = "Coming soon!"
    title = "none"
    subreddit = await r.subreddit('amogus')
    rng = random.randint(0,49)
    counter = 0
    async for submission in subreddit.hot(limit=50):
        if counter == rng:
            url = submission.url
            title = submission.title
            return title, url
        else:
            counter += 1
  
    return title, url

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    await client.change_presence(activity=discord.Game(name='$help or $help-dank'))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
  
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$meme'):
        await message.channel.send("$meme no longer works :sadge: use $help to see a list of functions (that hopefully work)")
    
    if message.content.startswith('$mc'):
        title, url = await mcMeme()
        await message.channel.send(title + "\n" + url)
    
  
    if message.content.startswith('$chess'):
        title, url = await chessMeme()
        await message.channel.send(title + "\n" + url)
    

    if message.content.startswith('$amogus'):
        title, url = await amongUsMeme()
        await message.channel.send(title + "\n" + url)

    if message.content.startswith('$inverse'):
        text = ["The mod has the following effects by default: \n \n", 
        "    * Spawn players in the Nether \n",
        "    * When players are in the Overworld \n",
        "        * Apply Poison I potion effect for 15 seconds to players every 60s they are in the overworld \n",
        "        * Reduce max health from players for evey 10 minutes they are in the overworld \n", 
        "        * Restore max health to the player for each hour they are in the nether or the end. \n",
        "    * Adds an expensive item (Iodised Apple) which allows players to get back max health (see $apple)\n \n", 
        "Made by: PandaMan and gremlite \n \n For more info : <https://github.com/kcranky/inverse-forge>"]

        await message.channel.send("".join(text))

    if message.content.startswith('$apple'):
        text = ["Crafting recipe for the Iodised Apple: \n ",
        "https://imgur.com/a/pNY0ORN"]

        await message.channel.send("".join(text))


    if message.content.startswith('$text'):

        '''
        banned = False
        banned_users = getBannedList()
        for user in banned_users:
            if user in str(message.author):
                banned = True
                await message.channel.send("You are banned from using this feature :/")    
                break
        
        if banned == False:
            text = str(message.content)[6:]
            telegram(text, message.author)
            await message.channel.send("Texted Snehin (Telegram): \n" + text + "\n     - " + str(message.author))
        '''
        await message.channel.send("Feature Removed")
    if message.content.startswith('$wagon'):
        await message.channel.send("Imagine Wagin' deez nuts :KEKW:  \n https://imgur.com/gallery/kehYigq")

    if message.content.startswith('$r '):
    
        subreddit = str(message.content)[3:]
        title, url = await redditMeme(subreddit)
        await message.channel.send(title + "\n" + url)

    if message.content.startswith('$banned'):
        banned_users = getBannedList()
        await message.channel.send("List of banned users: "+ ", ".join(banned_users))

    if message.content.startswith('$ip'):
        await message.channel.send("IP and Port Address: 102.135.162.37:25565 \n or use: inversesmp.mc-srv.com")

    if message.content.startswith('$status'):
        status = checkMCServer()

        if isinstance(status, str):
            await message.channel.send("Error server might be down or I'm bad at python or both")
        else:
            await message.channel.send("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))

    if message.content.startswith('$myrole'):
        print(message.author.roles)
        check_admin = await checkAdmin(message)
        print(check_admin)
        if check_admin:
            await message.channel.send('You are an admin')
        else:
            await message.channel.send("You don't have permission to do that")

    if message.content.startswith('$query'):
        
        '''
        guild_id = "726441148196978758"
        check_admin = False
        if str(message.guild.id) != guild_id:
             await message.channel.send("I can only do this in the InverseSMP Server")
             check_admin = False
        else:     
            check_admin = await checkAdmin(message)
        '''
        check_admin = await checkAdmin(message)
        if check_admin:
            resp = queryPlayers()
            print(resp)
            await message.channel.send("Minecraft: " + resp)

        else:
            await message.channel.send("You don't have permission to do that :/")


    if message.content.startswith('$rcon'):
        
        guild_id = "726441148196978758"
        check_admin = False
        if str(message.guild.id) != guild_id:
             await message.channel.send("I can only do this in the InverseSMP Server")
             check_admin = False
        else:     
            check_admin = await checkAdmin(message)
        
        if check_admin:
            command = str(message.content)[6:]
            resp = sendMCCommand(command)
            await message.channel.send("`Minecraft: " + resp + "`")

        else:
            await message.channel.send("You don't have permission to do that :/")


    if message.content.startswith('$setup'):
        instructions = ['**Setup Guide** \n',
        "Prerequisites - A Copy of Minecraft Java Edition <https://www.minecraft.net/en-us/store/minecraft-java-edition> \n",
        "1. Download Minecraft Fabric Loader here -->   <https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.10.0/fabric-installer-0.10.0.exe>",
        "2. Run the installer, make sure you install the Fabric 0.12.6 client loader (Check if the directory is your /.minecraft folder)",
        "3. Download the required mods here -->  TBD",
        "4. Extract the zip and drop the JAR files in C:/Users/<USER_NAME>/AppData/Roaming/.minecraft/mods",
        "\n For any issues @ a Head Admin"]
        separator = "\n"

        await message.channel.send(separator.join(instructions))

    if message.content.startswith('$voicechat'):
        instructions = ['** Proximity Chat: **\n',
        '* This mod adds a proximity voice chat to your Minecraft server. You can choose between push to talk (PTT) or voice activation. \n',
        '* The default PTT key is `CAPS LOCK`, but it can be changed in the controls. You can access the voice chat settings by pressing the `V` key.\n',
        '* For more info: <https://www.curseforge.com/minecraft/mc-mods/simple-voice-chat/>\n']

        separator = '\n'

        await message.channel.send(separator.join(instructions))

    if message.content == '$help-dank':

        instructions = ['Funtions:', 
        '1. $wagon - Provides a story on the origin of Imagine Wagon and the mission of Auto Wagon **RECOMMENDED!**',
        '2. $mc - sends a Minecraft Meme',
        '3. $chess - sends a Chess Meme',
        '4. $amogus - sends an amogus',
        "5. $r <subreddit> - sends a meme from a specified subreddit (pls don't try break it) \n  eg. $r memes - sends a random meme from r/memes",
        "See $help for Minecraft related functions"]
        separator = '\n'

        await message.channel.send(separator.join(instructions))

    if message.content == '$help':
        instructions = ["Minecraft functions: ",
        "1. $setup - Instructions on how to install the Fabric Loader and the required mods on your PC",
        "2. $voicechat - Explains how the Simple Voice Chat mod works",
        "4. $status - displays the status of the server",
        "5. $ip - displays the IP address and Port of the Minecraft Server"]

        separator = '\n'
        await message.channel.send(separator.join(instructions))

keep_alive()
client.run("<token>")
