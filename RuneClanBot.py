from urllib.request import urlopen
from bs4 import BeautifulSoup, SoupStrainer
import discord
from discord.ext import *
import asyncio
from itertools import chain

client = discord.Client() 

global list_of_clan_server_tuples
global stored_clan_tuples
global stored_next_clan_event
global stored_upcoming_clan_events 

list_of_clan_server_tuples = []
stored_clan_tuples = r"C:\Users\Riccardo\Desktop\Python Scripts\RuneClan Discord Bot\ClanServerTuples.txt"
stored_next_clan_event = r"C:\Users\Riccardo\Desktop\Python Scripts\RuneClan Discord Bot\NextClanEvent.txt"
stored_upcoming_clan_events = r"C:\Users\Riccardo\Desktop\Python Scripts\RuneClan Discord Bot\UpcomingClanEvents.txt"

# Imgur link: http://imgur.com/a/1ouSX
# add bot to server link: https://discordapp.com/oauth2/authorize?client_id=292458395280080907&scope=bot&permissions=0

def test_if_clan_correct():
	envision = "http://www.runeclan.com/clan/"+ clan_name
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	listToPrint = ""
	for names in soup.find_all('span', attrs={'class' : 'clan_subtext'}):
		listToPrint += names.text +" "+ names.next_sibling + "\n" #next sibling prints out untagged text 
	page.close()
	return listToPrint

			
def get_custom_event():
	if message_received.startswith("next event"):
		event_file = stored_next_clan_event
	if message_received.startswith("upcoming events"):
		event_file = stored_upcoming_clan_events
	with open(event_file, 'r') as myfile:
		clan_event = myfile.read()
		clan_event = clan_event.split(clan_name.lower() + ",",1)
		clan_event = clan_event[1].split("Event ends here!",1)
	return clan_event[0]
 
def open_external_file():
	with open(stored_clan_tuples, "r") as f:
		tmp_list_of_clan_server_tuples = []
		for i in f.readlines():
			tmp = i.split(",")
			tmp_list_of_clan_server_tuples.append((tmp[0],tmp[1][:-1]))
			
	return tmp_list_of_clan_server_tuples
	
def getActiveCompetitionRows():
	envision = "http://www.runeclan.com/clan/"+ clan_name +"/competitions"
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	count = 0
	i=0
	for tr in soup.find_all('table')[4:]:
		for row in soup.find_all('tr'):
			tds = tr.find_all('td')
			try:
				if tds[2+i].find('span').text == "active":
					count+=1
				i+=5
			except (AttributeError, IndexError):
				break
	return count
	
def getSkillsOfTheMonthNoPrint():
	envision = "http://www.runeclan.com/clan/"+ clan_name +"/competitions"
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	for tr1 in soup.find_all('table')[4:]:
		for row1 in soup.find_all('tr'):
			tds1 = tr1.find_all('td')
	return tds1
	
@client.event
async def getPlayersWhoCapped():
	clan_url = "https://docs.google.com/spreadsheets/d/1RYm1eVSq7op21I1xRcgqRMZMU4Ej1WVEz84QCTtBV3M/pubhtml?gid=187335414&single=true"
	page = urlopen(clan_url)
	soup = BeautifulSoup(page,"html.parser")
	listToPrint = ""
	i=0
	for tr in soup.find_all('table'):
		for row in soup.find_all('tr')[7:]:
			tds = row.find_all('td')
			if tds[10].text != "":
				listToPrint += tds[2].text + ", "
				i+=1
	capped_header = "A total of "+str(i)+ " people capped this week!\n"	
	await client.send_message(clientID,capped_header + listToPrint[:-2])
	page.close()
	
@client.event
async def getUserClanPoints():
	user = clan_points_user_input[12:]
	clan_url = "https://docs.google.com/spreadsheets/d/1RYm1eVSq7op21I1xRcgqRMZMU4Ej1WVEz84QCTtBV3M/pubhtml?gid=187335414&single=true"
	page = urlopen(clan_url)
	soup = BeautifulSoup(page,"html.parser")
	for tr in soup.find_all('table'):
		for row in soup.find_all('tr')[7:]:
			tds = row.find_all('td')
			if tds[2].text == user:
				await client.send_message(clientID,tds[2].text + " has "+ tds[3].text+ " clan points")
				return
	page.close()
	
@client.event
async def getUserRank():
	user = rank_user_input[5:]
	clan_url = "https://docs.google.com/spreadsheets/d/1RYm1eVSq7op21I1xRcgqRMZMU4Ej1WVEz84QCTtBV3M/pubhtml?gid=187335414&single=true"
	page = urlopen(clan_url)
	soup = BeautifulSoup(page,"html.parser")
	linkToRank = ["ranks/1.","ranks/2.","ranks/3.","ranks/4.","ranks/5.","ranks/6.","ranks/7.","ranks/8.","ranks/9.","ranks/10.","ranks/11.","ranks/12."]
	listOfRanks = ["Owner","Deputy Owner","Overseer", "Coordinator", "Organiser", "Admin", "General", "Captain", "Lieutenant","Sergeant","Corporal","Recruit"]
	i=0
	j=0
	for tr in soup.find_all('table'):
		for row in soup.find_all('tr')[7:]:
			tds = row.find_all('td')
			if tds[2].text == user:
				for link in soup.find_all(attrs={'class' : ['s5','s10','s23']})[j:]:
					for rank in linkToRank:
						if rank in link('div')[0]['style']:
							await client.send_message(clientID,listOfRanks[i])
							return
						i+=1
			j+=1
	page.close()	
	
@client.event
async def getClanEventLog():
	envision = "http://www.runeclan.com/clan/"+ clan_name
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	events = ""
	arrow = u"\u2192"
	clan_name_to_print = clan_name.replace("_", " ")
	events_to_print = 10
	events_counter = 0
	break_necessary = 0
	sent_message_nospaces = sent_message.replace(" ","")
	try:
		if sent_message_nospaces[6:9] == "top":
			if 0<int(sent_message_nospaces[9:])<41:
				events_to_print = int(sent_message_nospaces[9:])
			else:
				await client.send_message(clientID,"This feature is only valid for integer values between 1 and 40.")
				return			
	except: 
		await client.send_message(clientID,"This feature is only valid for integer values between 1 and 40.")
		return
	for names in soup.find_all(attrs={'class' : 'clan_event_box'})[0:events_to_print]:
			if " XP" in names.text:
				break_necessary += 1
				break
			else:
				events += names.text + "\n"
				events_counter += 1
	events = events.replace(".", " "+arrow+" ")
	events = events.replace("!", " "+arrow+" ")
	if break_necessary == 1:
		events  = "Only "+ str(events_counter) + " events are currently recorded on "+ clan_name_to_print+ "'s RuneClan page:\n" + events
	await client.send_message(clientID,events)
	page.close()
	
@client.event	
async def getClanAchievements():
	envision = "http://www.runeclan.com/clan/"+ clan_name
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	arrow = u"\u2192"
	achievements = ""
	clan_name_to_print = clan_name.replace("_", " ")
	achievements_start = 0
	total_achievements_displayed = 0
	achievements_to_print = 10
	sent_message_nospaces = sent_message.replace(" ","")
	try:
		if sent_message_nospaces[12:15] == "top":
			if 0<int(sent_message_nospaces[15:])<41:
				achievements_to_print = int(sent_message_nospaces[15:])
			else:
				await client.send_message(clientID,"This feature is only valid for integer values between 1 and 40.")
				return			
	except: 
		await client.send_message(clientID,"This feature is only valid for integer values between 1 and 40.")
		return
	for names in soup.find_all(attrs={'class' : 'clan_event_box'}):
		if " XP" not in names.text:
			achievements_start += 1
		else:
			break
	for names in soup.find_all(attrs={'class' : 'clan_event_box'})[achievements_start:achievements_start + achievements_to_print]:
		achievements += names.text + "\n"
		total_achievements_displayed += 1
	achievements = achievements.replace("XP","XP "+arrow + " ")
	
	max_skill_achievements = ["99 Attack", "99 Strength", "99 Defence", "99 Ranged", "99 Magic", \
	"99 Constitution", "99 Prayer", "99 Mining", "99 Herblore", "99 Smithing",\
	"99 Fletching", "99 Hunter", "99 Summoning", "99 Woodcutting", "99 Firemaking", \
	"99 Runecrafting", "99 Thieving", "99 Crafting", "99 Fishing", "99 Cooking",\
	"99 Agility", "99 Slayer", "99 Farming", "99 Divination", "99 Construction"  \
	"99 Invention", "120 Invention", "99 Dungeoneering", "120 Dungeoneering"]	
	
	for skill in max_skill_achievements:
		achievements = achievements.replace(skill,skill + " "+arrow + " ")
	if total_achievements_displayed != achievements_to_print:
		achievements = "Only "+ str(total_achievements_displayed) + " clan achievements are currently recorded on " + clan_name_to_print+"'s RuneClan page:\n" + achievements
	await client.send_message(clientID,achievements)
	page.close()
	
@client.event
async def getClanHiscores():
	envision = "http://www.runeclan.com/clan/"+ clan_name +"/hiscores"
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	clan_name_to_print = clan_name.replace("_", " ")
	arrow = u"\u2192"
	i=0	
	listToPrint = ""
	NewListToPrint = ""
	rows_to_print = "15"
	sent_message_nospaces = sent_message.replace(" ","")
	try:
		if sent_message_nospaces[8:11] == "top":
			if 0<int(sent_message_nospaces[11:])<26:
				rows_to_print = sent_message_nospaces[11:]
			else:
				await client.send_message(clientID,"This feature is only valid for integer values between 1 and 25.")
				return			
	except:
		await client.send_message(clientID,"This feature is only valid for integer values between 1 and 25.")
		return
	for tr in soup.find_all('table')[2:]:
		for row in soup.find_all('tr'):
			tds = tr.find_all('td')
			listToPrint =("Rank %s: %s %s Total Level: %s %s Total xp: %s xp\n" % \
						  (tds[0+i].text, tds[1+i].text, arrow, tds[2+i].text, arrow, tds[3+i].text))
			NewListToPrint += listToPrint
			if tds[0+i].text == rows_to_print:
				break
			else:
				i+=4
	hiscore_header = clan_name_to_print + "'s Overall Hiscores:\n\n"
	NewListToPrint = hiscore_header + NewListToPrint
	await client.send_message(clientID,NewListToPrint) 
	page.close()
	
@client.event
async def getKeyRanks():
	envision = "http://www.runeclan.com/clan/"+ clan_name
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	arrow = u"\u2192"
	listToPrint = ""
	NewListToPrint = ""
	for names in soup.find_all(attrs={'class' : 'clan_ownerbox'}):
		listToPrint= (names.text[2:]+ " "+arrow +" " + names('img')[0]['alt'] +"\n")
		NewListToPrint+=listToPrint
	await client.send_message(clientID,NewListToPrint) 
	page.close()
	
@client.event
async def getClanInfo():
	envision = "http://www.runeclan.com/clan/"+ clan_name
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	clan_name_to_print = clan_name.replace("_", " ") 
	listToPrint = clan_name_to_print + " - Clan Info:\n"
	for names in soup.find_all('span', attrs={'class' : 'clan_subtext'}):
		listToPrint += names.text +" "+ names.next_sibling + "\n" #next sibling prints out untagged text 
	await client.send_message(clientID,listToPrint)
	page.close()
		
@client.event	
async def getTodaysHiscores():
	envision = "http://www.runeclan.com/clan/"+ clan_name +"/xp-tracker"
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	arrow = u"\u2192"
	NewListToPrint = ""
	listToPrint = ""
	clan_name_to_print = clan_name.replace("_", " ")
	i=0	
	rows_to_print = "10"
	sent_message_nospaces = sent_message.replace(" ","")
	try:
		if sent_message_nospaces[14:17] == "top":
			if 0<int(sent_message_nospaces[17:])<41:
				rows_to_print = sent_message_nospaces[17:]
			else:
				await client.send_message(clientID,"This feature is only valid for integer values between 1 and 40.")
				return			
	except: 
		await client.send_message(clientID,"This feature is only valid for integer values between 1 and 40.")
		return
	
	for tr in soup.find_all('table')[3:]:
		for row in soup.find_all('tr'):
			tds = tr.find_all('td')
			listToPrint += "Rank %s: %s %s Total xp: %s xp\n" % \
				  (tds[5+i].text, tds[6+i].text, arrow, tds[7+i].text,)
			if tds[5+i].text == rows_to_print:
				break
			else:
				i+=5	
	todays_total_xp = clan_name_to_print + "'s Total Xp for Today: "+tds[2].text+ " xp\n\n"
	NewListToPrint = todays_total_xp + listToPrint
	await client.send_message(clientID,NewListToPrint)
	page.close()
		
@client.event			
async def getSkillsOfTheMonthTimeRemaining():
	envision = "http://www.runeclan.com/clan/"+ clan_name +"/competitions"
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")	
	no_of_rows = getActiveCompetitionRows()
	clan_name_to_print = clan_name.replace("_", " ") 
	i =0
	timeLeftPrint = ""
	if getActiveCompetitionRows() == 0:
		await client.send_message(clientID, clan_name_to_print + " has no active competitions at this time.")
	else:
		for tr in soup.find_all('table')[4:]:
			for row in soup.find_all('tr'):
				tds = tr.find_all('td')
		while no_of_rows > 0:
			if tds[2+i].find('span').text == "active":
				timeLeftPrint += "The currently active " + tds[1+i].text + " XP competition has "+ tds[4+i].text[:-6]+ " remaining!\n"
			no_of_rows-=1
			i+=5
		await client.send_message(clientID, timeLeftPrint)
		page.close()


@client.event
async def getSetEvent():
	clan_name_to_print = clan_name.replace("_", " ")
	try:		
		await client.send_message(clientID, get_custom_event())
	except:
		await client.send_message(clientID, clan_name_to_print + " has no custom events at this time.")
		
@client.event
async def setEvent():
	global event_set
	i=0
	if message_received.startswith("set next event:"):
		event_file = stored_next_clan_event
		event_set = message_received.replace("set next event:", "")
	if message_received.startswith("set upcoming events:"):
		event_file = stored_upcoming_clan_events
		event_set = message_received.replace("set upcoming events:", "")
	with open(event_file, 'r') as myfile:
		clan_event = myfile.read()
	if clan_name + "," not in clan_event:	
		with open(event_file, 'a') as outputfile:
			outputfile.writelines('{0},{1}{2}'.format(clan_name.lower(), event_set,"Event ends here!\n"))
	else: 
		file = open(event_file, "r")
		lines = file.readlines()
		file.close()
		file = open(event_file, "w")
		for line in lines:
			if not line.startswith(clan_name + ",") and i==0: 
				file.write(line)
			else:
				i=1
				if "Event ends here!" not in line:
					continue
				else:
					i=0
					continue					
		file.close()
		with open(event_file, 'a') as outputfile:
			outputfile.writelines('{0},{1}{2}'.format(clan_name.lower(), event_set,"Event ends here!\n"))
	await client.send_message(clientID, "These events have been set")

@client.event
async def getSkillsOfTheMonth():
	envision = "http://www.runeclan.com/clan/"+ clan_name +"/competitions"
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")	
	no_of_rows = getActiveCompetitionRows()
	clan_name_to_print = clan_name.replace("_", " ") 
	i =0
	skillsToPrint = ""
	if getActiveCompetitionRows() == 0:
		await client.send_message(clientID, clan_name_to_print + " has no active competitions at this time.")
	else:
		for tr in soup.find_all('table')[4:]:
			for row in soup.find_all('tr'):
				tds = tr.find_all('td')
		while no_of_rows > 0:
			if tds[2+i].find('span').text == "active":
				skillsToPrint += tds[1+i].text + ", "
			no_of_rows-=1
			i+=5
		await client.send_message(clientID, skillsToPrint[:-2])
		page.close()
	
@client.event
async def getSkillsOfTheMonthHiscores():
	envision = "http://www.runeclan.com/clan/"+ clan_name +"/competitions"
	page = urlopen(envision)
	soup = BeautifulSoup(page, 'html.parser')	
	table = soup.find_all('td', {'class': 'competition_td competition_name'})
	arrow = u"\u2192"
	tds1 = getSkillsOfTheMonthNoPrint()
	no_of_rows = getActiveCompetitionRows()
	clan_name_to_print = clan_name.replace("_", " ") 
	rows_to_print = "5"
	sent_message_nospaces = sent_message.replace(" ","")
	try:
		if sent_message_nospaces[12:15] == "top":
			if 0<int(sent_message_nospaces[15:])<11:
				rows_to_print = sent_message_nospaces[15:]
			else:
				await client.send_message(clientID,"This feature is only valid for integer values between 1 and 10.")
				return	
		if sent_message_nospaces[20:23] == "top" :
			if 0<int(sent_message_nospaces[23:])<11:
				rows_to_print = sent_message_nospaces[23:]
			else:
				await client.send_message(clientID,"This feature is only valid for integer values between 1 and 10.")
				return	
	except: 
		await client.send_message(clientID,"This feature is only valid for integer values between 1 and 10.")
		return
	listOfRanks = [None]*int(rows_to_print)*no_of_rows #array for the amount of ranks to print in the message
	listOfSkills = [None]*no_of_rows #array for the total amount of competitions
	SkillsToPrint = ""
	x=0 #iteration for player rank list
	k=0 #iteration for skill header
	l=0 #iteration for specific skill
	if getActiveCompetitionRows() == 0:
		await client.send_message(clientID, clan_name_to_print + " has no active competitions at this time.")
	else:	
		for n in table:
			for a in n.find_all('a', href=True):
				newLinkToSearch = "http://www.runeclan.com/clan/Envision/" + a['href']
				newPage = urlopen(newLinkToSearch)
				soup = BeautifulSoup(newPage, 'html.parser')
				i=0		
				for tr in soup.find_all('table')[3:]:
					while k < no_of_rows:
						listOfSkills[k] =  clan_name_to_print + "'s %s competition hiscores:\n" % (tds1[1+l].text)
						k+=1
						l+=5
					try:
						for row in soup.find_all('tr'):
							tds = tr.find_all('td')
							listOfRanks[x] = "Rank %s: %s %s Xp Gained: %s xp" % \
							(tds[0+i].text, tds[1+i].text, arrow, tds[2+i].text)
							if tds[0+i].text == rows_to_print:
								x+=1
								break
							else:
								i+=3
							x+=1
					except IndexError:
						break
						
		listToPrint = ""
		skillHeaders = 0
		skills = 0
		while skills<no_of_rows:
			listToPrint += listOfSkills[skillHeaders]
			for row in listOfRanks[skills*int(rows_to_print):(skills*int(rows_to_print)) + int(rows_to_print)]:
				listToPrint += str(row) + "\n"
			listToPrint += "\n"
			skillHeaders+=1
			skills+=1
		try:
			await client.send_message(clientID,listToPrint)
		except:
			await client.send_message(clientID,"Character limit exceeded. Please reduce the amount of ranks you wish to search for.")
		page.close()
		newPage.close()
	
@client.event
async def getBotsCommands():
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
	w=0
	list_of_commands = ["sotm", "sotm hiscores", "hiscores", "achievements", "events", \
	"sotm time", "todays hiscores", "key ranks", "clan info", "competitions", \
	"competitions hiscores", "competitions time" ]
	
	clientID = message.channel
	sent_message = message.content.lower().replace("'","")
	
	if message.content == "help!":
		await getBotsCommands()
	
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
			await client.send_message(clientID, "This bot is now searching " +clan_name_to_type+ "'s RuneClan page.")
	
	for server, name_of_clan in list_of_clan_server_tuples:
		if server == str(message.server):
			clan_name = name_of_clan
			if sent_message == "hiscores":
				await getClanHiscores()
			if sent_message.startswith("hiscores top"):
				await getClanHiscores()
			elif sent_message == "events":
				await getClanEventLog()
			elif sent_message.startswith("events top"):
				await getClanEventLog()
			elif sent_message == "achievements":
				await getClanAchievements()
			elif sent_message.startswith("achievements top"):
				await getClanAchievements()
			elif sent_message == "key ranks":
				await getKeyRanks()
			elif sent_message == "clan info":
				await getClanInfo()
			elif sent_message == "sotm" or sent_message == "competitions":
				await getSkillsOfTheMonth()
			elif sent_message == "sotm hiscores" or sent_message == "competitions hiscores":
				await getSkillsOfTheMonthHiscores()
			elif sent_message.startswith("sotm hiscores top") or sent_message.startswith("competitions hiscores top"):
				await getSkillsOfTheMonthHiscores()
			elif sent_message == "todays hiscores":
				await getTodaysHiscores()
			elif sent_message.startswith("todays hiscores top"):
				await getTodaysHiscores()
			elif sent_message.startswith("sotm time") or sent_message.startswith("competitions time"):
				await getSkillsOfTheMonthTimeRemaining()
			elif sent_message == "next event":
				message_received = message.content
				await getSetEvent()
			elif sent_message == "upcoming events":
				message_received = message.content
				await getSetEvent()
			elif sent_message.startswith("set next event:"):
				message_received = message.content
				await setEvent()
			elif sent_message.startswith("set upcoming events:"):
				message_received = message.content
				await setEvent()
			if name_of_clan.lower() == 'envision':
				if sent_message == ("capped this week"):
					await getPlayersWhoCapped()
				elif message.content.startswith("rank"):
					global rank_user_input
					rank_user_input = message.content
					await getUserRank()
				elif message.content.startswith("clan points"):
					global clan_points_user_input
					clan_points_user_input = message.content
					await getUserClanPoints()
			return
		
	for command in list_of_commands:
		if sent_message == list_of_commands[w]:
			await client.send_message(clientID, "This command isn't recognized. Please ensure you have used the 'setclan' command for this server.")
			break
		else:
			w+=1
			
client.run('MjkyNDU4Mzk1MjgwMDgwOTA3.C64V7A.S6UuOWydAX1E5Eret6pCq4YcdOo')