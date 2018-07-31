import csv
import discord
import pre

#TODO: Implement a command to ban users from accessing the bot.

commands = {}

async def commander(m, client):
    if m.content[0].lower() in commands:
        commands[m.content[0].lower()](m, client)


async def help(m, client):
    if m.content[0].lower() == 'help':
        if await pre.permCheck('users', m):
            embed = discord.Embed(title='Commands', description='A list of the available commands.', color=0x00ff00)
            for v,k in enumerate(commands):
                print(k)
                embed.add_field(name=k, value=k, inline=True)
            await client.send_message(m.channel, embed=embed)
        return True
commands['help'] = help


async def say(m, client):
    if m.content[0].lower() == 'say':
        if await pre.permCheck('users', m):
            msg = ' '.join(m.content[1:])
            await client.delete_message(m)
            await client.send_message(m.channel, msg)
        return True
commands['say'] = say

async def whoami(m, client):
    if m.content[0].lower() =='whoami':
        if await pre.permCheck('users', m):
            await client.send_message(m.channel, m.author.id)
        return True
commands['whoami'] = whoami


async def listAdmins(m, client):
    if m.content[0].lower() == 'listadmins':
        if await pre.permCheck('admins', m):
            #await client.send_message(m.channel, pre.admins)
            names = []
            for uID in pre.admins[m.server.name][1:]:
                temp = await client.get_user_info(uID) #I wanted to append directly with get user info, but it wouldnt
                #play very nice. So I had to store the object in a variable before getting its name value.
                names.append(temp.name)
            await client.send_message(m.channel, names)
        return True
commands['listadmins'] = listAdmins



async def addAdmin(m, client):
    if m.content[0].lower() == 'addadmin':
        if await pre.permCheck('admins', m):
            try:
                if not m.mentions[0].id in pre.admins[m.server.name]:
                    pre.admins[m.server.name].append(m.mentions[0].id)
                    await client.send_message(m.channel, "Admin authorized.")
                    await pre.writeSettings(client)
                else:
                    await client.send_message(m.channel, "Admin already authorized!")
            except:
                await client.send_message(m.channel, "Something went wrong. Admin not added.")
        return True
commands['addadmin'] = addAdmin


async def removeAdmin(m, client):
    if m.content[0].lower() == 'removeadmin':
        if await pre.permCheck('admins', m):
            try:
                if m.mentions[0].id in pre.admins[m.server.name]:
                    pre.admins[m.server.name].remove(m.mentions[0].id)
                    await client.send_message(m.channel, "Admin priviledges revoked!")
                    pre.writeSettings()
                else:
                    await client.send_message(m.channel, "Member isn't an admin!")
            except:
                await client.send_message(m.channel, "Something went wrong. Admin not removed.")
        return True
commands['removeadmin'] = removeAdmin


async def changePrefix(m, client):
    if m.content[0].lower() == 'changeprefix':
        if not len(m.content) == 2:
            await client.send_message(m.channel, "This command only takes exactly one argument!")
            return True
        if await pre.permCheck('admins', m):
            settings[m.server.name][1] = m.content[1]
            await pre.writeSettings()
            await client.send_message(m.channel, "Done.")
        return True
commands['changeprefix'] = changePrefix


async def listNotes(m, client):
    if m.content[0].lower() == 'listnotes':
        if await pre.permCheck('kyle', m):
            msg = ""
            for index, value in enumerate(pre.toDoList[m.server.name][1:], start=1):
                msg += "{}: {}\n".format(index, value)
            if not msg == None:
                await client.send_message(m.channel, msg)
            else:
                await client.send_message(m.channel, "Sorry, there is no to do list for this server.")
        return True
commands['listnotes'] = listNotes


async def addNote(m, client):
    if m.content[0].lower() == 'addnote':
        if await pre.permCheck('kyle', m):
            pre.toDoList[m.server.name].append(' '.join(m.content[1:]))
            await pre.writeSettings()
            await client.send_message(m.channel, "Added '{}' as a new note.".format(' '.join(m.content[1:])))
        return True
commands['addnote'] = addNote


async def removeNote(m, client):
    if m.content[0].lower() == 'removenote':
        if await pre.permCheck('kyle', m):
            try:
                m.content = int(m.content[1])
                del pre.toDoList[m.server.name][m.content]
                await pre.writeSettings()
                await client.send_message(m.channel, "Done. Congrats on knocking an item off the list!")
            except:
                await client.send_message(m.channel, "An error occurred. Did you use a number?")
        print('Command executed successfuly.')
        return True
commands['removenote'] = removeNote
