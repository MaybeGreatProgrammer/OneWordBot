import asyncio
import os
import re

import discord
from discord.ext.commands import Bot

TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXX'

client = Bot(command_prefix="!")

if not os.path.isfile("BannedWords.txt"):
    word_file = open("BannedWords.txt", "w+")
    word_file.write("ban")
    word_file.close()
word_file = open("BannedWords.txt")
with word_file as f:
    lines = f.read().splitlines()
    for line in lines:
        if not line or line == " " or line == "\n":
            lines.remove(line)
    print(str(lines))
word_file.close()


def get_regexp():
    matchword = ""
    for word in lines:
        if not matchword:
            matchword += word
        else:
            matchword += ("|" + word)
    regexp = r'\b(' + matchword + r')\b'
    regexp = regexp.replace("[", "\\[")
    regexp = regexp.replace("]", "\\]")
    return regexp


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="with words"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    full_functionality = (message.server.name == "One Word Ban")
    if message.author == client.user:
        return
    if full_functionality:
        regexp = get_regexp()
        if re.search(regexp, message.content, re.IGNORECASE) and lines:
            if message.content.startswith("!ubw") or message.content.startswith("!bw"):
                pass
            else:
                print(regexp + "   " + str(message.author))
                if "exempt" not in [y.name.lower() for y in
                                    message.author.roles] and not message.author == message.server.owner:
                    await client.add_reaction(message, "🚫")
                    await client.send_message(message.channel,
                                              "🚫" + message.author.mention + " will be banned for a message in 11 seconds!")
                    await asyncio.sleep(11)
                    ghost_role = discord.utils.get(message.server.roles, name="Ghost")
                    await client.add_roles(message.author, ghost_role)
                    await client.send_message(message.channel,
                                              "🚫" + message.author.mention + " has been banned for a message!")
                else:
                    await client.add_reaction(message, "✖")
        if message.content == "!bw" or message.content == "!bw " or message.content == "!ubw" or message.content == "!ubw ":
            await client.add_reaction(message, "❌")
            await client.send_message(message.channel, "❌Command must have argument [word]")
        else:
            await client.process_commands(message)
    else:
        regexp = get_regexp()
        if re.search(regexp, message.content, re.IGNORECASE) and lines:
            await client.add_reaction(message, "✖")
    return


@client.event
async def on_message_edit(old_msg, new_msg):
    full_functionality = (new_msg.server.name == "One Word Ban")
    if full_functionality:
        if not old_msg.content == new_msg.content:
            regexp = get_regexp()
            if re.search(regexp, new_msg.content, re.IGNORECASE) and lines:
                if new_msg.content.startswith("!ubw") or new_msg.content.startswith("!bw"):
                    pass
                else:
                    print(regexp + "   " + str(new_msg.author))
                    if "exempt" not in [y.name.lower() for y in
                                        new_msg.author.roles] and not new_msg.author == new_msg.server.owner:
                        await client.add_reaction(new_msg, "🚫")
                        await client.send_message(new_msg.channel,
                                                  "🚫" + new_msg.author.mention + " will be banned for an edit in 11 seconds!")
                        await asyncio.sleep(11)
                        ghost_role = discord.utils.get(new_msg.server.roles, name="Ghost")
                        await client.add_roles(new_msg.author, ghost_role)
                        await client.send_message(new_msg.channel,
                                                  "🚫" + new_msg.author.mention + " has been banned for an edit!")
                    else:
                        await client.add_reaction(new_msg, "✖")
    else:
        if not old_msg.content == new_msg.content:
            regexp = get_regexp()
            if re.search(regexp, new_msg.content, re.IGNORECASE) and lines:
                await client.add_reaction(new_msg, "✖")

    return


@client.event
async def on_member_join(member):
    full_functionality = (member.server.name == "One Word Ban")
    if full_functionality:
        channel = discord.utils.get(client.get_all_channels(), name='💬owb-general')
        await client.send_message(channel, "👋Welcome " + member.mention + "! Don't get banned!")
    return


@client.event
async def on_member_remove(member):
    full_functionality = (member.server.name == "One Word Ban")
    if full_functionality:
        if "ghost" in [y.name.lower() for y in member.roles] and not member == member.server.owner:
            await client.ban(member, 0)


@client.command(pass_context=True)
async def bw(ctx, *argv):
    word = ""
    for arg in argv:
        if word:
            word += " " + arg
        else:
            word += arg
    msg = ctx.message
    if "wordmaster" in [y.name.lower() for y in msg.author.roles] or msg.author == msg.server.owner:
        w_file = open("BannedWords.txt", "a+")
        w_file.write("\n" + word)
        w_file.close()
        lines.append(word)
        await client.say("✅The word " + word + " is now banned")
        await client.add_reaction(msg, "✅")
    else:
        await client.say("❌You are not authorized to use that command")
        await client.add_reaction(msg, "❌")
    return


@client.command(pass_context=True)
async def ubw(ctx, *argv):
    word = ""
    for arg in argv:
        if word:
            word += " " + arg
        else:
            word += arg
    msg = ctx.message
    if "wordmaster" in [y.name.lower() for y in msg.author.roles] or msg.author == msg.server.owner:
        if lines.__contains__(word):
            w_file = open("BannedWords.txt", "r")
            wlines = w_file.readlines()
            w_file.close()
            w_file = open("BannedWords.txt", "w")
            for wline in wlines:
                if wline != word + "\n" and wline != word and wline != " " and wline:
                    w_file.write(wline)
            w_file.close()
            while lines.__contains__(word):
                lines.remove(word)
            await client.say("✅The word " + word + " is now unbanned")
            await client.add_reaction(msg, "✅")
        else:
            await client.say("❌The word " + word + " was not banned in the first place")
            await client.add_reaction(msg, "❌")
    else:
        await client.say("❌You are not authorized to use that command")
        await client.add_reaction(msg, "❌")
    return


# @client.command(pass_context=True)
# async def listwords(ctx):
#    msg = ctx.message
#    if "wordmaster" in [y.name.lower() for y in msg.author.roles] or msg.author == msg.server.owner:
#        word_text_list = ""
#        for word in lines:
#            word_text_list += word + "\n"
#        await client.say("Banned words: \n" + word_text_list)
#        await client.add_reaction(msg, "✅")
#    else:
#        await client.say("❌You are not authorized to use that command")
#        await client.add_reaction(msg, "❌")
#    return


@client.command(pass_context=True)
async def takeout(ctx):
    msg = ctx.message
    if "wordmaster" in [y.name.lower() for y in msg.author.roles] or msg.author == msg.server.owner:
        await client.send_file(msg.channel, "BannedWords.txt")
    else:
        await client.say("❌You are not authorized to use that command")
        await client.add_reaction(msg, "❌")
    return


@client.command(pass_context=True)
async def ping(ctx):
    msg = ctx.message
    await client.say("Pong!")
    await client.add_reaction(msg, "✅")
    return


@client.command(pass_context=True)
async def pong(ctx):
    msg = ctx.message
    await client.say("Ping!")
    await client.add_reaction(msg, "✅")
    return


@client.command(pass_context=True)
async def say(ctx, channel, *argv):
    msg = ctx.message
    if "wordmaster" in [y.name.lower() for y in msg.author.roles] or msg.author == msg.server.owner:
        sentence = ""
        for arg in argv:
            if sentence:
                sentence += " " + arg
            else:
                sentence += arg
        send_channel = discord.utils.get(client.get_all_channels(), name=channel)
        await client.send_message(send_channel, sentence)
        await client.add_reaction(msg, "✅")
        return


client.run(TOKEN)
