import csv

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
    return

async def writeSettings():
    for server in client.servers:
        with open("{}.csv".format(server.id), 'w', newline='') as file:
            write = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            write.writerow(settings[server.name])
            write.writerow(admins[server.name])
            write.writerow(banned[server.name])
            write.writerow(toDoList[server.name])


async def permCheck(lvl, m):
    if m.author.id == "176473884919332864": #My uID. You should probably replace it with your own. You can easily find it with the bot's "whoami" command.
        return True
    elif (m.author.id in admins[m.server.name]) and (lvl == "admins"):
        return True
    elif (m.author.id in banned[m.server.name]):
        await client.send_message(m.channel, "Error: User is banned.")
        return False
    elif lvl != "admins" and lvl != "kyle":
        return True
    else:
        await client.send_message(m.channel, "Error! Insufficient permissions! Command permission level: {}".format(lvl))
        return False



