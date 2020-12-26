import re
from os import getcwd, mkdir, path

from helper_methods import soup_session


CLAN_SERVER_MAPPING_FILE = getcwd() + "clanfile/clan_server_mapping.txt"


def get_clan_server_mapping():
    with open(CLAN_SERVER_MAPPING_FILE, "r") as file:
        clan_server_tuples = []
        for line in file.readlines():
            line = line.split(",")
            clan_server_tuples.append((line[0], line[1][:-1]))

    return clan_server_tuples


def clan_exists(clan_name):
    """
    Checks if clan name entered can be found on runeclan.com.
    Returns True if clan exists. Returns False otherwise.
    """

    soup = soup_session(clan_name)
    if soup.find('span', attrs={'class': 'clan_subtext'}):
        return True

    return False


def remove_clan(server, clan_name, clan_server_tuples):

    discord_server_id = str(server.id)

    if clan_exists(clan_name) and discord_server_id in [clan_serve_tuple[0] for clan_serve_tuple in clan_server_tuples]:
        file = open(CLAN_SERVER_MAPPING_FILE, "r")
        lines = file.readlines()
        file.close()
        file = open(CLAN_SERVER_MAPPING_FILE, "w")
        for line in lines:
            if not line.startswith(discord_server_id + ","):
                file.write(line)
        file.close()

        # Removes clan from the !setclan command from the clan server tuple list if it was already there and associates the new clan to the server
        clan_server_tuples = [(server_id, name) for (server_id, name) in clan_server_tuples if server_id != discord_server_id]

        return f"This bot is no longer searching {clan_name.replace('_', ' ')}'s RuneClan page.", clan_server_tuples

    return "The clan you are searching does not exist or is not being tracked by your Discord server. Please ensure the clans name is spelled correctly.", clan_server_tuples


def set_clan(server, clan_name, clan_server_tuples):

    discord_server_id = str(server.id)

    if clan_exists(clan_name):
        if discord_server_id not in [clan_serve_tuple[0] for clan_serve_tuple in clan_server_tuples]:
            clan_server_tuples.append((discord_server_id, clan_name))
            with open(CLAN_SERVER_MAPPING_FILE, 'a') as output_file:
                output_file.write(f'{discord_server_id},{clan_name}\n')
        else:
            file = open(CLAN_SERVER_MAPPING_FILE, "r")
            lines = file.readlines()
            file.close()
            file = open(CLAN_SERVER_MAPPING_FILE, "w")
            for line in lines:
                if not line.startswith(discord_server_id + ","):
                    file.write(line)
            file.close()

            # Removes clan from the !setclan command from the clan server tuple list if it was already there and associates the new clan to the server
            clan_server_tuples = [(server_id, name) for (server_id, name) in clan_server_tuples if server_id != discord_server_id]
            clan_server_tuples.append((discord_server_id, clan_name))

            with open(CLAN_SERVER_MAPPING_FILE, 'a') as output_file:
                output_file.write(f'{discord_server_id},{clan_name}\n')

        return f"This bot is now searching {clan_name.replace('_', ' ')}'s RuneClan page.", clan_server_tuples

    return "The clan you are searching does not exist or is not being tracked by RuneClan. Please ensure the clans name is spelled correctly.", clan_server_tuples


def clan_server_management(server, sent_message, clan_server_tuples):

    # Creates clan server mapping directory/file if it doesn't yet exist.
    if not path.isdir(CLAN_SERVER_MAPPING_FILE.rsplit('/', 1)[0] + '/'):
        # Creates directory.
        mkdir(CLAN_SERVER_MAPPING_FILE.rsplit('/', 1)[0] + '/')

        # Creates clan server mapping file at specified location.
        with open(CLAN_SERVER_MAPPING_FILE, 'w'):
            pass

    if not server:
        return 'This bot is not meant to work in private chat. Please enter a command on a channel of a server that this bot has joined. Use the command "!help" for more info.', clan_server_tuples

    if not clan_server_tuples:
        clan_server_tuples = get_clan_server_mapping()

    if sent_message.lower().startswith("!setclan "):
        clan_name = re.split("!setclan", sent_message, flags=re.IGNORECASE)[1].strip().replace(" ", "_")
        return set_clan(server, clan_name, clan_server_tuples)

    elif sent_message.lower().startswith("!removeclan "):
        clan_name = re.split("!removeclan", sent_message, flags=re.IGNORECASE)[1].strip().replace(" ", "_")
        return remove_clan(server, clan_name, clan_server_tuples)

    return "", clan_server_tuples
