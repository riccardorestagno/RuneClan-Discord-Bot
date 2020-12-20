import discord
from os import environ

from helper_methods import *

client = discord.Client()

stored_clan_tuples_file = "clan_server_mapping.txt"
website = "http://www.runeclan.com/clan/"
arrow = u"\u2192"


class RuneClanBot:

    channel = None
    clan_name = ""
    list_of_clan_server_tuples = []
    sent_message = ""

    def __init__(self, channel, clan_name, list_of_clan_server_tuples, sent_message):
        self.channel = channel
        self.clan_name = clan_name
        self.list_of_clan_server_tuples = list_of_clan_server_tuples
        self.sent_message = sent_message


def remove_clan(server):
    if not server:
        return 'This bot is not meant to work in private chat. Please enter a command on a channel of a server that this bot has joined. Use the command "!help" for more info.'

    discord_server_id = str(server.id)
    clan_name = re.split("!removeclan", RuneClanBot.sent_message, flags=re.IGNORECASE)[1].strip().replace(" ", "_")

    if test_if_clan_exists(website, clan_name) and discord_server_id in [clan_serve_tuple[0] for clan_serve_tuple in RuneClanBot.list_of_clan_server_tuples]:
        file = open(stored_clan_tuples_file, "r")
        lines = file.readlines()
        file.close()
        file = open(stored_clan_tuples_file, "w")
        for line in lines:
            if not line.startswith(discord_server_id + ","):
                file.write(line)
        file.close()

        # Removes clan from the !setclan command from the clan server tuple list if it was already there and associates the new clan to the server
        RuneClanBot.list_of_clan_server_tuples = [(server_id, name) for (server_id, name) in RuneClanBot.list_of_clan_server_tuples if server_id != discord_server_id]

        return f"This bot is no longer searching {clan_name.replace('_', ' ')}'s RuneClan page."

    return "The clan you are searching does not exist or is not being tracked by your Discord server. Please ensure the clans name is spelled correctly."


def set_clan(server):
    if not server:
        return 'This bot is not meant to work in private chat. Please enter a command on a channel of a server that this bot has joined. Use the command "!help" for more info.'

    discord_server_id = str(server.id)
    clan_name = re.split("!setclan", RuneClanBot.sent_message, flags=re.IGNORECASE)[1].strip().replace(" ", "_")

    if test_if_clan_exists(website, clan_name):
        if discord_server_id not in [clan_serve_tuple[0] for clan_serve_tuple in RuneClanBot.list_of_clan_server_tuples]:
            RuneClanBot.list_of_clan_server_tuples.append((discord_server_id, clan_name))
            with open(stored_clan_tuples_file, 'a') as output_file:
                output_file.write(f'{discord_server_id},{clan_name}\n')
        else:
            file = open(stored_clan_tuples_file, "r")
            lines = file.readlines()
            file.close()
            file = open(stored_clan_tuples_file, "w")
            for line in lines:
                if not line.startswith(discord_server_id + ","):
                    file.write(line)
            file.close()

            # Removes clan from the !setclan command from the clan server tuple list if it was already there and associates the new clan to the server
            list_of_clan_server_tuples = [(server_id, name) for (server_id, name) in RuneClanBot.list_of_clan_server_tuples if server_id != discord_server_id]
            list_of_clan_server_tuples.append((discord_server_id, clan_name))

            RuneClanBot.list_of_clan_server_tuples = list_of_clan_server_tuples

            with open(stored_clan_tuples_file, 'a') as output_file:
                output_file.write(f'{discord_server_id},{clan_name}\n')

        RuneClanBot.clan_name = clan_name

        return f"This bot is now searching {clan_name.replace('_', ' ')}'s RuneClan page."

    return "The clan you are searching does not exist or is not being tracked by RuneClan. Please ensure the clans name is spelled correctly.",


@client.event
async def get_clan_event_log():

    soup = soup_session(website + RuneClanBot.clan_name)

    events = ""
    events_counter = 0

    list_count_requested = get_requested_list_count(RuneClanBot.sent_message, 40, 10)

    if list_count_requested[1]:
        await RuneClanBot.channel.send(list_count_requested[1])
        return

    events_to_print = list_count_requested[0]

    for events_table in soup.find_all(attrs={'class': 'clan_event_box'})[0:events_to_print]:
        if " XP" in events_table.text or re.match("([0-9]{2,3} [A-Z][a-z]+)", events_table.text):
            events = f"Only {str(events_counter)} events are currently recorded on {RuneClanBot.clan_name.replace('_', ' ')}'s RuneClan page:\n\n" + events
            break

        events += events_table.text + "\n"
        events_counter += 1

    events = events.replace(".", " " + arrow + " ")
    events = events.replace("!", " " + arrow + " ")

    await RuneClanBot.channel.send(events)


@client.event
async def get_clan_achievements():

    soup = soup_session(website + RuneClanBot.clan_name)

    achievements = ""
    index = 0
    total_achievements_displayed = 0
    list_count_requested = get_requested_list_count(RuneClanBot.sent_message, 40, 10)

    if list_count_requested[1]:
        await RuneClanBot.channel.send(list_count_requested[1])
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
        achievements = f"Only {str(total_achievements_displayed)} clan achievements are currently recorded on {RuneClanBot.clan_name.replace('_', ' ')}'s RuneClan page:\n\n" + achievements

    await RuneClanBot.channel.send(achievements)


@client.event
async def get_clan_hiscores():

    soup = soup_session(website + RuneClanBot.clan_name + "/hiscores")

    table_cell = 0
    list_to_print = ""

    list_count_requested = get_requested_list_count(RuneClanBot.sent_message, 25, 15)

    if list_count_requested[1]:
        await RuneClanBot.channel.send(list_count_requested[1])
        return

    rows_to_print = list_count_requested[0]

    for table in soup.find_all('table')[2:]:
        for _ in soup.find_all('tr'):
            row = table.find_all('td')
            list_to_print += f"Rank {row[table_cell].text}: {row[table_cell+1].text} {arrow} Total Level: {row[table_cell+2].text} {arrow} Total xp: {row[table_cell+3].text} xp\n"

            if int(row[table_cell].text) == rows_to_print:
                break
            else:
                table_cell += 4

    list_to_print = f"{RuneClanBot.clan_name.replace('_', ' ')}'s Overall Hiscores:\n\n" + list_to_print

    await RuneClanBot.channel.send(list_to_print)


@client.event
async def get_key_ranks():

    soup = soup_session(website + RuneClanBot.clan_name)

    list_to_print = ""

    for names in soup.find_all(attrs={'class': 'clan_ownerbox'}):
        list_to_print += (names.text[2:] + " " + arrow + " " + names('img')[0]['alt'] + "\n")

    await RuneClanBot.channel.send(list_to_print)


@client.event
async def get_clan_info():

    soup = soup_session(website + RuneClanBot.clan_name)

    list_to_print = RuneClanBot.clan_name.replace('_', ' ') + " - Clan Info:\n"

    for clan_info in soup.find_all('span', attrs={'class': 'clan_subtext'}):
        list_to_print += clan_info.text + " " + clan_info.next_sibling + "\n"  # next sibling prints out untagged text

    await RuneClanBot.channel.send(list_to_print)


@client.event
async def get_todays_hiscores():

    soup = soup_session(website + RuneClanBot.clan_name + "/xp-tracker")

    todays_hiscores = ""
    list_count_requested = get_requested_list_count(RuneClanBot.sent_message, 40, 10)

    if list_count_requested[1]:
        await RuneClanBot.channel.send(list_count_requested[1])
        return

    rows_to_print = list_count_requested[0]

    table = soup.find_all('table')[3]

    for row_cell in table.find_all('tr')[1:]:
        row = row_cell.find_all('td')

        if not row:
            break

        if "Clan Total" == row[1].text:
            todays_hiscores += RuneClanBot.clan_name.replace('_', ' ') + "'s Total Xp for Today: " + row[2].text + " xp\n\n"
            continue

        # Prevents row duplication.
        if f"Rank {row[0].text}:" in todays_hiscores:
            continue

        todays_hiscores += f"Rank {row[0].text}: {row[1].text} {arrow} Total xp: {row[2].text} xp\n"

        if int(row[0].text) == rows_to_print:
            break

    await RuneClanBot.channel.send(todays_hiscores)


@client.event
async def get_skills_of_the_month_time_remaining():

    soup = soup_session(website + RuneClanBot.clan_name + "/competitions")

    competition_rows = get_active_competition_rows(website, RuneClanBot.clan_name)
    row_index = 0
    time_left = ""

    if competition_rows == 0:
        await RuneClanBot.channel.send(RuneClanBot.clan_name.replace('_', ' ') + " has no active competitions at this time.")
    else:
        row = None
        for table in soup.find_all('table')[4:]:
            row = table.find_all('td')

        if row:
            while competition_rows > 0:
                if row[row_index+2].find('span').text == "active":
                    time_left += "The currently active " + row[row_index+1].text + " XP competition has " + row[row_index+4].text[:-6] + " remaining!\n"
                competition_rows -= 1
                row_index += 5

        await RuneClanBot.channel.send(time_left)


@client.event
async def get_skills_of_the_month():

    soup = soup_session(website + RuneClanBot.clan_name + "/competitions")

    active_competition_rows = get_active_competition_rows(website, RuneClanBot.clan_name)
    row_index = 0
    skills_to_print = ""

    if active_competition_rows == 0:
        await RuneClanBot.channel.send(RuneClanBot.clan_name.replace('_', ' ') + " has no active competitions at this time.")
    else:
        row = None
        for table in soup.find_all('table')[4:]:
            for _ in soup.find_all('tr'):
                row = table.find_all('td')
        if row:
            while active_competition_rows > 0:
                if row[row_index+2].find('span').text == "active":
                    skills_to_print += row[row_index+1].text + ", "
                row_index += 5

        await RuneClanBot.channel.send(skills_to_print[:-2])


@client.event
async def get_skills_of_the_month_hiscores():

    soup = soup_session(website + RuneClanBot.clan_name + "/competitions")

    table = soup.find_all('td', {'class': 'competition_td competition_name'})
    skills_of_the_month = get_skills_in_clan_competition(website, RuneClanBot.clan_name)
    active_competition_rows = get_active_competition_rows(website, RuneClanBot.clan_name)

    list_count_requested = get_requested_list_count(RuneClanBot.sent_message, 10, 5)

    if list_count_requested[1]:
        await RuneClanBot.channel.send(list_count_requested[1])
        return

    rows_to_print = list_count_requested[0]

    list_of_ranks = []
    list_of_skills = []

    player_rank_count = 0
    skill_header_count = 0
    skill_count = 0
    if active_competition_rows == 0:
        await RuneClanBot.channel.send(RuneClanBot.clan_name.replace('_', ' ') + " has no active competitions at this time.")
    else:
        for row in table:
            for link in row.find_all('a', href=True):

                soup = soup_session(f"{website}{RuneClanBot.clan_name}/{link['href']}")

                row_index = 0
                for table in soup.find_all('table')[3:]:
                    while skill_header_count < active_competition_rows:
                        list_of_skills.append(f"{RuneClanBot.clan_name.replace('_', ' ')}'s competition hiscores:\n {skills_of_the_month[1+skill_count].text}")
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

        while skills < active_competition_rows:
            list_to_print += list_of_skills[skills]
            for row in list_of_ranks[skills*rows_to_print:(skills*rows_to_print) + rows_to_print]:
                list_to_print += str(row) + "\n\n"

            skills += 1

        try:
            await RuneClanBot.channel.send(list_to_print)
        except discord.errors.HTTPException:
            await RuneClanBot.channel.send("Character limit exceeded. Please reduce the amount of ranks you wish to search for.")


@client.event
async def get_bots_commands():
    await RuneClanBot.channel.send("""RuneClan Discord bot commands:

"!setclan [Clan Name]": Sets the clan you wish to search for on RuneClan 

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

Things to note:
  1. The "top [x]" feature is optional, and the default value is used if not entered.
  2. This bot is not meant to work in private chat.

- Bot made by Slick Rick""")


@client.event
async def on_message(message):

    RuneClanBot.channel = message.channel
    RuneClanBot.sent_message = message.content.replace("'", "")

    if RuneClanBot.sent_message.lower() == "!help":
        await get_bots_commands()
        return

    if not RuneClanBot.list_of_clan_server_tuples:
        RuneClanBot.list_of_clan_server_tuples = open_external_file(stored_clan_tuples_file)

    if RuneClanBot.sent_message.lower().startswith("!setclan "):

        set_clan_message = set_clan(message.guild)
        await RuneClanBot.channel.send(set_clan_message)
        return

    elif RuneClanBot.sent_message.lower().startswith("!removeclan "):

        remove_clan_message = remove_clan(message.guild)
        await RuneClanBot.channel.send(remove_clan_message)
        return

    for server, name_of_clan in RuneClanBot.list_of_clan_server_tuples:
        if server == str(message.guild.id):
            RuneClanBot.clan_name = name_of_clan
            try:
                command = list_of_commands[RuneClanBot.sent_message.lower().rsplit(" top", 1)[0].strip()]
                await command()
            except KeyError:
                pass

            return


if __name__ == '__main__':

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

    client.run(environ["RUNECLANBOT_TOKEN"])
