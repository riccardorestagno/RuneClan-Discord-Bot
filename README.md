RuneClan Discord Bot
=====================

Description
===========

A discord bot that uses BeautifulSoup to gather clan information from runeclan.com and posts the requested information 
on the chat channel that the command was sent to.


Dependencies
=================
Supported Python versions: 3.6.0+ 

discord.py (https://pypi.python.org/pypi/discord.py/) 
BeautifulSoup (https://www.crummy.com/software/BeautifulSoup/)
urllib.request (included in Python 3.6+ default library)
asyncio (included in Python 3.6+ default library)
itertools (included in Python 3.6+ default library)


List of Commands
=================

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

  
Author
==============
Rick Restagno