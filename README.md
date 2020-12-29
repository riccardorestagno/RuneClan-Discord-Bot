RuneClan Discord Bot
=====================

Description
===========

A discord bot that uses BeautifulSoup to gather clan information from https://www.runeclan.com and posts the requested information 
on the chat channel that the command was sent to.


Dependencies
=================
Supported Python versions: 3.6.0+ 

- BeautifulSoup4 (https://www.crummy.com/software/BeautifulSoup/)
- discord.py (https://pypi.python.org/pypi/discord.py/) 


Usage
=======

Add RuneClan bot to your discord server: https://discordapp.com/oauth2/authorize?client_id=292458395280080907&scope=bot&permissions=0

Sample usage: http://imgur.com/a/1ouSX


List of Commands
=================

`!help`: Prints the list of commands below. 

&nbsp;

`!setclan [Clan Name]`: Sets the clan you wish to search for on runeclan.

`!removeclan`: Removes the clan association from the Discord server.

&nbsp;

`!hiscores top [x]`: Prints clans overall hiscores. (default: top 15)

`!today's hiscores top [x]`: Prints clans overall hiscores for today. (default: top 10)

`!competitions`: Lists the currently active competitions on RuneClan.

`!competitions hiscores top [x]`: Shows the hiscores for all active clan competitions. (default: top 5 for each skill) 

`!competitions time`: Tell you how much time is remaining in the active competitions listed on RuneClan.

`!clan info`: Prints the clan info listed on RuneClan .

`!key ranks`: Lists the clans key ranks.

`!events top [x]`: Prints the clan event log as seen on RuneClan. (default: 10 most recent)

`!achievements top [x]`: Prints the clan achievement log as seen on RuneClan. (default: 10 most recent)

&nbsp;
#### Things to note:
  1. The `top [x]` feature is optional, and the default value is used if not entered.
  2. This bot does not work in private chat.

  
Author
==============
Rick Restagno
