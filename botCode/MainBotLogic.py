########################################
# - - - - - - MEB PRESENTS - - - - - - #
# Name of produce: Room-DiscordBot     #
# Author of the bot: Machnev Egor      #
# Contacts in the network:             #
# --Web-Site > smtechnology.info       #
# --Telegram > @machnev_egor           #
# --VK > https://vk.com/machnev_egor   #
# --Email > meb.official.com@gmail.com #
########################################

# import main modules
import discord as discord
from discord.ext import commands as commands
from configurationFile import BotConfig as BotConfig
from re import sub as StandardizationText
import datetime as datetime
import pickle as pickle
from random import randint as randint

# creating a client for the bot
client = discord.Client()
# prefix for all ctx-commands of the bot
client = commands.Bot(command_prefix=BotConfig.BotPrefixes)
# to use the internal help command
client.remove_command("help")

# timeout to change the settings of the room
room_update_timeout = 5


# working with the database where all the bot markers are stored
def working_with_the_database(registered_channels=None):
    # check for the integrity of the database, try to access the database and get the correct answer
    try:
        pickle.load(open("configurationFile/database.sm", "rb+"))
    # if a database fault is detected, data is reset, and the structure is restored
    except Exception as E:
        pickle.dump(
            dict({60547261464449: dict({60547261464449: [60547261464449, "{/branch/}🚪Room {/counter/}", dict()]})}),
            open("configurationFile/database.sm", "rb+"))
    # uploading updated data to the database if required
    if registered_channels != None:
        pickle.dump(registered_channels, open("configurationFile/database.sm", "rb+"))
    # returning the current stored database
    return pickle.load(open("configurationFile/database.sm", "rb+"))


# connection notification
@client.event
async def on_ready():
    # sending data to the terminal
    print("-----------------------------")
    print("Bot launched into the network")
    print(f"Name in network: {client.user}")
    print(f"ID: {client.user.id}")
    print("-----------------------------")
    # list of all servers that the bot is connected to
    members = "\n".join([f"|♡|➳ {guild.name}" for guild in client.guilds])
    print(f"|♡|All friends of the bot:\n{members}")
    print("-----------------------------")
    # setting the bot's status
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game(f"{BotConfig.BotPrefixes[0]}help"))


# sending all necessary information about the bot to help embed
@client.command(pass_context=True)
async def help(ctx):
    # creating and sending embed
    help_embed = discord.Embed(colour=discord.Color(0x3b1a11), url=BotConfig.BotInvite,
                               title="**Room** - Сlick here to __invite__ to your server😏")
    help_embed.add_field(inline=True, name="List of all current commands:",
                         value=f"┣ **{BotConfig.BotPrefixes[0]}addmarker** - then enter the channel ID and category ID (you must activate _developer mode_)\n┣ **{BotConfig.BotPrefixes[0]}deletemarker** - then enter the channel ID\n┗ **{BotConfig.BotPrefixes[0]}info** - next, you will immediately see all the information about all the markers on your server")
    help_embed.add_field(inline=True, name="Technical support site:",
                         value=f"{BotConfig.BotSite}\n```The ROOM-BOT was developed by MEB from the SM_TECHNOLOGY projects community, enjoy your use👽```")
    help_embed.set_footer(
        text=f"P.S. {['To add a marker, you must have administrator rights', 'To delete a marker, you must have administrator rights', 'To view information about markers, you must have administrator rights', 'To interact with the bot, you must have administrator rights', 'Sometimes dynamic room names may not change immediately, this is due to the Discord timeout (I hope that the allowed frequency of sending requests will increase soon)', 'Thank you for inviting the bot to your server, I am very pleased'][randint(0, 5)]}")
    await ctx.send(embed=help_embed)


# adding a marker on the server using the channel ID and category ID
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def addmarker(ctx, *, args="SM TECHNOLOGY"):
    # sending data to the terminal
    print(datetime.datetime.today())
    print(f"{ctx.guild.name}-->{ctx.author}")
    print(f"Command name: {BotConfig.BotPrefixes[0]}addmarker {list(args.split())}")
    # logic for adding a marker on the server
    try:
        # checking for the number of characters in the passed parameters to add a marker to the server
        if (len(list(args.split())[0]) == 18) and (len(list(args.split())[1]) == 18):
            # correction of the entered data for further work with them and adding them to the server
            marker_id, category_id = int(list(args.split())[0]), int(list(args.split())[1])
            layout_text = "🚪Room{〚/author/〛}"
            if len(list(args.split())) > 2:
                layout_text = " ".join(args.split()[2:])
            # adding a marker if this is the first channel on the server
            if ctx.guild.id not in list(working_with_the_database().keys()):
                # uploading new data to the database
                updated_database = working_with_the_database()
                updated_database.update(dict({ctx.guild.id: dict({marker_id: [category_id, layout_text, dict()]})}))
                working_with_the_database(registered_channels=updated_database)
                # creating and forming an embed structure
                add_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                          title="**Room** - Your first marker on this server was created __successfully__🥳")
            # changing the marker if the channel already exists
            elif marker_id in list(working_with_the_database()[ctx.guild.id].keys()):
                # uploading new data to the database
                updated_database = working_with_the_database()
                updated_database[ctx.guild.id][marker_id] = [category_id, layout_text,
                                                             updated_database[ctx.guild.id][marker_id][2]]
                working_with_the_database(registered_channels=updated_database)
                # creating and forming an embed structure
                add_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                          title="**Room** - The marker was __successfully modified__✍")
            # adding a marker if there are already added channels on the server
            elif list(working_with_the_database().keys()) != []:
                # uploading new data to the database
                updated_database = working_with_the_database()
                updated_database[ctx.guild.id].update(dict({marker_id: [category_id, layout_text, dict()]}))
                working_with_the_database(registered_channels=updated_database)
                # creating and forming an embed structure
                add_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                          title="**Room** - Your additional marker was created __successfully__👌")
            # adding informative data and sending embed
            add_embed.add_field(inline=True, name="Marker ID:", value=f"{marker_id}")
            add_embed.add_field(inline=True, name="Category ID:", value=f"{category_id}")
            add_embed.add_field(inline=True, name="Standard name:", value=f"{layout_text}")
            await ctx.send(embed=add_embed)
            # sending data to the terminal
            print(f"Added/changed marker: {marker_id}-->{category_id}-->{layout_text}")
        # warnings about incorrect data
        else:
            # creating and sending embed
            error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                        title="**Room** - Oops, I think you're __typing__ something __wrong__😜")
            error_embed.add_field(inline=True, name="Example of a simple marker addition:",
                                  value=f"```{BotConfig.BotPrefixes[0]}addmarker {randint(10 ** (18 - 1), 10 ** 18 - 1)} {randint(10 ** (18 - 1), 10 ** 18 - 1)}```")
            error_embed.add_field(inline=True, name="Additional parameter for room names:",
                                  value="┗ **{/author/}** - parameter for displaying the _nickname_ of the creator of this room in the channel name")
            error_embed.add_field(inline=True, name="Little updated parameters (due to discord timeout):",
                                  value="┣ **{/branch/}** - to create a visual _channels branch_\n┣ **{/rainbow/}** - to create a rainbow of rooms\n┗ **{/counter/}** - to display the room number")
            error_embed.set_footer(
                text=f"P.S. You can also change the standard rooms name and special characters, for example: {BotConfig.BotPrefixes[0]}addmarker {randint(10 ** (18 - 1), 10 ** 18 - 1)} {randint(10 ** (18 - 1), 10 ** 18 - 1)} " + "{/branch/}🎄Party {〖/counter/〗}")
            await ctx.send(embed=error_embed)
            # sending data to the terminal
            print(f"ERROR: Incorrect data entry")
    # catching errors when adding a marker
    except Exception as E:
        # generating an embed that informs you of an error and sending it
        error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                    title="**Room** - Oops, something __went wrong__ when you set the marker😳")
        error_embed.add_field(inline=True, name="Technical support site:", value=f"{BotConfig.BotSite}")
        error_embed.add_field(inline=True, name="Error date:", value=f"{datetime.datetime.today()}")
        error_embed.add_field(inline=True, name="Сause of error:", value=f"{E}")
        await ctx.send(embed=error_embed)
        # sending data to the terminal
        print(f"ERROR: {E}")
    # sending data to the terminal
    print("-----------------------------")


# catching errors about a lack of rights
@addmarker.error
async def addmarker_error(ctx, error):
    # generating an embed that informs you of an error and sending it
    error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                title="**Room** - You __don't have__ enough __rights__ to add markers🤨")
    await ctx.send(embed=error_embed)


# deleting an installed marker
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def deletemarker(ctx, marker_id=None):
    # sending data to the terminal
    print(datetime.datetime.today())
    print(f"{ctx.guild.name}-->{ctx.author}")
    print(f"Command name: {BotConfig.BotPrefixes[0]}deletemarker {list(ctx.args)[1:]}")
    # logic for deleting a marker from the server
    try:
        # checking for the number of characters in the passed parameters to delete a marker from the server
        if marker_id != None and len(list(marker_id)) == 18:
            # correction of the entered data for further work with them
            marker_id = int(marker_id)
            # when the server is not registered yet
            if ctx.guild.id not in list(working_with_the_database().keys()):
                # creating and forming an embed structure
                delete_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                             title="**Room** - There is __nothing to delete__ on this server yet😄")
            # when the server is registered but the specified marker does not exist
            elif marker_id not in list(working_with_the_database()[ctx.guild.id].keys()):
                # creating and forming an embed structure
                delete_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                             title="**Room** - In any case, this channel __wasn't in__ the database🧐")
            # when everything is fine and you can delete the marker
            else:
                # uploading new data to the database
                updated_database = working_with_the_database()
                updated_database[ctx.guild.id].pop(marker_id)
                working_with_the_database(registered_channels=updated_database)
                # creating and forming an embed structure
                delete_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                             title="**Room** - The specified channel was __successfully deleted__😊")
            # adding informative data and sending embed
            delete_embed.add_field(inline=True, name="Marker ID:", value=f"{marker_id}")
            delete_embed.add_field(inline=True, name="Delete status:", value="The channel is not in the database")
            delete_embed.add_field(inline=True, name="Recommended commands:",
                                   value=f"┣ **{BotConfig.BotPrefixes[0]}addmarker**\n┗ **{BotConfig.BotPrefixes[0]}info**")
            await ctx.send(embed=delete_embed)
        # warnings about incorrect data
        else:
            # creating and sending embed
            error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                        title="**Room** - Oops, I think you're __typing__ something __wrong__😜")
            error_embed.add_field(inline=True, name="Example of the correct spelling of this command:",
                                  value=f"```{BotConfig.BotPrefixes[0]}deletemarker {randint(10 ** (18 - 1), 10 ** 18 - 1)}```")
            error_embed.add_field(inline=True, name="Recommended commands:",
                                  value=f"┣ **{BotConfig.BotPrefixes[0]}help**\n┗ **{BotConfig.BotPrefixes[0]}info**")
            await ctx.send(embed=error_embed)
            # sending data to the terminal
            print(f"ERROR: Incorrect data entry")
    # catching errors when deleting a marker
    except Exception as E:
        # generating an embed that informs you of an error and sending it
        error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                    title="**Room** - Oops, something __went wrong__ when you removed the marker😳")
        error_embed.add_field(inline=True, name="Technical support site:", value=f"{BotConfig.BotSite}")
        error_embed.add_field(inline=True, name="Error date:", value=f"{datetime.datetime.today()}")
        error_embed.add_field(inline=True, name="Сause of error:", value=f"{E}")
        await ctx.send(embed=error_embed)
        # sending data to the terminal
        print(f"ERROR: {E}")
    # sending data to the terminal
    print("-----------------------------")


# catching errors about a lack of rights
@deletemarker.error
async def deletemarker_error(ctx, error):
    # generating an embed that informs you of an error and sending it
    error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                title="**Room** - You __don't have__ enough __rights__ to delete markers🤨")
    await ctx.send(embed=error_embed)


# view information about all existing markers
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def info(ctx):
    # sending data to the terminal
    print(datetime.datetime.today())
    print(f"{ctx.guild.name}-->{ctx.author}")
    print(f"Command name: {BotConfig.BotPrefixes[0]}info {list(ctx.args)[1:]}")
    # the logic for generating the output information
    try:
        # when the server is not yet in the database
        if ctx.guild.id not in list(working_with_the_database().keys()):
            # creating and forming an embed structure
            info_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                       title="**Room** - Wow, it looks like you __haven't put__ any markers yet😀")
        # if the server is registered, but there are no markers on it
        elif list(working_with_the_database()[ctx.guild.id].keys()) == []:
            # creating and forming an embed structure
            info_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                       title="**Room** - Wow, looks like __you deleted__ all your markers😮")
        # when everything is fine and you can output data about all markers on the server
        else:
            # creating and forming an embed structure
            info_embed = discord.Embed(colour=discord.Color(0x00FF00), url=BotConfig.BotInvite,
                                       title="**Room** - Yes, of course, here are __all the channels__ with __markers__😎")
            # getting the most recent data from the database
            updated_database = working_with_the_database()
            # listing of all information about the markers on the server
            for marker_id in list(working_with_the_database()[ctx.guild.id].keys()):
                # collecting markers information
                info_embed.add_field(inline=True,
                                     name=f"Complete data about __marker__[{list(working_with_the_database()[ctx.guild.id].keys()).index(marker_id) + 1}]:",
                                     value=f"```Marker ID: {marker_id}\nCategory ID: {updated_database[ctx.guild.id][marker_id][0]}\nRooms name: {updated_database[ctx.guild.id][marker_id][1]}\nSome data: {list(updated_database[ctx.guild.id][marker_id][2].keys())}```")
        # concluding information and sending embed
        info_embed.set_footer(text="P.S. The last element is a list of active room IDs created by the bot")
        await ctx.send(embed=info_embed)
    # catching errors when checking the information on the markers
    except Exception as E:
        # generating an embed that informs you of an error and sending it
        error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                    title="**Room** - Oops, something __went wrong__ when you removed the marker😳")
        error_embed.add_field(inline=True, name="Technical support site:", value=f"{BotConfig.BotSite}")
        error_embed.add_field(inline=True, name="Error date:", value=f"{datetime.datetime.today()}")
        error_embed.add_field(inline=True, name="Сause of error:", value=f"{E}")
        await ctx.send(embed=error_embed)
        # sending data to the terminal
        print(f"ERROR: {E}")
    # sending data to the terminal
    print("-----------------------------")


# catching errors about a lack of rights
@info.error
async def info_error(ctx, error):
    # generating an embed that informs you of an error and sending it
    error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                title="**Room** - You __don't have__ enough __rights__ to view existing markers🤨")
    await ctx.send(embed=error_embed)


# working with voice channels, logic for analyzing the presence of participants in the marker and channel
@client.event
async def on_voice_state_update(member: discord.Member, before, after):
    # working with member, checking for its presence in the marker
    try:
        # checking for connection to a specific channel on the server
        if after.channel is not None:
            for guild in client.guilds:
                # checking for the presence of a server in the database
                if guild.id not in list(working_with_the_database().keys()):
                    return
                # checking the correspondence between the ID of the channel that the participant has connected to and the IDs of all existing and registered server markers
                if after.channel.id in list(working_with_the_database()[guild.id].keys()):
                    # creating a new room to move the participant to in the future
                    new_voice_channel = await guild.create_voice_channel(
                        name=f"🚪Server analysis for {member.display_name}...",
                        category=discord.utils.get(guild.categories,
                                                   id=working_with_the_database()[guild.id][after.channel.id][0]))
                    # configuring the rights of the creator who owns the channel
                    await new_voice_channel.set_permissions(member, connect=True, mute_members=True, move_members=True,
                                                            manage_channels=True)
                    # reserving channels ID for further work with the user
                    channel_id_reservation = after.channel.id
                    new_channel_id_reservation = new_voice_channel.id
                    # moving a user to a new channel
                    await member.move_to(new_voice_channel)
                    # side by side analysis of the channels, working with the database
                    client.loop.create_task(
                        server_analysis(guild=guild, channel_id_reservation=channel_id_reservation,
                                        new_channel_id_reservation=new_channel_id_reservation,
                                        room_author=member.display_name))
                    # loop to wait for the created room to be completely cleared of users
                    while len(new_voice_channel.members) != 0:
                        await client.wait_for("voice_state_update")
                    # complete removal of an empty channel from the server
                    await new_voice_channel.delete()
                    # side by side analysis of the channels, working with the database
                    client.loop.create_task(
                        server_analysis(guild=guild, channel_id_reservation=channel_id_reservation,
                                        new_channel_id_reservation=new_channel_id_reservation,
                                        room_author=member.display_name))
    # catching errors and sending them to the terminal
    except Exception as E:
        # sending data to the terminal
        print(datetime.datetime.today())
        print(f"Server: {''.join([f'{guild.name} (ID={guild.id})' for guild in client.guilds])}")
        print(f"VOICE ERROR: {E}")
        print("-----------------------------")


# full analysis of all channels that were attached to this marker at the time of the call
async def server_analysis(guild, channel_id_reservation, new_channel_id_reservation, room_author):
    # getting the most recent data from the database, adding a new room when calling the function if required
    updated_database = working_with_the_database()
    if new_channel_id_reservation not in updated_database[guild.id][channel_id_reservation][2].keys():
        updated_database[guild.id][channel_id_reservation][2].update(
            dict({new_channel_id_reservation: [room_author, datetime.datetime.now(), True]}))
    # channel-by-channel analysis of active and passive channels, database editing
    channel_number = 0
    while channel_number != len(updated_database[guild.id][channel_id_reservation][2].keys()):
        # working with the channel, if it exists at the time of calling the function
        try:
            # getting a channel from the server for further work
            channel = guild.get_channel(
                list(updated_database[guild.id][channel_id_reservation][2].keys())[channel_number])
            # if the channel is active, then go to the analysis of the next one by shifting the register
            if len(channel.members) != 0:
                channel_number += 1
            # when there are no participants in the channel, then delete it from the server and database
            else:
                await channel.delete()
                updated_database[guild.id][channel_id_reservation][2].pop(
                    list(updated_database[guild.id][channel_id_reservation][2].keys())[channel_number])
        # catching channels that no longer exist on the server, removing them from the database
        except Exception as E:
            updated_database[guild.id][channel_id_reservation][2].pop(
                list(updated_database[guild.id][channel_id_reservation][2].keys())[channel_number])
    # saving updated data to the main database
    working_with_the_database(registered_channels=updated_database)
    # calling the function to create a "channels branch" by renaming them
    for channel_id in updated_database[guild.id][channel_id_reservation][2].keys():
        client.loop.create_task(
            creating_channels_branch(guild=guild, channel_id_reservation=channel_id_reservation, channel_id=channel_id))


# renaming a "channels branch" based on updated and edited data
async def creating_channels_branch(guild, channel_id_reservation, channel_id):
    # renaming a channel if all data is still up to date
    try:
        # getting fresh data from the database for renaming
        updated_database = working_with_the_database()
        # checking to prevent the discord from being timed out by change requests
        if divmod((updated_database[guild.id][channel_id_reservation][2][channel_id][
                       1] - datetime.datetime.now()).total_seconds(), 60)[1] >= room_update_timeout * 60 and \
                updated_database[guild.id][channel_id_reservation][2][channel_id][2] != True:
            return
        # getting a channel from the server for further work with it
        channel = guild.get_channel(channel_id)
        # creating a full-fledged channel name from data
        layout_text = []
        for indicator in str("{}" + updated_database[guild.id][channel_id_reservation][1]).split("{"):
            # add the name of the room creator to the channel name
            if len(indicator.split("}")[0].split("/author/")) >= 2:
                if (indicator.split("}")[0].split("/author/")[0] != "") and (
                        indicator.split("}")[0].split("/author/")[1] != ""):
                    layout_text.append(str(indicator.split("}")[0].split("/author/")[0]) + str(
                        updated_database[guild.id][channel_id_reservation][2][channel_id][0]) + str(
                        indicator.split("}")[0].split("/author/")[1]))
                else:
                    layout_text.append(str(updated_database[guild.id][channel_id_reservation][2][channel_id][0]))
            # when you need to create a channel branch
            elif len(indicator.split("}")[0].split("/branch/")) >= 2:
                # analysis of additional characters if they are required
                if (indicator.split("}")[0].split("/branch/")[0] != "") and (
                        indicator.split("}")[0].split("/branch/")[1] != ""):
                    channels_branch_symbols = indicator.split("}")[0].split("/branch/")
                else:
                    channels_branch_symbols = ["┣", "┗"]
                # depending on where the channel is located on the server, continue the channels branch or close it
                if channel_id != list(updated_database[guild.id][channel_id_reservation][2].keys())[-1]:
                    layout_text.append(channels_branch_symbols[0])
                else:
                    layout_text.append(channels_branch_symbols[1])
            # when you need to create a rainbow of rooms
            elif len(indicator.split("}")[0].split("/rainbow/")) >= 2:
                # analysis for editing the color palette
                emoji_collection = "🔴🟠🟡🟢🔵🟣"
                if len("".join(indicator.split("}")[0].split("/rainbow/"))) >= 6:
                    emoji_collection = "".join(indicator.split("}")[0].split("/rainbow/"))
                # setting a color on a channel depending on its sequence number
                layout_text.append(emoji_collection[
                                       list(updated_database[guild.id][channel_id_reservation][2].keys()).index(
                                           channel_id) % len(emoji_collection)])
            # when you want to print the channel number from the created by marker
            elif len(indicator.split("}")[0].split("/counter/")) >= 2:
                if (indicator.split("}")[0].split("/counter/")[0] != "") and (
                        indicator.split("}")[0].split("/counter/")[1] != ""):
                    layout_text.append(str(indicator.split("}")[0].split("/counter/")[0]) + str(
                        list(updated_database[guild.id][channel_id_reservation][2].keys()).index(channel_id) + 1) + str(
                        indicator.split("}")[0].split("/counter/")[1]))
                else:
                    layout_text.append(
                        f"[{list(updated_database[guild.id][channel_id_reservation][2].keys()).index(channel_id) + 1}]")
            # add the rest of the text without instruction pointer
            layout_text.append("".join(indicator.split("}")[1:]))
        # comparison for matches of the old and new names
        if channel.name != "".join(layout_text):
            # update the time of the last timeout and omit the check box for rooms with a timeout protection exception
            updated_database[guild.id][channel_id_reservation][2][channel_id] = [
                updated_database[guild.id][channel_id_reservation][2][channel_id][0], datetime.datetime.now(), False]
            working_with_the_database(registered_channels=updated_database)
            # rename the channel with the name that passed the full analysis
            await channel.edit(name="".join(layout_text))
    # catching cases where irrelevant data was transmitted
    except Exception as E:
        pass


# sending a warning about an incorrectly entered command if the correct one was not found
@client.event
async def on_command_error(ctx, error):
    # checking whether the requested command is non-existent
    if isinstance(error, commands.CommandNotFound):
        # generating an embed that informs you of an error and sending it
        error_embed = discord.Embed(colour=discord.Color(0xFF0000), url=BotConfig.BotInvite,
                                    title=f"**Room** - Someone __doesn't know__ the __commands__, enter **{BotConfig.BotPrefixes[0]}help**🤔")
        await ctx.send(embed=error_embed)


# connect the bot to the servers discord
client.run(BotConfig.BotToken)

########################################
# - - - - - - MEB PRESENTS - - - - - - #
# Name of produce: Room-DiscordBot     #
# Author of the bot: Machnev Egor      #
# Contacts in the network:             #
# --Web-Site > smtechnology.info       #
# --Telegram > @machnev_egor           #
# --VK > https://vk.com/machnev_egor   #
# --Email > meb.official.com@gmail.com #
########################################
