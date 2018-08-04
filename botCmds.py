import csv
import discord
from enum import Enum
import pre
import os
import urllib.parse
import urllib.request
import re
import youtube_dl
import datetime

commands = {}
cmdHelp = {}
kyleMsg = 'Sorry, but only VyleKyle#2754 may run this command'

async def help(m, client):
    if m.content[0].lower() == 'help':
        if await pre.permCheck('users', m):
            embed = discord.Embed(title='Commands', description='A list of the available commands.', color=0x00ff00)
            for v,k in enumerate(commands):
                embed.add_field(name=k, value=cmdHelp[k], inline=True)
            await client.send_message(m.channel, embed=embed)
        return True
commands['help'] = help
cmdHelp['help'] = ':thinking: :thinking: :thinking:'

async def say(m, client):
    if m.content[0].lower() == 'say':
        if await pre.permCheck('users', m):
            msg = ' '.join(m.content[1:])
            await client.delete_message(m)
            await client.send_message(m.channel, msg)
        return True
commands['say'] = say
cmdHelp['say'] = 'Repeat after me!'

async def getvid(m, client): #TODO Maybe add list so you can pick from search results?
    query_string = urllib.parse.urlencode({"search_query": ' '.join(m.content[1:])})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    await client.send_message(m.channel, "Found youtube video.\nhttp://www.youtube.com/watch?v={}".format(search_results[0]))
    return "http://www.youtube.com/watch?v=" + search_results[0]

async def joinVoice(m, client):
        if await pre.permCheck('users', m):
            if client.voice_client_in(m.server) == None: #Are we already in a voice channel?
                joined = False
                for channel in m.server.channels:
                    if channel.type == discord.enums.ChannelType.voice and m.author in channel.voice_members:
                        pre.logger.info('Joining a voice channel with a user in it.')
                        await client.join_voice_channel(channel)
                        joined = True
                        break
                    elif channel.name == m.channel.name and channel.type == discord.enums.ChannelType.voice:
                        pre.logger.info('Joining a voice channel based on the name of the channel.')
                        await client.join_voice_channel(channel)
                        joined = True
                        break
                if not joined:
                    await client.send_message(m.channel, "Couldn't find voice channel!")
                    return True
                await client.send_message(m.channel, "Joined voice channel.")
            else:
                await client.send_message(m.channel, "I'm already in a voice channel!")

        return True
commands['join'] = joinVoice
cmdHelp['join'] = "Used to get the bot to join a voice channel."

async def begone(m, client):
    if m.content[0].lower() == 'begone':
        if await pre.permCheck('users', m):
            try:
                voice = client.voice_client_in(m.server)
                await voice.disconnect()
                await client.send_message(m.channel, "Left successfully.")
                try:
                    vc = pre.musicPlayers[m.server.id][0]
                    vc.stop()
                except:
                    pass
                pre.musicPlayers[m.server.id] = []
            except Exception as e:
                await client.send_message(m.channel, "I wasn't able to leave the voice channel! Was I in one to begin with...?")
                pre.logger.info(e)
        return True
commands['begone'] = begone
cmdHelp['begone'] = "Kick the bot out of a voice channel. Because you're a bad person."

"""async def play(m, client):
    if m.content[0].lower() == 'play':
        if await pre.permCheck('users', m):
            try: #TODO Note to self: I've been thinking about it all wrong. musicQueue shouldn't hold strings,
                #according to a video I saw, you should be starting a new player object per each song.
                #the musicQueue should be filled with player objects rather than strings
                #meaning I should also get rid of musicPlayers, seeing as it's no longer needed.
                voiceClient = client.voice_client_in(m.server)
                if len(pre.musicPlayers[m.server.id]) == 0:
                    music = await voiceClient.create_ytdl_player(await getvid(m, client), ytdl_options={"-reconnect" : 1,  "-reconnect_streamed" : 1, "-reconnect_delay_max" : 5}, after=lambda: pre.logger.info('Called after. '))
                    #music = await voiceClient.create_ytdl_player(await getfic(m, client), before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", after=pre.keepPlaying())
                    time.sleep(2)
                    if music.duration < 900:
                        if len(pre.musicPlayers[m.server.id]) == 0:
                            pre.musicPlayers[m.server.id].append(music)
                            music.volume = 0.2
                            music.start()
                    else:
                        await client.send_message(m.channel, "That video's a bit too long. Max is 15 min.")
                        return True
                else:
                    pre.logging.info("It went through all the statements.")
                    pre.musicPlayers[m.server.id].append(await getvid(m, client))
                    pre.logger.info(pre.musicPlayers)
            except Exception as xcpt:
                try:
                    await client.send_message(m.channel, "Nope.avi\n{}\n{}".format(music.error, xcpt))
                except:
                    await client.send_message(m.channel, "Something has gone terribly wrong.\n{}".format(xcpt))
        return True"""
async def play(m, client):
    if m.content[0].lower() == 'play':
        if await pre.permCheck('users', m):
            try:
                voiceClient = client.voice_client_in(m.server)
            except Exception as e:
                await client.send_message(m.channel, "Am I even in a voice channel tho?.\n{}".format(e))
                return True
            music = await voiceClient.create_ytdl_player(await getvid(m, client), after=lambda x: pre.keepPlaying(m.server, x))
            if music.duration < 900:
                pre.musicPlayers[m.server.id].append(music)
                music.volume = 0.2
                if len(pre.musicPlayers[m.server.id]) == 1:
                    pre.logger.info("Starting music.")
                    music.start()
        return True
commands['play'] = play
cmdHelp['play'] = "Tell the bot to play a song! (Must already be in voice channel)"


async def pause(m, client):
    if m.content[0].lower() == 'pause' and await pre.permCheck('users', m) and len(pre.musicPlayers[m.server.id]) > 0:
        player = pre.musicPlayers[m.server.id][0]
        if player.is_playing():
            player.pause()
            await client.send_message(m.channel, "Song paused. Use the resume command when you're ready to keep listening.")
        else:
            await client.send_message(m.channel, "Can't really pause a pause... Did you mean resume?")
    return True
commands['pause'] = pause
cmdHelp['pause'] = "Pause any currently playing song."

async def resume(m, client):
    if m.content[0].lower() == 'resume' and await pre.permCheck('users', m) and len(pre.musicPlayers[m.server.id]) > 0:
        player = pre.musicPlayers[m.server.id][0]
        if not player.is_playing():
            player.resume()
        else:
            await client.send_message(m.channel, "Can't really resume a playing song... Did you mean pause?")
        return True
commands['resume'] = resume
cmdHelp['resume'] = "Continue playing paused music."

async def skip(m, client):
    if m.content[0].lower() == 'skip' and await pre.permCheck('users', m) and len(pre.musicPlayers[m.server.id]) > 0:
        player = pre.musicPlayers[m.server.id].pop(0)
        player.stop()
        if len(pre.musicPlayers[m.server.id]) > 0:
            pre.musicPlayers[m.server.id][0].start()
        await client.send_message(m.channel, "Yeet. May you rest in pieces of oof, {}".format(player.title))
        return True
commands['skip'] = skip
cmdHelp['skip'] = "Skip the currently playing song"

async def songQueue(m, client):
    num = 0
    if m.content[0].lower() == 'songqueue' and await pre.permCheck('users', m) and len(pre.musicPlayers[m.server.id]) > 1:
        embed = discord.Embed(title=pre.musicPlayers[m.server.id][0].title, description='Current song', color=0x00ff00)
        for player in pre.musicPlayers[m.server.id][1:]:
            num += 1
            embed.add_field(name="{}. {}".format(num, player.title), value="({})".format(str(datetime.timedelta(seconds=player.duration))), inline=False)
        await client.send_message(m.channel, embed=embed)
        return True
commands['songqueue'] = songQueue
cmdHelp['songqueue'] = "Show the queue of songs to be played."

async def removeFromQueue(m, client):
    if m.content[0].lower() == 'removefromqueue' and await pre.permCheck('users', m) and len(pre.musicPlayers[m.server.id]) > 1 and int(m.content[1]):
        position = int(m.content[1])
        if position > 0 and position <= len(pre.musicPlayers[m.server.id]):
            player = pre.musicPlayers[m.server.id].pop(position)
            await client.send_message(m.channel, "{} is no longer in the queue.".format(player.title))
        else:
            await client.send_message(m.channel, "No song in that position of the queue!")
        return True
commands['removefromqueue'] = removeFromQueue
cmdHelp['removefromqueue'] = "Remove a song from X position in queue"

async def clearQueue(m, client):
    if await pre.permCheck('users', m) and len(pre.musicPlayers[m.server.id]) > 0:
        pre.musicPlayers[m.server.id] = []
        await client.send_message(m.channel, "Queue cleared. Rest in peace.")
    return True
commands['clearqueue'] = clearQueue
cmdHelp['clearqueue'] = "Completely decimate any song queue currently going on. Because you hate other peoples fun."

async def changeVolume(m, client):
    if m.content[0].lower() == 'changevolume':
        if await pre.permCheck('users', m):
            try:
                if len(pre.musicPlayers[m.server.id]) > 0:
                    player = pre.musicPlayers[m.server.id][0]
                    player.volume = 0.01 * int(m.content[1])
                    await client.send_message(m.channel, "New volume set.")
                else:
                    await client.send_message(m.channel, "Nope.")
            except Exception as e:
                await client.send_message(m.channel, "Invalid argument received.")
                pre.logger.info(e)
        return True
commands['changevolume'] = changeVolume
cmdHelp['changevolume'] = "Change the volume of the music being played."

async def whoami(m, client):
    if m.content[0].lower() == 'whoami':
        if await pre.permCheck('users', m):
            await client.send_message(m.channel, m.author.id)
        return True
commands['whoami'] = whoami
cmdHelp['whoami'] = 'Returns your user ID'

async def whereami(m, client):
    if m.content[0].lower() == 'whereami':
        if await pre.permCheck('users', m):
            await client.send_message(m.channel, m.server.id)
        return True
commands['whereami'] = whereami
cmdHelp['whereami'] = 'Gives you the ID of the server. Mainly for debugging.'

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
cmdHelp['listadmins'] = 'Returns a list of admins'

async def addAdmin(m, client):
    if m.content[0].lower() == 'addadmin':
        if await pre.permCheck('admins', m):
            try:
                if not m.mentions[0].id in pre.admins[m.server.name]:
                    pre.admins[m.server.name].append(m.mentions[0].id)
                    await client.send_message(m.channel, "Admin authorized.")
                    await pre.writeSettings()
                else:
                    await client.send_message(m.channel, "Admin already authorized!")
            except:
                await client.send_message(m.channel, "Something went wrong. Admin not added.")
        return True
commands['addadmin'] = addAdmin
cmdHelp['addadmin'] = 'Add an oofbot admin on this server'

async def removeAdmin(m, client):
    if m.content[0].lower() == 'removeadmin':
        if await pre.permCheck('admins', m):
            try:
                if m.mentions[0].id in pre.admins[m.server.name]:
                    pre.admins[m.server.name].remove(m.mentions[0].id)
                    await client.send_message(m.channel, "Admin priviledges revoked!")
                    await pre.writeSettings()
                else:
                    await client.send_message(m.channel, "Member isn't an admin!")
            except:
                await client.send_message(m.channel, "Something went wrong. Admin not removed.")
        return True
commands['removeadmin'] = removeAdmin
cmdHelp['removeadmin'] = 'Remove an oofbot admin on this server'

async def purge(m, client):
    if m.content[0].lower() == 'purge':
        if await pre.permCheck('admins', m):
            if len(m.content) > 1 and int(m.content[1]):
                msgs = []
                async for x in client.logs_from(m.channel, limit = int(m.content[1])+1):
                    msgs.append(x)

                if len(msgs) <= 100:
                    await client.delete_messages(msgs)
                else:
                    deletion = []
                    for message in msgs:
                        deletion.append(message)
                        if len(deletion) == 100:
                            await client.delete_messages(deletion)
                            print('len of deletion was exactly 100\n{}'.format(len(deletion)))
                    if len(deletion) > 0:
                        await client.delete_messages(deletion)
                        print('Len of deletion was more than zero, but less than 100, deleting {}'.format(len(deletion)))
                await client.send_message(m.channel, "Done. Purged {} messages from this channel.".format(m.content[1]))
            else:
                await client.send_message(m.channel, 'Sorry buddy. Somethin about that just didn\'t work.')
        return True
commands['purge'] = purge
cmdHelp['purge'] = 'Delete X amount of commands.'

async def changePrefix(m, client):
    if m.content[0].lower() == 'changeprefix':
        if not len(m.content) == 2:
            await client.send_message(m.channel, "This command only takes exactly one argument!")
            return True
        if await pre.permCheck('admins', m):
            pre.settings[m.server.name][1] = m.content[1]
            await pre.writeSettings()
            await client.send_message(m.channel, "Done.")
        return True
commands['changeprefix'] = changePrefix
cmdHelp['changeprefix'] = 'Change the prefix used to send commands to the bot.'

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
cmdHelp['listnotes'] = kyleMsg

async def addNote(m, client):
    if m.content[0].lower() == 'addnote':
        if await pre.permCheck('kyle', m):
            pre.toDoList[m.server.name].append(' '.join(m.content[1:]))
            await pre.writeSettings()
            await client.send_message(m.channel, "Added '{}' as a new note.".format(' '.join(m.content[1:])))
        return True
commands['addnote'] = addNote
cmdHelp['addnote'] = kyleMsg

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
cmdHelp['removenote'] = kyleMsg

async def reboot(m, client):
    if m.content[0].lower() == 'reboot':
        if await pre.permCheck('kyle', m):
            await client.send_message(m.channel, 'Attempting a reboot...')
            msg = m.channel.id
            await client.logout()
            pre.logger.info('Logged out.')
            os.system('python discordBot.py reboot {}'.format(msg))
        return True
commands['reboot'] = reboot
cmdHelp['reboot'] = kyleMsg

async def kys(m, client):
    if m.content[0].lower() == 'kys':
        if await pre.permCheck('kyle', m):
            await client.send_message(m.channel, "Jeez, okay, I can see when I'm not wanted anymore...")
            await client.logout()
    return True
commands['kys'] = kys
cmdHelp['kys'] = 'I feel this one deserves explaining. It disables the bot.'