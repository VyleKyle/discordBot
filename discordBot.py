#Oofbot v0.6, made by VyleKyle#2754
#I suck at coding. I have no idea what I'm doing.
#I'm just using google and throwing things together.

#I know the commands API exists.
#But where's the fun in that?


#IMPORTS AND VARIABLES

import discord
import csv #used for remembering/changing settings between activations
import time
import sys
import botCmds
from tokens import Tokens
import pre
import sys

client = discord.Client()


prefix = {}



#BOT LOGIC


@client.event
async def on_message(m):
    if pre.logger is not None:
        try:
            if m.author.bot or m.server == None:
                return
            await pre.writeSettings()
            prefix[m.server.name] = pre.settings[m.server.name][1]
            if m.content.startswith(prefix[m.server.name]):
                pre.m = m
                m.content = m.content[len(prefix[m.server.name]):].split(' ') #ex: !!yeet my guy becomes 'yeet', 'my', 'guy'
                pre.logger.info(" Command: {}".format(' '.join(m.content))) #The line below used to be needed, but isn't anymore...???
                #The purpose of this code was to prevent sending text that crashed the bot, text that previously crashed the bot no longer does so
                #don't ask me why.
                # for word in m.content:
                #     try:
                #         print(str(word))
                #     except:
                #         if word.isprintable():
                #             continue
                #         await client.send_message(m.channel, "Sorry, it looks like you used a character I don't recognize.\nKeep in mind, this bot doesn't support emoji in its commands.")
                #         return

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
    else:
        pass


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


@client.event
async def on_ready():
    print('Oofbot online and ready!')
    await pre.init(client)

    #READING SETTINGS

    csvOutput = []


    for server in client.servers:
        pre.logger.info('looking at {}'.format(server.name))
        try:
            with open('{}.csv'.format(server.id), newline='') as file:
                read = csv.reader(file, delimiter=',', quotechar='|')
                for row in read:
                    csvOutput.append(row)
                pre.logger.info("Finished gathering CSV data for {}".format(server.name))
                pre.logger.info(csvOutput)

            pre.settings[server.name] = list(csvOutput[0])
            pre.admins[server.name] = list(csvOutput[1])
            pre.banned[server.name] = list(csvOutput[2])
            pre.toDoList[server.name] = list(csvOutput[3])
            csvOutput = []

            prefix[server.name] = pre.settings[server.name][1]
        except:
            pre.logger.info("Unable to open settings for {}. Writing new settings.\n{}".format(server.name, sys.exc_info()))
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
                pre.logger.info("Finished gathering CSV data...")
                pre.logger.info(csvOutput)

            pre.settings[server.name] = list(csvOutput[0])
            pre.admins[server.name] = list(csvOutput[1])
            pre.banned[server.name] = list(csvOutput[2])
            pre.toDoList[server.name] = list(csvOutput[3])
            csvOutput = []

            prefix[server.name] = pre.settings[server.name][1]
    await pre.writeSettings()
    if len(sys.argv) > 1:
        chanID = client.get_channel(sys.argv[2])
        await client.send_message(chanID, "Reboot successful.")

client.run(Tokens['OofBot'])
