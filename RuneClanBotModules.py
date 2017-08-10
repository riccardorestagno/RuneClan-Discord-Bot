from urllib.request import urlopen
from bs4 import BeautifulSoup
import math
botRequest = input()
clan_name = 'Envision'
def getPlayersWhoCapped():
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
	print(listToPrint[:-2])
			
def getUserClanPoints():
	user = botRequest[12:]
	clan_url = "https://docs.google.com/spreadsheets/d/1RYm1eVSq7op21I1xRcgqRMZMU4Ej1WVEz84QCTtBV3M/pubhtml?gid=187335414&single=true"
	page = urlopen(clan_url)
	soup = BeautifulSoup(page,"html.parser")
	for tr in soup.find_all('table'):
		for row in soup.find_all('tr')[7:]:
			tds = row.find_all('td')
			if tds[2].text == user:
				print(tds[2].text+ " has "+ tds[3].text+ " clan points")
				
def getUserRank():
	user = botRequest[5:]
	clan_url = "https://docs.google.com/spreadsheets/d/1RYm1eVSq7op21I1xRcgqRMZMU4Ej1WVEz84QCTtBV3M/pubhtml?gid=187335414&single=true"
	page = urlopen(clan_url)
	soup = BeautifulSoup(page,"html.parser")
	linkToRank = ["ranks/1.","ranks/2.","ranks/3.","ranks/4.","ranks/5.","ranks/6."\
	,"ranks/7.","ranks/8.","ranks/9.","ranks/10.","ranks/11.","ranks/12."]
	listOfRanks = ["Owner","Deputy Owner","Overseer", "Coordinator", "Organiser", "Admin",\
	"General", "Captain", "Lieutenant","Sergeant","Corporal","Recruit"]
	i=0
	j=0
	for tr in soup.find_all('table'):
		for row in soup.find_all('tr')[7:]:
			tds = row.find_all('td')
			if tds[2].text == user:
				for link in soup.find_all(attrs={'class' : ['s5','s10']})[j:]:
					for rank in linkToRank:
						if rank in link('div')[0]['style']:
							print(listOfRanks[i])
							return
						i+=1
			j+=1
			
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
				#print(tds[2+i].find('span').text)
				if tds[2+i].find('span').text == "active":
					count+=1
				i+=5
			except (IndexError, AttributeError):
				break
			
	print(count)
	
def getClanEventLog():
	envision = "http://www.runeclan.com/clan/" + clan_name
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	events = ""
	arrow = u"\u2192"
	for names in soup.find_all(attrs={'class' : 'clan_event_box'})[0:39]:
			events += names.text + "\n"
	events = events.replace(".", " "+arrow+" ")
	events = events.replace("!", " "+arrow+" ")
	print(events)
	
def getClanAchievements():
	envision = "http://www.runeclan.com/clan/" + clan_name
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	arrow = u"\u2192"
	achievements = ""
	for names in soup.find_all(attrs={'class' : 'clan_event_box'})[40:79]:
		#for dates in soup.find_all(attrs={'class' : 'clan_event_box_date'}):
		achievements += names.text + "\n"
	achievements = achievements.replace("XP","XP "+arrow + " ")
	max_skill_achievements = ["99 Attack", "99 Strength", "99 Defence", "99 Ranged", "99 Magic", \
	"99 Constitution", "99 Prayer", "99 Mining", "99 Herblore", "99 Smithing",\
	"99 Fletching", "99 Hunter", "99 Summoning", "99 Woodcutting", "99 Firemaking", \
	"99 Runecrafting", "99 Thieving", "99 Crafting", "99 Fishing", "99 Cooking",\
	"99 Agility", "99 Slayer", "99 Farming", "99 Divination", "99 Construction"  \
	"99 Invention", "120 Invention", "99 Dungeoneering", "120 Dungeoneering"]	
	for skill in max_skill_achievements:
		achievements = achievements.replace(skill,skill + " "+arrow + " ")
	print(achievements)
		
	
def getTodaysHiscores():
	envision = "http://www.runeclan.com/clan/" + clan_name + "/xp-tracker"
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	i=0	
	for tr in soup.find_all('table')[3:]:
		for row in soup.find_all('tr'):
			tds = tr.find_all('td')
			print ("Rank %s: %s, Total xp: %s" % \
				  (tds[5+i].text, tds[6+i].text, tds[7+i].text,))
			if tds[5+i].text == "10":
				break
			else:
				i+=5
		print( "Clan Total Xp for Today: "+tds[2].text)		


def getKeyRanks():
	envision = "http://www.runeclan.com/clan/" + clan_name
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	for names in soup.find_all(attrs={'class' : 'clan_ownerbox'}):
		print (names.text[2:]+ ": " + names('img')[0]['alt'])

def getClanInfo():
	envision = "http://www.runeclan.com/clan/" + clan_name
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	list = [None]*6
	x=0
	for names in soup.find_all('span', attrs={'class' : 'clan_subtext'}):
		list[x] = (names.text, names.next_sibling) #next sibling prints out untagged text 
		x+=1
	listToPrint = ""
	for row in list:
		listToPrint += str(row) + "\n"
	listToPrint = listToPrint[:-1]
	print(listToPrint) # USE THIS METHOD FOR ALL MULTILINE PRINTS


def getSkillsOfTheMonthTimeRemaining():
	envision = "http://www.runeclan.com/clan/" + clan_name + "/competitions"
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")	
	i=5
	for tr in soup.find_all('table')[4:]:
		for row in soup.find_all('tr'):
			tds = tr.find_all('td')
			print (tds[4].text)
			break
			
def getSkillsOfTheMonthNoPrint():
	envision = "http://www.runeclan.com/clan/" + clan_name + "/competitions"
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")	
	
	for tr1 in soup.find_all('table')[4:]:
		for row1 in soup.find_all('tr'):
			tds1 = tr1.find_all('td')
	return tds1
	
def getSkillsOfTheMonth():
	envision = "http://www.runeclan.com/clan/" + clan_name + "/competitions"
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")	
	no_of_rows = getActiveCompetitionRows()
	i =0
	skillsToPrint = ""
	for tr in soup.find_all('table')[4:]:
		for row in soup.find_all('tr'):
			tds = tr.find_all('td')
	while no_of_rows > 0:
		skillsToPrint += tds[1+i].text + ", "
		no_of_rows -= 1
		i+=5
	print(skillsToPrint[:-2])
	
def getSkillsOfTheMonthHiscores():
	envision = "http://www.runeclan.com/clan/" + clan_name + "/competitions"
	page = urlopen(envision)
	soup = BeautifulSoup(page, 'html.parser')	
	table = soup.find_all('td', {'class': 'competition_td competition_name'})
	tds1 = getSkillsOfTheMonthNoPrint()
	no_of_rows = getActiveCompetitionRows()
	listOfRanks = [None]*5*no_of_rows
	listOfSkills = [None]*no_of_rows
	SkillsToPrint = ""
	x=0 #iteration for player rank list
	k=0 #iteration for skill header
	l=0 #iteration for specific skill
	for n in table:
		for a in n.find_all('a', href=True):
			newLinkToSearch = "http://www.runeclan.com/clan/Envision/" + a['href']
			newPage = urlopen(newLinkToSearch)
			soup = BeautifulSoup(newPage, 'html.parser')
			i=0		
			for tr in soup.find_all('table')[3:]:
				while k < no_of_rows:
					print ("hi")
					print (tds1[1+l].text)
					listOfSkills[k] =  "Clan %s Xp hiscores for this month: \n" % (tds1[1+l].text)
					k+=1
					l+=5
				for row in soup.find_all('tr'):
					tds = tr.find_all('td')
					print (tds[0+i].text)
					print(tds[1+i].text)
					listOfRanks[x] = "Rank %s: %s Xp Gained: %s xp" % \
					(tds[0+i].text, tds[1+i].text, tds[2+i].text)
					if tds[0+i].text == "5":
						x+=1
						break
					else:
						i+=3
					x+=1
	listToPrint = ""
	skillHeaders = 0
	skills = 0
	while skills<no_of_rows:
		listToPrint += listOfSkills[skillHeaders]
		for row in listOfRanks[skills*5:(skills*5) + 5]:
			listToPrint += str(row) + "\n"
		listToPrint += "\n"
		skillHeaders+=1
		skills+=1

	print(listToPrint) # USE THIS METHOD FOR ALL MULTILINE PRINTS
	page.close()
	newPage.close()	
def getClanInfo():
	envision = "http://www.runeclan.com/clan/"+ clan_name
	page = urlopen(envision)
	soup = BeautifulSoup(page,"html.parser")
	listToPrint = clan_name + " Clan Info: \n"
	for names in soup.find_all('span', attrs={'class' : 'clan_subtext'}):
		listToPrint += names.text +" "+ names.next_sibling + "\n" #next sibling prints out untagged text 
	print(listToPrint) # USE THIS METHOD FOR ALL MULTILINE PRINTS
	page.close()
	
def getBotsCommands():
	print(
'''RuneClan discord bot commands:
"help or "how": activates everything that you're seeing right now
"hiscores": prints clans overall hiscores (top 15)
"todays hiscores": prints clans overall hiscores for today 
"sotm": prints skills of the month (only works with 2)
"sotm hiscores": prints the hiscores   
"sotm time": tell you how much time is left in the skills of the month competition
"clan info": prints the clan info listed on runeclan 
"key ranks": prints the key ranks in envision''')

while botRequest != "end":
	if botRequest == "hiscores":
		getClanHiscores()
	elif botRequest == "key ranks":
		getKeyRanks()
	elif botRequest == "clan info":
		getClanInfo()
	elif botRequest == "sotm":
		getSkillsOfTheMonth()
	elif botRequest == "sotm h":
		getSkillsOfTheMonthHiscores()
	elif botRequest == "todays hiscores":
		getTodaysHiscores()
	elif botRequest == "a":
		getClanAchievements()
	elif botRequest == "e":
		getClanEventLog()
	elif botRequest.startswith("sotm time"):
		getSkillsOfTheMonthTimeRemaining()
	elif botRequest.startswith("help") or botRequest.startswith("how"):
		getBotsCommands()
	elif botRequest == "r":	
		getNoOfSOTMRows()
	elif botRequest == "cap":	
		getPlayersWhoCapped()
	elif botRequest.startswith("rank"):	
		getUserRank()
	elif botRequest.startswith("clan points"):	
		getUserClanPoints()
	elif botRequest == "rows":	
		getActiveCompetitionRows()
	botRequest = input()



