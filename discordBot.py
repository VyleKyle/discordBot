#Oofbot v0.6, made by VyleKyle#2754
#I suck at coding. But I'm not really gonna get better unless I start practicing, now will I?



#IMPORTS AND VARIABLES

import discord
import logging
import csv #used for remembering/changing settings between activations
import time
import sys
import botCmds
from tokens import Tokens #You can get rid of this import if you're using the bot yourself. I haven't included my bot tokens.
import pre



client = discord.Client()


prefix = {}



#SETTING UP THE LOGGER

#TODO Add logging literally everywhere that's relevant to literally anything.

logger = logging.getLogger('discord')

logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#If I'm being brutally honest, I copy/pasted the logger code from online.

logger.addHandler(handler)


#BOT LOGIC


@client.event #I still don't understand this. I think what happens is that discord.Client() is
#running a loop, and when it triggers an event, this code gets run. I should probably research decorators more some time.
async def on_message(m):
    try:
        if m.author.bot:
            return
        prefix[m.server.name] = pre.settings[m.server.name][1]
        if m.content.startswith(prefix[m.server.name]):
            await pre.writeSettings()
            m.content = m.content[len(prefix[m.server.name]):].split(' ') #ex: "!!say i like pie" becomes ['say', 'i', 'like', 'pie']
            logging.info("Recieved command: {}".format(m.content))
            for word in m.content: #This section of code is weird. I was having some issues, but those issues stopped happening???
                try: #The test version of the bot has this code commented out and ready if needed
                    print(str(word)) #The purpose it served was to prevent emoji and weird ascii characters from crashing the bot.
                except: #But I commented out this code once just to see what'd happen, and it could handle anything I threw at it.
                    if word.isprintable(): #The only exception being if you changePrefix into some weird unicode. That's where it draws the line.
                        continue
                    await client.send_message(m.channel, "Sorry, it looks like you used a character I don't recognize.\nKeep in mind, this bot doesn't support emoji in its commands.")
                    return

            if m.content[0].lower() in botCmds.commands:
                try: #Forcing it to lower because not everybody likes capitalizing it the way I do.
                    await botCmds.commands[m.content[0].lower()](m, client)
                except:
                    await client.send_message(m.channel, "Something about that nearly crashed me! That stuff's lethal, y'know!\nError: {}".format(sys.exc_info()))
            else:
                await client.send_message(m.channel, "Sorry, I didn't recognize that command.")
    except:
        await client.send_message(m.channel, "MAYDAY, MAYDAY, THE BOT IS GOING DOWN! I REPEAT, THE BOT IS GOING DOWN!\nGuilty command: {}\nError message: {}".format(m.content, sys.exc_info()))
        await client.logout()


@client.event
async def on_server_join(server):
    lowest = 9999
    default = None
    for channel in server.channels:
        try:
            int(channel.type)
        except:
            if channel.type == discord.enums.ChannelType.text:
                if channel.permissions_for(channel.server.me).send_messages:
                    if channel.position < lowest:
                        lowest = channel.position
                        default = channel
    try:
        await client.send_message(server.default_channel().id, "I exist now! Thank you!\nFor any assistance, please contact VyleKyle#2754\nI recommend you configure the prefix with changePrefix.\nMy default prefix is !!\n ex. `!!say Do the thing!`")
        logger.info("Default channel found.")
    except:
        try:
            logger.info("No default channel found, going with top-most channel available.")
            await client.send_message(default, "I exist now! Thank you!\nFor any assistance, please contact VyleKyle#2754\nI recommend you configure the prefix with changePrefix.\nMy default prefix is !!\n ex. `!!say Do the thing!`")
        except:
            logger.warn("I just joined {} but I wasn't able to send my greeting!\n{}".format(server.name, sys.exc_info()))


@client.event #If I'm right about the other decorator, then I'm still confused about this one.
#How does it know where to stop? Are you just supposed to put it above a function and if it
#wants that function it calls it, otherwise it ignores it?
async def on_ready():
    logger.info('Oofbot online and ready!')
    await pre.init(client)
    admins = pre.admins #admins and banned are left over from overhauling the permissions system
    banned = pre.banned
    toDoList = pre.toDoList #TODO: Remove per-server-todolist in favor of a global todolist. I'm the only one who can access it, anyway.
    logger.info("I was born on {}".format(time.asctime(time.localtime())))
    logger.info("Connected to : {}".format([server.name for server in client.servers]))

    #READING SETTINGS

    csvOutput = []


    for server in client.servers:
        try:
            with open('{}.csv'.format(server.id), newline='') as file:
                read = csv.reader(file, delimiter=',', quotechar='|')
                for row in read:
                    csvOutput.append(row)
                logger.info("Finished gathering CSV data for {}".format(server.name))
                logger.info(csvOutput)

            pre.settings[server.name] = list(csvOutput[0])
            pre.admins[server.name] = list(csvOutput[1])
            pre.banned[server.name] = list(csvOutput[2])
            pre.toDoList[server.name] = list(csvOutput[3])
            csvOutput = []

            prefix[server.name] = pre.settings[server.name][1]
        except:
            logger.warn("Unable to open settings for {}. Writing new settings.\n{}".format(server.name, sys.exc_info()))
            with open("{}.csv".format(server.id), 'w', newline='') as file:
                write = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                write.writerow(['SETTINGS','!!'])
                write.writerow(['ADMINS'])
                write.writerow(['BANNED'])
                write.writerow(['TODOLIST'])

            
            with open('{}.csv'.format(server.id), newline='') as file:
                read = csv.reader(file, delimiter=',', quotechar='|')
                for row in read:
                    csvOutput.append(row)
                logger.info("Finished gathering CSV data...")
                logger.info(csvOutput)

            pre.settings[server.name] = list(csvOutput[0])
            pre.admins[server.name] = list(csvOutput[1])
            pre.banned[server.name] = list(csvOutput[2])
            pre.toDoList[server.name] = list(csvOutput[3])
            csvOutput = []

            prefix[server.name] = pre.settings[server.name][1]
    await pre.writeSettings()

client.run(Tokens['OofBot']) #You can replace Tokens[] with your own token
