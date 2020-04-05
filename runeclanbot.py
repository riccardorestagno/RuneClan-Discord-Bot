import discord
from itertools import chain
from os import environ
from urllib.request import urlopen

from helper_methods import *


client = discord.Client()
text_files_path = environ["RUNECLANBOT_TEXT_FILES_PATH"]

list_of_clan_server_tuples = []
stored_clan_tuples = f"{text_files_path}\\ClanServerTuples.txt"
arrow = u"\u2192"


@client.event
async def get_clan_event_log():

    soup = soup_session("http://www.runeclan.com/clan/" + clan_name)

    events = ""
    events_counter = 0
    event_list_end = False

    list_count_requested = get_requested_list_count(sent_message, 40, 10)

    if list_count_requested[1]:
        await channel.send(list_count_requested[1])
        return

    events_to_print = list_count_requested[0]

    for events_table in soup.find_all(attrs={'class': 'clan_event_box'})[0:events_to_print]:
        if " XP" in events_table.text or re.match("([0-9]{2,3} [A-Z][a-z]+)", events_table.text):
            event_list_end = True
            break

        events += events_table.text + "\n"
        events_counter += 1

    events = events.replace(".", " " + arrow + " ")
    events = events.replace("!", " " + arrow + " ")

    if event_list_end:
        events = "Only " + str(events_counter) + " events are currently recorded on " + clan_name.replace("_", " ") + "'s RuneClan page:\n\n" + events

    await channel.send(events)


@client.event
async def get_clan_achievements():

    soup = soup_session("http://www.runeclan.com/clan/" + clan_name)

    achievements = ""
    clan_name_to_print = clan_name.replace("_", " ")
    index = 0
    total_achievements_displayed = 0
    list_count_requested = get_requested_list_count(sent_message, 40, 10)

    if list_count_requested[1]:
        await channel.send(list_count_requested[1])
        return

    achievements_to_print = list_count_requested[0]

    for clan_achievements_table in soup.find_all(attrs={'class': 'clan_event_box'}):
        if " XP" not in clan_achievements_table.text and not re.match("([0-9]{2,3} [A-Z][a-z]+)", clan_achievements_table.text):
            index += 1
        else:
            break

    for clan_achievements_table in soup.find_all(attrs={'class': 'clan_event_box'})[index:index + achievements_to_print]:
        achievements += clan_achievements_table.text + "\n"
        total_achievements_displayed += 1

    achievements = achievements.replace("XP", "XP " + arrow + " ")

    achievements = re.sub("([0-9]{2,3} [A-Z][a-z]+)", r"\1" + " " + arrow + " ", achievements)

    if total_achievements_displayed != achievements_to_print:
        achievements = "Only " + str(total_achievements_displayed) + " clan achievements are currently recorded on " + clan_name_to_print + "'s RuneClan page:\n\n" + achievements

    await channel.send(achievements)


@client.event
async def get_clan_hiscores():

    soup = soup_session("http://www.runeclan.com/clan/" + clan_name + "/hiscores")

    clan_name_to_print = clan_name.replace("_", " ")
    table_cell = 0
    list_to_print = ""

    list_count_requested = get_requested_list_count(sent_message, 25, 15)

    if list_count_requested[1]:
        await channel.send(list_count_requested[1])
        return

    rows_to_print = list_count_requested[0]

    for table in soup.find_all('table')[2:]:
        for row_tag in soup.find_all('tr'):
            row = table.find_all('td')
            list_to_print += f"Rank {row[table_cell].text}: {row[table_cell+1].text} {arrow} Total Level: {row[table_cell+2].text} {arrow} Total xp: {row[table_cell+3].text} xp\n"

            if int(row[table_cell].text) == rows_to_print:
                break
            else:
                table_cell += 4

    list_to_print = clan_name_to_print + "'s Overall Hiscores:\n\n" + list_to_print

    await channel.send(list_to_print)


@client.event
async def get_key_ranks():

    soup = soup_session("http://www.runeclan.com/clan/" + clan_name)

    list_to_print = ""

    for names in soup.find_all(attrs={'class': 'clan_ownerbox'}):
        list_to_print += (names.text[2:] + " " + arrow + " " + names('img')[0]['alt'] + "\n")

    await channel.send(list_to_print)


@client.event
async def get_clan_info():

    soup = soup_session("http://www.runeclan.com/clan/" + clan_name)

    list_to_print = clan_name.replace("_", " ") + " - Clan Info:\n"

    for clan_info in soup.find_all('span', attrs={'class': 'clan_subtext'}):
        list_to_print += clan_info.text + " " + clan_info.next_sibling + "\n"  # next sibling prints out untagged text

    await channel.send(list_to_print)


@client.event
async def get_todays_hiscores():

    soup = soup_session("http://www.runeclan.com/clan/" + clan_name + "/xp-tracker")

    todays_hiscores = ""
    list_count_requested = get_requested_list_count(sent_message, 40, 10)

    if list_count_requested[1]:
        await channel.send(list_count_requested[1])
        return

    rows_to_print = list_count_requested[0]

    table = soup.find_all('table')[3]

    for row_cell in table.find_all('tr')[1:]:
        row = row_cell.find_all('td')

        if "Clan Total" == row[1].text:
            todays_hiscores += clan_name.replace("_", " ") + "'s Total Xp for Today: " + row[2].text + " xp\n\n"
            continue

        # Prevents row duplication.
        if f"Rank {row[0].text}:" in todays_hiscores:
            continue

        todays_hiscores += f"Rank {row[0].text}: {row[1].text} {arrow} Total xp: {row[2].text} xp\n"

        if int(row[0].text) == rows_to_print:
            break

    await channel.send(todays_hiscores)


@client.event
async def get_skills_of_the_month_time_remaining():

    soup = soup_session("http://www.runeclan.com/clan/" + clan_name +"/competitions")

    competition_rows = get_active_competition_rows(clan_name)
    row_index = 0
    time_left = ""

    if competition_rows == 0:
        await channel.send(clan_name.replace("_", " ") + " has no active competitions at this time.")
    else:
        for table in soup.find_all('table')[4:]:
            row = table.find_all('td')
        while competition_rows > 0:
            if row[row_index+2].find('span').text == "active":
                time_left += "The currently active " + row[row_index+1].text + " XP competition has " + row[row_index+4].text[:-6] + " remaining!\n"
            competition_rows -= 1
            row_index += 5
        await channel.send(time_left)


@client.event
async def get_skills_of_the_month():
    
    envision = "http://www.runeclan.com/clan/" + clan_name + "/competitions"
    page = urlopen(envision)
    soup = BeautifulSoup(page, "html.parser")
    no_of_rows = get_active_competition_rows()
    clan_name_to_print = clan_name.replace("_", " ")
    row_index = 0
    skills_to_print = ""
    
    if get_active_competition_rows() == 0:
        await channel.send(clan_name_to_print + " has no active competitions at this time.")
    else:
        for table in soup.find_all('table')[4:]:
            for row_cell in soup.find_all('tr'):
                row = table.find_all('td')
        while no_of_rows > 0:
            if row[row_index+2].find('span').text == "active":
                skills_to_print += row[row_index+1].text + ", "
            no_of_rows -= 1
            row_index += 5
            
        await channel.send(skills_to_print[:-2])
        page.close()


@client.event
async def get_skills_of_the_month_hiscores():

    soup = soup_session("http://www.runeclan.com/clan/" + clan_name + "/competitions")

    table = soup.find_all('td', {'class': 'competition_td competition_name'})
    skills_of_the_month = get_skills_in_clan_competition(clan_name)
    row_count = get_active_competition_rows(clan_name)
    clan_name_to_print = clan_name.replace("_", " ")

    list_count_requested = get_requested_list_count(sent_message, 10, 5)

    if list_count_requested[1]:
        await channel.send(list_count_requested[1])
        return

    rows_to_print = list_count_requested[0]

    list_of_ranks = []
    list_of_skills = []

    player_rank_count = 0
    skill_header_count = 0
    skill_count = 0
    if get_active_competition_rows(clan_name) == 0:
        await channel.send(clan_name_to_print + " has no active competitions at this time.")
    else:
        for row in table:
            for link in row.find_all('a', href=True):

                soup = soup_session("http://www.runeclan.com/clan/Envision/" + link['href'])

                row_index = 0
                for table in soup.find_all('table')[3:]:
                    while skill_header_count < row_count:
                        list_of_skills.append(f"{clan_name_to_print}'s competition hiscores:\n {skills_of_the_month[1+skill_count].text}")
                        skill_header_count += 1
                        skill_count += 5
                    try:
                        rows = table.find_all('td')
                        list_of_ranks.append(f"Rank {rows[row_index].text}: {rows[row_index+1].text} {arrow} Xp Gained: {rows[row_index+2].text} xp")
                        if rows[row_index].text == rows_to_print:
                            player_rank_count += 1
                            break
                        else:
                            row_index += 3
                        player_rank_count += 1
                    except IndexError:
                        break

        list_to_print = ""
        skills = 0

        while skills < row_count:
            list_to_print += list_of_skills[skills]
            for row in list_of_ranks[skills*rows_to_print:(skills*rows_to_print) + rows_to_print]:
                list_to_print += str(row) + "\n\n"

            skills += 1
            
        try:
            await channel.send(list_to_print)
        except:
            await channel.send("Character limit exceeded. Please reduce the amount of ranks you wish to search for.")


@client.event
async def get_bots_commands():
    await channel.send("""RuneClan Discord bot commands:

"!setclan [Clan Name]": Sets the clan you wish to search for on runeclan 

"!help": Prints everything that you're seeing right now
"!hiscores top [x]": Prints clans overall hiscores (default: top 15)
"!todays hiscores top [x]": Prints clans overall hiscores for today (default: top 10)
"!competitions": Lists the currently active competitions on RuneClan
"!competitions hiscores top [x]": Shows the hiscores for all active clan competitions  (default: top 5 for each skill) 
"!competitions time": Tell you how much time is remaining in the active competitions listed on RuneClan
"!clan info": Prints the clan info listed on RuneClan 
"!key ranks": Lists the clans key ranks
"!events top [x]": Prints the clan event log as seen on RuneClan (default: 10 most recent)
"!achievements top [x]": Prints the clan achievement log as seen on RuneClan (default: 10 most recent)
"!set next event: [event]": Records a customizable event that can be printed later (can be cleared by leaving [event] empty)
"!next event": Prints the customized event that has been previously set
"!set upcoming events: [events]": Records customizable events that can be printed later (can be cleared by leaving [events] empty)
"!upcoming events": Prints the customized events that have been previously set

Things to note:
  1. The "top [x]" feature is optional, and the default value is used if not entered.
  2. This bot is not meant to work in private chat.

- Bot made by Slick Rick""")


@client.event
async def on_message(message):
    global channel
    global clan_name
    global discord_server_name
    global list_of_clan_server_tuples
    global sent_message

    list_of_commands = {
        "!sotm": get_skills_of_the_month,
        "!competitions": get_skills_of_the_month,
        "!sotm hiscores": get_skills_of_the_month_hiscores,
        "!competitions hiscores": get_skills_of_the_month_hiscores,
        "!sotm time": get_skills_of_the_month_time_remaining,
        "!competitions time": get_skills_of_the_month_time_remaining,
        "!hiscores": get_clan_hiscores,
        "!todays hiscores": get_todays_hiscores,
        "!achievements": get_clan_achievements,
        "!events": get_clan_event_log,
        "!key ranks": get_key_ranks,
        "!clan info": get_clan_info
    }

    channel = message.channel
    sent_message = message.content.replace("'", "")

    if sent_message.lower() == "!help":
        await get_bots_commands()

    if not list_of_clan_server_tuples:
        list_of_clan_server_tuples = open_external_file(stored_clan_tuples)

    if sent_message.lower().startswith("!setclan"):
        discord_server_name = str(message.guild)
        clan_name = re.split("!setclan", sent_message, flags=re.IGNORECASE)[1].strip().replace(" ", "_")

        if discord_server_name == "None":
            await channel.send('This bot is not meant to work in private chat. Please enter a command on a channel of a server that this bot has joined. Use the command "!help" for more info.')
            return
        elif not test_if_clan_exists(clan_name):
            await channel.send("The clan you are searching does not exist or is not being searched by RuneClan. Please ensure the clans name is spelled correctly.")
        else:
            if discord_server_name not in chain(*list_of_clan_server_tuples):
                list_of_clan_server_tuples.append((discord_server_name, clan_name))
                with open(stored_clan_tuples, 'a') as output_file:
                    output_file.write(f'{discord_server_name},{clan_name}\n')
            else:
                file = open(stored_clan_tuples, "r")
                lines = file.readlines()
                file.close()
                file = open(stored_clan_tuples, "w")
                for line in lines:
                    if not line.startswith(discord_server_name + ","):
                        file.write(line)
                file.close()
                temp_list_of_clan_server_tuples = [(server, name) for (server, name) in list_of_clan_server_tuples if server != discord_server_name]
                list_of_clan_server_tuples = temp_list_of_clan_server_tuples
                list_of_clan_server_tuples.append((discord_server_name, clan_name))
                with open(stored_clan_tuples, 'a') as output_file:
                    output_file.write(f'{discord_server_name},{clan_name}\n')

            clan_name_to_type = re.split("!setclan", sent_message, flags=re.IGNORECASE)[1].strip()

            await channel.send("This bot is now searching " + clan_name_to_type + "'s RuneClan page.")

    for server, name_of_clan in list_of_clan_server_tuples:
        if server == str(message.guild):
            clan_name = name_of_clan
            try:
                command = list_of_commands[sent_message.lower().rsplit(" top", 1)[0].strip()]
                await command()
            except KeyError:
                pass

            return

    for message in list(list_of_commands.keys()):
        if sent_message.lower().startswith(message):
            await channel.send("This command isn't recognized. Please ensure you have used the '!setclan' command for this server.")


if __name__ == '__main__':
    client.run(environ["RUNECLANBOT_TOKEN"])
