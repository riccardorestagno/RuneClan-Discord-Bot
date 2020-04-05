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


Usage
=======

Add RuneClan bot to your discord server: https://discordapp.com/oauth2/authorize?client_id=292458395280080907&scope=bot&permissions=0

Sample usage: http://imgur.com/a/1ouSX


List of Commands
=================

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


Things to note:
  1. The "top [x]" feature is optional, and the default value is used if not entered.
  2. This bot is not meant to work in private chat.

  
Author
==============
Rick Restagno
