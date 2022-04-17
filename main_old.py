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
import pyping
#pings the server
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

def ping_mc():
	"""
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
 	"""
    host = "102.135.162.37"
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0


def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
	print(update.effective_chat.id)
	print('/start')

#Deprecated
'''
def initializeTelegram():

  updater = Updater(str(os.getenv('TELEGRAM_API_KEY')), use_context = True)
  dispatcher = updater.dispatcher
  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  start_handler = CommandHandler('start', start)
  txt_handler = MessageHandler()
  dispatcher.add_handler(start_handler)
  return updater
'''
def telegram(text, author):

  #format text to include author name 
	text = text + "\n     - " + str(author)
	token = str("1768484191:AAGDpiqAgiRxny79Di7Qv9m9zJ8UhTgz21Q")
	chat_id = '1452774608'
	url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
	results = requests.get(url_req)
  #print(results.json())



client = discord.Client()

r = asyncpraw.Reddit( #reddit instance
    client_id = "W725iAZ0XOGuf9H4mcXPNw",
    client_secret = "HEv60EHOk6ijX5NXxGzM-zaf09F3dw",
    user_agent = "wagontestbot:example:v0.0"
)

print("Reddit status Read-only? ")
print(r.read_only)
#updater = initializeTelegram()
#updater.start_polling()
#telegram('Hello there!', "None")
print("Telegram initialized!")


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
  	await client.change_presence(activity=discord.Game(name='$help NOW 24/7!!'))


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

  	if message.content.startswith('$text'):
    	if "acmahaja" in str(message.author):
    		await message.channel.send("You aren banned from using this feature :/")    
    	else:
    		text = str(message.content)[6:]
    		telegram(text, message.author)
    		await message.channel.send("Texted Snehin (Telegram): \n" + text + "\n     - " + str(message.author))
    
  	if message.content.startswith('$wagon'):
    	await message.channel.send("Imagine Wagin' deez nuts :KEKW:  \n https://imgur.com/gallery/kehYigq")
  	if message.content.startswith('$ping'):
    	result = ping_mc()
    	if result:
        	await message.channel.send("Inverse SMP Creative is running on 102.135.162.37:25565")
    	else:
        	await message.channel.send("Error! notifying the analog wagon!")
        	msg = "Something is wrong with the server!"
        	telegram(msg, "Ping Error")
        	await message.channel.send("Texted Snehin (Telegram): \n" + msg + "\n     -  Ping Error!")
  	if message.content.startswith('$r'):
    
    	subreddit = str(message.content)[3:]
    	title, url = await redditMeme(subreddit)
    	await message.channel.send(title + "\n" + url)

    

  	if message.content.startswith('$help'):
    	instructions = ['Funtions:', 
    	'1. $wagon - Provides a story on the origin of Imagine Wagon and the mission of Auto Wagon *RECOMMENDED*!',
    	'2. $mc - sends a Minecraft Meme',
    	'3. $chess - sends a Chess Meme',
    	'4. $amogus - sends an amogus',
    	'5. $text <message> - sends Snehin a text message on Telegram **NEW**',
    	"6. $r <subreddit> - sends a meme from a specified subreddit (pls don't try break it) **NEW** \n  eg. $r memes - sends a random meme from r/memes"]
    	separator = '\n'

    	await message.channel.send(separator.join(instructions))

keep_alive()
client.run("ODY5MjgzOTIyMzAxODI1MDM1.YP79vQ.x67e3QoLlIxdaCWyghbbKpy_yfg")