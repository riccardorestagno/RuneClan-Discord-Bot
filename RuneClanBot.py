from urllib.request import urlopen
from bs4 import BeautifulSoup
import discord
from itertools import chain

client = discord.Client()

list_of_clan_server_tuples = []
stored_clan_tuples = r"C:\Users\Riccardo\Desktop\Python Scripts\RuneClan Discord Bot\ClanServerTuples.txt"
stored_next_clan_event = r"C:\Users\Riccardo\Desktop\Python Scripts\RuneClan Discord Bot\NextClanEvent.txt"
stored_upcoming_clan_events = r"C:\Users\Riccardo\Desktop\Python Scripts\RuneClan Discord Bot\UpcomingClanEvents.txt"

# Imgur link: http://imgur.com/a/1ouSX
# add bot to server link: https://discordapp.com/oauth2/authorize?client_id=292458395280080907&scope=bot&permissions=0

def test_if_clan_correct():
    envision = "http://www.runeclan.com/clan/" + clan_name
    page = urlopen(envision)
    soup = BeautifulSoup(page, "html.parser")
    list_to_print = ""
    for names in soup.find_all('span', attrs={'class': 'clan_subtext'}):
        list_to_print += names.text + " " + names.next_sibling + "\n"  # next sibling prints out untagged text
    page.close()
    return list_to_print


def get_custom_event():
    if message_received.startswith("next event"):
        event_file = stored_next_clan_event
    if message_received.startswith("upcoming events"):
        event_file = stored_upcoming_clan_events
    with open(event_file, 'r') as file:
        clan_event = file.read()
        clan_event = clan_event.split(clan_name.lower() + "," , 1)
        clan_event = clan_event[1].split("Event ends here!" , 1)
    return clan_event[0]


def open_external_file():
    with open(stored_clan_tuples, "r") as file:
        tmp_list_of_clan_server_tuples = []
        for line in file.readlines():
            line = line.split(",")
            tmp_list_of_clan_server_tuples.append((line[0],line[1][:-1]))

    return tmp_list_of_clan_server_tuples


def get_active_competition_rows():
    envision = "http://www.runeclan.com/clan/"+ clan_name + "/competitions"
    page = urlopen(envision)
    soup = BeautifulSoup(page, "html.parser")
    count = 0
    i = 0
    for tr in soup.find_all('table')[4:]:
        for row in soup.find_all('tr'):
            tds = tr.find_all('td')
            try:
                if tds[2+i].find('span').text == "active":
                    count += 1
                i += 5
            except (AttributeError, IndexError):
                break
    return count


def get_skills_of_the_month_no_print():
    envision = "http://www.runeclan.com/clan/" + clan_name + "/competitions"
    page = urlopen(envision)
    soup = BeautifulSoup(page,"html.parser")
    for tr1 in soup.find_all('table')[4:]:
        for row1 in soup.find_all('tr'):
            tds1 = tr1.find_all('td')
    return tds1


@client.event
async def get_players_who_capped():
    clan_url = "https://docs.google.com/spreadsheets/d/1RYm1eVSq7op21I1xRcgqRMZMU4Ej1WVEz84QCTtBV3M/pubhtml?gid=187335414&single=true"
    page = urlopen(clan_url)
    soup = BeautifulSoup(page,"html.parser")
    list_to_print = ""
    row_count = 0
    for tr in soup.find_all('table'):
        for row in soup.find_all('tr')[7:]:
            tds = row.find_all('td')
            if tds[10].text != "":
                list_to_print += tds[2].text + ", "
                row_count += 1
    capped_header = "A total of " + str(row_count) + " people capped this week!\n"
    await client.send_message(clientID,capped_header + list_to_print[:-2])
    page.close()


@client.event
async def get_user_clan_points():
    user = clan_points_user_input[12:]
    clan_url = "https://docs.google.com/spreadsheets/d/1RYm1eVSq7op21I1xRcgqRMZMU4Ej1WVEz84QCTtBV3M/pubhtml?gid=187335414&single=true"
    page = urlopen(clan_url)
    soup = BeautifulSoup(page, "html.parser")
    for tr in soup.find_all('table'):
        for row in soup.find_all('tr')[7:]:
            tds = row.find_all('td')
            if tds[2].text == user:
                await client.send_message(clientID,tds[2].text + " has " + tds[3].text + " clan points")
                return
    page.close()


@client.event
async def get_user_rank():
    user = rank_user_input[5:]
    clan_url = "https://docs.google.com/spreadsheets/d/1RYm1eVSq7op21I1xRcgqRMZMU4Ej1WVEz84QCTtBV3M/pubhtml?gid=187335414&single=true"
    page = urlopen(clan_url)
    soup = BeautifulSoup(page, "html.parser")
    link_to_rank = ["ranks/1.", "ranks/2.", "ranks/3.", "ranks/4.", "ranks/5.", "ranks/6.", "ranks/7.", "ranks/8.",
                  "ranks/9.", "ranks/10.", "ranks/11.", "ranks/12."]
    list_of_ranks = ["Owner", "Deputy Owner", "Overseer", "Coordinator", "Organiser", "Admin", "General", "Captain",
                   "Lieutenant", "Sergeant", "Corporal", "Recruit"]
    rank_count = 0
    row_count = 0
    for tr in soup.find_all('table'):
        for row in soup.find_all('tr')[7:]:
            tds = row.find_all('td')
            if tds[2].text == user:
                for link in soup.find_all(attrs={'class' : ['s5','s10','s23']})[row_count:]:
                    for rank in link_to_rank:
                        if rank in link('div')[0]['style']:
                            await client.send_message(clientID, list_of_ranks[rank_count])
                            return
                        rank_count += 1
            row_count += 1
    page.close()


@client.event
async def get_clan_event_log():
    envision = "http://www.runeclan.com/clan/" + clan_name
    page = urlopen(envision)
    soup = BeautifulSoup(page, "html.parser")
    events = ""
    arrow = u"\u2192"
    clan_name_to_print = clan_name.replace("_", " ")
    events_to_print = 10
    events_counter = 0
    break_necessary = 0
    sent_message_nospaces = sent_message.replace(" ", "")

    try:
        if sent_message_nospaces[6:9] == "top":
            if 0 < int(sent_message_nospaces[9:]) < 41:
                events_to_print = int(sent_message_nospaces[9:])
            else:
                await client.send_message(clientID,"This feature is only valid for integer values between 1 and 40.")
                return
    except:
        await client.send_message(clientID, "This feature is only valid for integer values between 1 and 40.")
        return

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
        events = "Only "+ str(events_counter) + " events are currently recorded on " + clan_name_to_print + "'s RuneClan page:\n" + events

    await client.send_message(clientID, events)
    page.close()


@client.event
async def get_clan_achievements():
    envision = "http://www.runeclan.com/clan/"+ clan_name
    page = urlopen(envision)
    soup = BeautifulSoup(page,"html.parser")
    arrow = u"\u2192"
    achievements = ""
    clan_name_to_print = clan_name.replace("_", " ")
    achievements_start = 0
    total_achievements_displayed = 0
    achievements_to_print = 10
    sent_message_nospaces = sent_message.replace(" ", "")

    try:
        if sent_message_nospaces[12:15] == "top":
            if 0 < int(sent_message_nospaces[15:]) < 41:
                achievements_to_print = int(sent_message_nospaces[15:])
            else:
                await client.send_message(clientID,"This feature is only valid for integer values between 1 and 40.")
                return
    except:
        await client.send_message(clientID, "This feature is only valid for integer values between 1 and 40.")
        return

    for names in soup.find_all(attrs={'class' : 'clan_event_box'}):
        if " XP" not in names.text:
            achievements_start += 1
        else:
            break

    for names in soup.find_all(attrs={'class': 'clan_event_box'})[achievements_start:achievements_start + achievements_to_print]:
        achievements += names.text + "\n"
        total_achievements_displayed += 1

    achievements = achievements.replace("XP", "XP "+arrow + " ")

    max_skill_achievements = [
        "99 Attack",
        "99 Strength",
        "99 Defence",
        "99 Ranged",
        "99 Magic",
        "99 Constitution",
        "99 Prayer",
        "99 Mining",
        "99 Herblore",
        "99 Smithing",
        "99 Fletching",
        "99 Hunter",
        "99 Summoning",
        "99 Woodcutting",
        "99 Firemaking",
        "99 Runecrafting",
        "99 Thieving",
        "99 Crafting",
        "99 Fishing",
        "99 Cooking",
        "99 Agility",
        "99 Slayer",
        "99 Farming",
        "99 Divination",
        "99 Construction",
        "99 Invention",
        "120 Invention",
        "99 Dungeoneering",
        "120 Dungeoneering"]

    for skill in max_skill_achievements:
        achievements = achievements.replace(skill, skill + " "+arrow + " ")
    if total_achievements_displayed != achievements_to_print:
        achievements = "Only " + str(total_achievements_displayed) + " clan achievements are currently recorded on " + clan_name_to_print+"'s RuneClan page:\n" + achievements
    await client.send_message(clientID, achievements)
    page.close()


@client.event
async def get_clan_hiscores():
    envision = "http://www.runeclan.com/clan/" + clan_name + "/hiscores"
    page = urlopen(envision)
    soup = BeautifulSoup(page, "html.parser")
    clan_name_to_print = clan_name.replace("_", " ")
    arrow = u"\u2192"
    i = 0
    new_list_to_print = ""
    rows_to_print = "15"
    sent_message_nospaces = sent_message.replace(" ", "")
    try:
        if sent_message_nospaces[8:11] == "top":
            if 0 < int(sent_message_nospaces[11:]) < 26:
                rows_to_print = sent_message_nospaces[11:]
            else:
                await client.send_message(clientID, "This feature is only valid for integer values between 1 and 25.")
                return
    except:
        await client.send_message(clientID, "This feature is only valid for integer values between 1 and 25.")
        return
    for tr in soup.find_all('table')[2:]:
        for row in soup.find_all('tr'):
            tds = tr.find_all('td')
            list_to_print = ("Rank %s: %s %s Total Level: %s %s Total xp: %s xp\n" %
                            (tds[0+i].text, tds[1+i].text, arrow, tds[2+i].text, arrow, tds[3+i].text))
            new_list_to_print += list_to_print
            if tds[0+i].text == rows_to_print:
                break
            else:
                i += 4
    hiscore_header = clan_name_to_print + "'s Overall Hiscores:\n\n"
    new_list_to_print = hiscore_header + new_list_to_print
    await client.send_message(clientID,new_list_to_print)
    page.close()


@client.event
async def get_key_ranks():
    envision = "http://www.runeclan.com/clan/"+ clan_name
    page = urlopen(envision)
    soup = BeautifulSoup(page,"html.parser")
    arrow = u"\u2192"
    new_list_to_print = ""
    for names in soup.find_all(attrs={'class' : 'clan_ownerbox'}):
        list_to_print = (names.text[2:] + " "+arrow + " " + names('img')[0]['alt'] + "\n")
        new_list_to_print += list_to_print
    await client.send_message(clientID,new_list_to_print)
    page.close()


@client.event
async def get_clan_info():
    envision = "http://www.runeclan.com/clan/"+ clan_name
    page = urlopen(envision)
    soup = BeautifulSoup(page,"html.parser")
    clan_name_to_print = clan_name.replace("_", " ")
    list_to_print = clan_name_to_print + " - Clan Info:\n"
    for names in soup.find_all('span', attrs={'class': 'clan_subtext'}):
        list_to_print += names.text + " " + names.next_sibling + "\n"  # next sibling prints out untagged text
    await client.send_message(clientID, list_to_print)
    page.close()


@client.event
async def get_todays_hiscores():
    envision = "http://www.runeclan.com/clan/"+ clan_name +"/xp-tracker"
    page = urlopen(envision)
    soup = BeautifulSoup(page,"html.parser")
    arrow = u"\u2192"
    list_to_print = ""
    clan_name_to_print = clan_name.replace("_", " ")
    i = 0
    rows_to_print = "10"
    sent_message_nospaces = sent_message.replace(" ", "")
    try:
        if sent_message_nospaces[14:17] == "top":
            if 0 < int(sent_message_nospaces[17:]) < 41:
                rows_to_print = sent_message_nospaces[17:]
            else:
                await client.send_message(clientID, "This feature is only valid for integer values between 1 and 40.")
                return
    except:
        await client.send_message(clientID, "This feature is only valid for integer values between 1 and 40.")
        return

    for tr in soup.find_all('table')[3:]:
        tds = tr.find_all('td')
        list_to_print += "Rank %s: %s %s Total xp: %s xp\n" % \
              (tds[5+i].text, tds[6+i].text, arrow, tds[7+i].text,)
        if tds[5+i].text == rows_to_print:
            break
        else:
            i += 5
    todays_total_xp = clan_name_to_print + "'s Total Xp for Today: " + tds[2].text + " xp\n\n"
    new_list_to_print = todays_total_xp + list_to_print
    await client.send_message(clientID, new_list_to_print)
    page.close()


@client.event
async def get_skills_of_the_month_time_remaining():
    envision = "http://www.runeclan.com/clan/" + clan_name +"/competitions"
    page = urlopen(envision)
    soup = BeautifulSoup(page,"html.parser")
    competition_rows = get_active_competition_rows()
    clan_name_to_print = clan_name.replace("_", " ")
    i = 0
    time_left = ""
    if competition_rows == 0:
        await client.send_message(clientID, clan_name_to_print + " has no active competitions at this time.")
    else:
        for tr in soup.find_all('table')[4:]:
            tds = tr.find_all('td')
        while competition_rows > 0:
            if tds[2+i].find('span').text == "active":
                time_left += "The currently active " + tds[1+i].text + " XP competition has " + tds[4+i].text[:-6] + " remaining!\n"
            competition_rows -= 1
            i += 5
        await client.send_message(clientID, time_left)
        page.close()


@client.event
async def get_current_event():
    clan_name_to_print = clan_name.replace("_", " ")
    try:
        await client.send_message(clientID, get_custom_event())
    except:
        await client.send_message(clientID, clan_name_to_print + " has no custom events at this time.")


@client.event
async def set_event():    
    event_set = ""
    is_searching_event = True
    
    if message_received.startswith("set next event:"):
        event_file = stored_next_clan_event
        event_set = message_received.replace("set next event:", "")
    if message_received.startswith("set upcoming events:"):
        event_file = stored_upcoming_clan_events
        event_set = message_received.replace("set upcoming events:", "")
        
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
                if "Event ends here!" in line:
                    is_searching_event = True
                else:
                    is_searching_event = False

        file.close()
        
        with open(event_file, 'a') as outputfile:
            outputfile.writelines('{0},{1}{2}'.format(clan_name.lower(), event_set, "Event ends here!\n"))
            
    await client.send_message(clientID, "These events have been set")


@client.event
async def get_skills_of_the_month():
    
    envision = "http://www.runeclan.com/clan/"+ clan_name + "/competitions"
    page = urlopen(envision)
    soup = BeautifulSoup(page,"html.parser")
    no_of_rows = get_active_competition_rows()
    clan_name_to_print = clan_name.replace("_", " ")
    row_index = 0
    skills_to_print = ""
    
    if get_active_competition_rows() == 0:
        await client.send_message(clientID, clan_name_to_print + " has no active competitions at this time.")
    else:
        for tr in soup.find_all('table')[4:]:
            for row in soup.find_all('tr'):
                tds = tr.find_all('td')
        while no_of_rows > 0:
            if tds[2+row_index].find('span').text == "active":
                skills_to_print += tds[1+row_index].text + ", "
            no_of_rows -= 1
            row_index += 5
            
        await client.send_message(clientID, skills_to_print[:-2])
        page.close()


@client.event
async def get_skills_of_the_month_hiscores():
    envision = "http://www.runeclan.com/clan/"+ clan_name + "/competitions"
    page = urlopen(envision)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find_all('td', {'class': 'competition_td competition_name'})
    arrow = u"\u2192"
    tds1 = get_skills_of_the_month_no_print()
    no_of_rows = get_active_competition_rows()
    clan_name_to_print = clan_name.replace("_", " ")
    rows_to_print = "5"
    sent_message_nospaces = sent_message.replace(" ", "")
    
    try:
        if sent_message_nospaces[12:15] == "top":
            if 0 < int(sent_message_nospaces[15:]) < 11:
                rows_to_print = sent_message_nospaces[15:]
            else:
                await client.send_message(clientID, "This feature is only valid for integer values between 1 and 10.")
                return
        if sent_message_nospaces[20:23] == "top":
            if 0 < int(sent_message_nospaces[23:]) < 11:
                rows_to_print = sent_message_nospaces[23:]
            else:
                await client.send_message(clientID, "This feature is only valid for integer values between 1 and 10.")
                return
    except:
        await client.send_message(clientID, "This feature is only valid for integer values between 1 and 10.")
        return
    list_of_ranks = [None]*int(rows_to_print)*no_of_rows  # array for the amount of ranks to print in the message
    list_of_skills = [None]*no_of_rows  # array for the total amount of competitions

    player_rank_count = 0  # iteration for player rank list
    skill_header_count = 0  # iteration for skill header
    skill_count = 0  # iteration for specific skill
    if get_active_competition_rows() == 0:
        await client.send_message(clientID, clan_name_to_print + " has no active competitions at this time.")
    else:
        for n in table:
            for a in n.find_all('a', href=True):
                newLinkToSearch = "http://www.runeclan.com/clan/Envision/" + a['href']
                newPage = urlopen(newLinkToSearch)
                soup = BeautifulSoup(newPage, 'html.parser')
                i = 0
                for tr in soup.find_all('table')[3:]:
                    while skill_header_count < no_of_rows:
                        list_of_skills[skill_header_count] =  clan_name_to_print + "'s %s competition hiscores:\n" % tds1[1+skill_count].text
                        skill_header_count += 1
                        skill_count += 5
                    try:
                        tds = tr.find_all('td')
                        list_of_ranks[player_rank_count] = "Rank %s: %s %s Xp Gained: %s xp" % \
                            (tds[0+i].text, tds[1+i].text, arrow, tds[2+i].text)
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
            for row in list_of_ranks[skills*int(rows_to_print):(skills*int(rows_to_print)) + int(rows_to_print)]:
                list_to_print += str(row) + "\n"
                list_to_print += "\n"
            skill_headers += 1
            skills += 1
            
        try:
            await client.send_message(clientID, list_to_print)
        except:
            await client.send_message(clientID, "Character limit exceeded. Please reduce the amount of ranks you wish to search for.")
            
        page.close()
        newPage.close()


@client.event
async def get_bots_commands():
    await client.send_message(clientID,
        '''RuneClan Discord bot commands:
        
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
        
        - Bot made by Slick Rick''')


@client.event
async def on_message(message):
    global clientID
    global clan_name
    global discord_server_name
    global list_of_clan_server_tuples
    global sent_message
    global message_received

    list_of_commands = {
        "sotm": get_skills_of_the_month,
        "competitions": get_skills_of_the_month,
        "sotm hiscores": get_skills_of_the_month_hiscores,
        "competitions hiscores": get_skills_of_the_month_hiscores,
        "sotm hiscores top": get_skills_of_the_month_hiscores,
        "competitions hiscores top": get_skills_of_the_month_hiscores,
        "sotm time": get_skills_of_the_month_time_remaining,
        "competitions time": get_skills_of_the_month_time_remaining,
        "hiscores": get_clan_hiscores,
        "hiscores top": get_clan_hiscores,
        "todays hiscores": get_todays_hiscores,
        "todays hiscores top": get_todays_hiscores,
        "achievements": get_clan_achievements,
        "achievements top": get_clan_achievements,
        "events": get_clan_event_log,
        "events top": get_clan_event_log,
        "key ranks": get_key_ranks,
        "clan info": get_clan_info,
        "set next event": set_event,
        "upcoming events": get_current_event
    }

    clientID = message.channel
    sent_message = message.content.lower().replace("'", "")

    if message.content == "help!":
        await get_bots_commands()

    if not list_of_clan_server_tuples:
        list_of_clan_server_tuples = open_external_file()

    if message.content.startswith("setclan"):
        discord_server_name = str(message.server)
        clan_name = message.content[8:].replace(" ", "_")
        if discord_server_name == "None":
            await client.send_message(clientID, 'This bot is not meant to work in private chat. \
Please enter a command on a channel of a server that this bot has joined. Use the command "help!" for more info.')
            return
        if not test_if_clan_correct():
            await client.send_message(clientID, "The clan you are searching does not exist or is not being searched by RuneClan. \
Please ensure the clans name is spelled correctly.")
        else:
            if discord_server_name not in chain(*list_of_clan_server_tuples):
                list_of_clan_server_tuples.append((discord_server_name, clan_name))
                with open(stored_clan_tuples, 'a') as outputfile:
                    outputfile.writelines('{0},{1}{2}'.format(discord_server_name, clan_name,"\n"))
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
                with open(stored_clan_tuples, 'a') as outputfile:
                    outputfile.writelines('{0},{1}{2}'.format(discord_server_name, clan_name,"\n"))

            clan_name_to_type = message.content[8:]
            await client.send_message(clientID, "This bot is now searching " + clan_name_to_type + "'s RuneClan page.")

    for server, name_of_clan in list_of_clan_server_tuples:
        if server == str(message.server):
            clan_name = name_of_clan
            try:
                if any(char.isdigit() for char in sent_message):
                    command = list_of_commands[sent_message.rsplit(" ", 1)[0]]
                    await command()
                else:
                    command = list_of_commands[sent_message]
                    await command()
            except KeyError:
                pass

            if name_of_clan.lower() == 'envision':
                if sent_message == "capped this week":
                    await get_players_who_capped()
                elif message.content.startswith("rank"):
                    global rank_user_input
                    rank_user_input = message.content
                    await get_user_rank()
                elif message.content.startswith("clan points"):
                    global clan_points_user_input
                    clan_points_user_input = message.content
                    await get_user_clan_points()
            return

    if sent_message in list_of_commands:
        await client.send_message(clientID, "This command isn't recognized. Please ensure you have used the 'setclan' command for this server.")

client.run('MjkyNDU4Mzk1MjgwMDgwOTA3.C64V7A.S6UuOWydAX1E5Eret6pCq4YcdOo')
