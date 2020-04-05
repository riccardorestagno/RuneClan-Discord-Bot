import discord
import re
from bs4 import BeautifulSoup
from itertools import chain
from os import environ
from urllib.request import urlopen


client = discord.Client()
text_files_path = environ["RUNECLANBOT_TEXT_FILES_PATH"]

list_of_clan_server_tuples = []
stored_clan_tuples = f"{text_files_path}\\ClanServerTuples.txt"
stored_next_clan_event = f"{text_files_path}\\NextClanEvent.txt"
stored_upcoming_clan_events = f"{text_files_path}\\UpcomingClanEvents.txt"
arrow = u"\u2192"

# Imgur link: http://imgur.com/a/1ouSX
# add bot to server link: https://discordapp.com/oauth2/authorize?client_id=292458395280080907&scope=bot&permissions=0


def test_if_clan_correct(clan_name):
    envision = "http://www.runeclan.com/clan/" + clan_name
    page = urlopen(envision)
    soup = BeautifulSoup(page, "html.parser")
    list_to_print = ""
    for names in soup.find_all('span', attrs={'class': 'clan_subtext'}):
        list_to_print += names.text + " " + names.next_sibling + "\n"  # next sibling prints out untagged text
    page.close()
    return list_to_print


def get_custom_event():
    if sent_message.startswith("next event"):
        event_file = stored_next_clan_event
    if sent_message.startswith("upcoming events"):
        event_file = stored_upcoming_clan_events
    with open(event_file, 'r') as file:
        clan_event = file.read()
        clan_event = clan_event.split(clan_name.lower() + ",", 1)
        clan_event = clan_event[1].split("Event ends here!", 1)
    return clan_event[0]


def open_external_file():
    with open(stored_clan_tuples, "r") as file:
        tmp_list_of_clan_server_tuples = []
        for line in file.readlines():
            line = line.split(",")
            tmp_list_of_clan_server_tuples.append((line[0], line[1][:-1]))

    return tmp_list_of_clan_server_tuples


def get_active_competition_rows():
    envision = "http://www.runeclan.com/clan/" + clan_name + "/competitions"
    page = urlopen(envision)
    soup = BeautifulSoup(page, "html.parser")
    count = 0
    table_cell = 0
    for table in soup.find_all('table')[4:]:
        for row_tag in soup.find_all('tr'):
            row = table.find_all('td')
            try:
                if row[table_cell+2].find('span').text == "active":
                    count += 1
                table_cell += 5
            except (AttributeError, IndexError):
                break

    return count


def get_skills_of_the_month_no_print():
    envision = "http://www.runeclan.com/clan/" + clan_name + "/competitions"
    page = urlopen(envision)
    soup = BeautifulSoup(page,"html.parser")
    for table in soup.find_all('table')[4:]:
        for row in soup.find_all('tr'):
            return table.find_all('td')


def get_requested_list_count(message, max_list, default):
    try:
        if "top" in message:
            if not message.split("top", 1)[1].strip().isdigit() or not 1 <= int(message.split("top", 1)[1].strip()) <= max_list:
                return 0, f"This feature is only valid for integer values between 1 and {max_list}."
            else:
                return int(message.split("top", 1)[1].strip()), ""
    except:
        return 0, f"This feature is only valid for integer values between 1 and {max_list}."

    return default, ""


@client.event
async def get_clan_event_log():
    envision = "http://www.runeclan.com/clan/" + clan_name
    page = urlopen(envision)
    soup = BeautifulSoup(page, "html.parser")
    events = ""
    clan_name_to_print = clan_name.replace("_", " ")
    events_counter = 0
    break_necessary = 0

    list_count_requested = get_requested_list_count(sent_message, 40, 10)

    if list_count_requested[1]:
        await channel.send(list_count_requested[1])
        return

    events_to_print = list_count_requested[0]

    for names in soup.find_all(attrs={'class': 'clan_event_box'})[0:events_to_print]:
        if " XP" in names.text:
            break_necessary += 1
            break
        else:
            events += names.text + "\n"
            events_counter += 1

    events = events.replace(".", " " + arrow + " ")
    events = events.replace("!", " " + arrow + " ")

    if break_necessary == 1:
        events = "Only " + str(events_counter) + " events are currently recorded on " + clan_name_to_print + "'s RuneClan page:\n" + events

    await channel.send(events)
    page.close()


@client.event
async def get_clan_achievements():
    envision = "http://www.runeclan.com/clan/" + clan_name
    page = urlopen(envision)
    soup = BeautifulSoup(page, "html.parser")
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
        achievements = "Only " + str(total_achievements_displayed) + " clan achievements are currently recorded on " + clan_name_to_print + "'s RuneClan page:\n" + achievements

    await channel.send(achievements)
    page.close()


@client.event
async def get_clan_hiscores():
    envision = "http://www.runeclan.com/clan/" + clan_name + "/hiscores"
    page = urlopen(envision)
    soup = BeautifulSoup(page, "html.parser")
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

    hiscore_header = clan_name_to_print + "'s Overall Hiscores:\n\n"
    new_list_to_print = hiscore_header + list_to_print
    await channel.send(new_list_to_print)
    page.close()


@client.event
async def get_key_ranks():
    clan_url = "http://www.runeclan.com/clan/" + clan_name
    page = urlopen(clan_url)
    soup = BeautifulSoup(page, "html.parser")
    new_list_to_print = ""
    for names in soup.find_all(attrs={'class': 'clan_ownerbox'}):
        list_to_print = (names.text[2:] + " " + arrow + " " + names('img')[0]['alt'] + "\n")
        new_list_to_print += list_to_print
    await channel.send(new_list_to_print)
    page.close()


@client.event
async def get_clan_info():
    envision = "http://www.runeclan.com/clan/" + clan_name
    page = urlopen(envision)
    soup = BeautifulSoup(page, "html.parser")
    clan_name_to_print = clan_name.replace("_", " ")
    list_to_print = clan_name_to_print + " - Clan Info:\n"
    for names in soup.find_all('span', attrs={'class': 'clan_subtext'}):
        list_to_print += names.text + " " + names.next_sibling + "\n"  # next sibling prints out untagged text
    await channel.send(list_to_print)
    page.close()


@client.event
async def get_todays_hiscores():
    clan_url = "http://www.runeclan.com/clan/" + clan_name + "/xp-tracker"
    page = urlopen(clan_url)
    soup = BeautifulSoup(page, "html.parser")
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
    page.close()


@client.event
async def get_skills_of_the_month_time_remaining():
    envision = "http://www.runeclan.com/clan/" + clan_name +"/competitions"
    page = urlopen(envision)
    soup = BeautifulSoup(page, "html.parser")
    competition_rows = get_active_competition_rows()
    clan_name_to_print = clan_name.replace("_", " ")
    i = 0
    time_left = ""
    if competition_rows == 0:
        await channel.send(clan_name_to_print + " has no active competitions at this time.")
    else:
        for tr in soup.find_all('table')[4:]:
            tds = tr.find_all('td')
        while competition_rows > 0:
            if tds[2+i].find('span').text == "active":
                time_left += "The currently active " + tds[1+i].text + " XP competition has " + tds[4+i].text[:-6] + " remaining!\n"
            competition_rows -= 1
            i += 5
        await channel.send(time_left)
        page.close()


@client.event
async def get_current_event():
    clan_name_to_print = clan_name.replace("_", " ")
    try:
        await channel.send(get_custom_event())
    except:
        await channel.send(clan_name_to_print + " has no custom events at this time.")


@client.event
async def set_event():    
    event_set = ""
    is_searching_event = True
    
    if sent_message.startswith("set next event:"):
        event_file = stored_next_clan_event
        event_set = sent_message.replace("set next event:", "")
    if sent_message.startswith("set upcoming events:"):
        event_file = stored_upcoming_clan_events
        event_set = sent_message.replace("set upcoming events:", "")
        
    with open(event_file, 'r') as file:
        clan_event = file.read()
        
    if clan_name + "," not in clan_event:
        with open(event_file, 'a') as outputfile:
            outputfile.writelines('{0},{1}{2}'.format(clan_name.lower(), event_set, "Event ends here!\n"))
    else:
        file = open(event_file, "r")
        lines = file.readlines()
        file.close()
        file = open(event_file, "w")
        for line in lines:
            if not line.startswith(clan_name + ",") and is_searching_event:
                file.write(line)
            else:               
                is_searching_event = "Event ends here!" in line

        file.close()
        
        with open(event_file, 'a') as output_file:
            output_file.writelines('{0},{1}{2}'.format(clan_name.lower(), event_set, "Event ends here!\n"))
            
    await channel.send("These events have been set")


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
    envision = "http://www.runeclan.com/clan/" + clan_name + "/competitions"
    page = urlopen(envision)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find_all('td', {'class': 'competition_td competition_name'})
    tds1 = get_skills_of_the_month_no_print()
    no_of_rows = get_active_competition_rows()
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
    if get_active_competition_rows() == 0:
        await channel.send(clan_name_to_print + " has no active competitions at this time.")
    else:
        for n in table:
            for a in n.find_all('a', href=True):
                newLinkToSearch = "http://www.runeclan.com/clan/Envision/" + a['href']
                newPage = urlopen(newLinkToSearch)
                soup = BeautifulSoup(newPage, 'html.parser')
                i = 0
                for tr in soup.find_all('table')[3:]:
                    while skill_header_count < no_of_rows:
                        list_of_skills.append(f"{clan_name_to_print}'s competition hiscores:\n {tds1[1+skill_count].text}")
                        skill_header_count += 1
                        skill_count += 5
                    try:
                        tds = tr.find_all('td')
                        list_of_ranks.append(f"Rank {tds[0+i].text}: {tds[1+i].text} {arrow} Xp Gained: {tds[2+i].text} xp")
                        if tds[0+i].text == rows_to_print:
                            player_rank_count += 1
                            break
                        else:
                            i += 3
                        player_rank_count += 1
                    except IndexError:
                        break

        list_to_print = ""
        skill_headers = 0
        skills = 0

        while skills < no_of_rows:
            list_to_print += list_of_skills[skill_headers]
            for row in list_of_ranks[skills*rows_to_print:(skills*rows_to_print) + rows_to_print]:
                list_to_print += str(row) + "\n"
                list_to_print += "\n"
            skill_headers += 1
            skills += 1
            
        try:
            await channel.send(list_to_print)
        except:
            await channel.send("Character limit exceeded. Please reduce the amount of ranks you wish to search for.")
            
        page.close()
        newPage.close()


@client.event
async def get_bots_commands():
    await channel.send("""RuneClan Discord bot commands:

"setclan [Clan Name]": Sets the clan you wish to search for on runeclan 

"help!": Prints everything that you're seeing right now
"hiscores top [x]": Prints clans overall hiscores (default: top 15)
"todays hiscores top [x]": Prints clans overall hiscores for today (default: top 10)
"competitions": Lists the currently active competitions on RuneClan
"competitions hiscores top [x]": Shows the hiscores for all active clan competitions  (default: top 5 for each skill) 
"competitions time": Tell you how much time is remaining in the active competitions listed on RuneClan
"clan info": Prints the clan info listed on RuneClan 
"key ranks": Lists the clans key ranks
"events top [x]": Prints the clan event log as seen on RuneClan (default: 10 most recent)
"achievements top [x]": Prints the clan achievement log as seen on RuneClan (default: 10 most recent)
"set next event: [event]": Records a customizable event that can be printed later (can be cleared by leaving [event] empty)
"next event": Prints the customized event that has been previously set
"set upcoming events: [events]": Records customizable events that can be printed later (can be cleared by leaving [events] empty)
"upcoming events": Prints the customized events that have been previously set

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
        "!clan info": get_clan_info,
        "!set next event": set_event,
        "!upcoming events": get_current_event
    }

    channel = message.channel
    sent_message = message.content.lower().replace("'", "")

    if sent_message == "!help":
        await get_bots_commands()

    if not list_of_clan_server_tuples:
        list_of_clan_server_tuples = open_external_file()

    if sent_message.startswith("setclan"):
        discord_server_name = str(message.guild)
        clan_name = sent_message.split("setclan")[1].strip().replace(" ", "_")

        if discord_server_name == "None":
            await channel.send('This bot is not meant to work in private chat. Please enter a command on a channel of a server that this bot has joined. Use the command "!help" for more info.')
            return
        elif not test_if_clan_correct(clan_name):
            await channel.send("The clan you are searching does not exist or is not being searched by RuneClan. Please ensure the clans name is spelled correctly.")
        else:
            if discord_server_name not in chain(*list_of_clan_server_tuples):
                list_of_clan_server_tuples.append((discord_server_name, clan_name))
                with open(stored_clan_tuples, 'a') as output_file:
                    output_file.writelines(f'{discord_server_name},{clan_name}\n')
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
                    output_file.writelines('{0},{1}{2}'.format(discord_server_name, clan_name, "\n"))

            clan_name_to_type = sent_message.split("setclan")[1].strip()

            await channel.send("This bot is now searching " + clan_name_to_type + "'s RuneClan page.")

    for server, name_of_clan in list_of_clan_server_tuples:
        if server == str(message.guild):
            clan_name = name_of_clan
            try:
                command = list_of_commands[sent_message.rsplit(" top", 1)[0].strip()]
                await command()
            except KeyError:
                pass

            return

    if sent_message in list_of_commands:
        await channel.send("This command isn't recognized. Please ensure you have used the 'setclan' command for this server.")

if __name__ == '__main__':
    client.run(environ["RUNECLANBOT_TOKEN"])
