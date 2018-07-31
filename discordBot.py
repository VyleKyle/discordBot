#Oofbot v0.7, made by VyleKyle#2754




#IMPORTS AND VARIABLES

import discord
import logging
import csv #used for remembering/changing settings between activations
import time
import sys
import botCmds
from tokens import Tokens
import pre



client = discord.Client()


prefix = {}



#SETTING UP THE LOGGER

#TODO Add logging literally everywhere.

logger = logging.getLogger('discord') #tell the logger to exist and give it an alias

logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#part of the logger that interacts with files automagically

handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#I can read and understand this, but I don't understand the syntax

logger.addHandler(handler)


#BOT LOGIC


@client.event #I still don't understand this. I think what happens is that discord.Client() is
#passively running, and when it triggers an event, this code gets run.
async def on_message(m):
    try:
        if m.author.bot:
            return
        await pre.writeSettings()
        prefix[m.server.name] = pre.settings[m.server.name][1]
        if m.content.startswith(prefix[m.server.name]):
            m.content = m.content[len(prefix[m.server.name]):].split(' ')
            logging.info("Recieved command: {}".format(m.content))
            for word in m.content:
                try:
                    print(str(word))
                except:
                    if word.isprintable():
                        continue
                    await client.send_message(m.channel, "Sorry, it looks like you used a character I don't recognize.\nKeep in mind, this bot doesn't support emoji in its commands.")
                    return

            if m.content[0].lower() in botCmds.commands:
                try:
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
    print(client.user.name)
    for channel in server.channels:
        print(channel)
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
        print("Default channel found.")
    except:
        try:
            print("No default channel found, going with top-most channel available.")
            await client.send_message(default, "I exist now! Thank you!\nFor any assistance, please contact VyleKyle#2754\nI recommend you configure the prefix with changePrefix.\nMy default prefix is !!\n ex. `!!say Do the thing!`")
        except:
            print("I just joined {} but I wasn't able to send my greeting!\n{}".format(server.name, sys.exc_info()))


@client.event #If I'm right about the other @ symbol, then I'm still confused about this one.
#How does it know where to stop? Are you just supposed to put it above a function and if it
#wants that function it calls it, otherwise it ignores it?
async def on_ready():
    print('Oofbot online and ready!')
    await pre.init(client)
    admins = pre.admins
    banned = pre.banned
    toDoList = pre.toDoList
    logger.log(logging.INFO, "I EXIST NOW!")
    logger.log(logging.INFO, "I was born on {}".format(time.asctime(time.localtime())))
    logger.log(logging.INFO, "Connected to : {}".format([x.name for x in client.servers]))

    #READING SETTINGS

    csvOutput = []


    for server in client.servers:
        try:
            with open('{}.csv'.format(server.id), newline='') as file:
                read = csv.reader(file, delimiter=',', quotechar='|')
                for row in read:
                    csvOutput.append(row)
                logging.info("Finished gathering CSV data for {}".format(server.name))
                logging.info(csvOutput)

            pre.settings[server.name] = list(csvOutput[0])
            pre.admins[server.name] = list(csvOutput[1])
            pre.banned[server.name] = list(csvOutput[2])
            pre.toDoList[server.name] = list(csvOutput[3])
            csvOutput = []

            prefix[server.name] = pre.settings[server.name][1]
        except:
            print("Unable to open settings for {}. Writing new settings.\n{}".format(server.name, sys.exc_info()))
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
                logging.info(logging.INFO, "Finished gathering CSV data...")
                logging.log(logging.INFO, csvOutput)

            pre.settings[server.name] = list(csvOutput[0])
            pre.admins[server.name] = list(csvOutput[1])
            pre.banned[server.name] = list(csvOutput[2])
            pre.toDoList[server.name] = list(csvOutput[3])
            csvOutput = []

            prefix[server.name] = pre.settings[server.name][1]
    await pre.writeSettings()

client.run(Tokens['OofBot'])
