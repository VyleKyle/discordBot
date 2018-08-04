import csv
import logging
import time
import asyncio
import youtube_dl

async def init(cli):
    global settings
    settings = {}
    global admins
    admins = {}
    global banned
    banned = {}
    global toDoList
    toDoList = {}
    global client
    client = cli
    global m
    m = None
    global musicPlayers
    servers = []
    for server in client.servers:
        servers.append(server.id)
    musicPlayers = {k:[] for (k) in servers} #Intended format: {'server ID' : [function, ['list', 'of', 'songs']]}
    global logger

    logging.basicConfig(level = logging.INFO)

    logger = logging.getLogger('discord')  # tell the logger to exist and give it an alias

    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    # part of the logger that interacts with files automagically

    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    # I can read and understand this, but I don't understand the syntax in the string

    logger.addHandler(handler)
    return


def keepPlaying(player):
    if player.is_done():
        logger.info("Stopping music.")
        old = musicPlayers[server.id].pop(0)
        old.stop()
        if len(musicPlayers[server.id]) > 0:
            musicPlayers[server.id][0].start()


async def writeSettings():
    for server in client.servers:
        with open("{}.csv".format(server.id), 'w', newline='') as file:
            write = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            write.writerow(settings[server.name])
            write.writerow(admins[server.name])
            write.writerow(banned[server.name])
            write.writerow(toDoList[server.name])


async def permCheck(lvl, m):
    if m.author.id == "176473884919332864": #My uID
        return True
    elif ((m.author.id in admins[m.server.name]) or m.author == m.server.owner) and (lvl == "admins"):
        return True
    elif (m.author.id in banned[m.server.name]):
        await client.send_message(m.channel, "Error: User is banned.")
        return False
    elif lvl != "admins" and lvl != "kyle":
        return True
    else:
        await client.send_message(m.channel, "Error! Insufficient permissions! Command permission level: {}".format(lvl))
        return False

