import re
from os import path

from helper_methods import soup_session


CLAN_SERVER_MAPPING_FILE = "clan_server_mapping.txt"


def open_clan_server_mapping_file():
    with open(CLAN_SERVER_MAPPING_FILE, "r") as file:
        tmp_list_of_clan_server_tuples = []
        for line in file.readlines():
            line = line.split(",")
            tmp_list_of_clan_server_tuples.append((line[0], line[1][:-1]))

    return tmp_list_of_clan_server_tuples


def test_if_clan_exists(clan_name):

    soup = soup_session(clan_name)

    list_to_print = ""
    for names in soup.find_all('span', attrs={'class': 'clan_subtext'}):
        list_to_print += names.text + " " + names.next_sibling + "\n"  # next sibling prints out untagged text

    return list_to_print


def remove_clan(server, clan_name, clan_server_tuples_list):

    discord_server_id = str(server.id)

    if test_if_clan_exists(clan_name) and discord_server_id in [clan_serve_tuple[0] for clan_serve_tuple in clan_server_tuples_list]:
        file = open(CLAN_SERVER_MAPPING_FILE, "r")
        lines = file.readlines()
        file.close()
        file = open(CLAN_SERVER_MAPPING_FILE, "w")
        for line in lines:
            if not line.startswith(discord_server_id + ","):
                file.write(line)
        file.close()

        # Removes clan from the !setclan command from the clan server tuple list if it was already there and associates the new clan to the server
        clan_server_tuples_list = [(server_id, name) for (server_id, name) in clan_server_tuples_list if server_id != discord_server_id]

        return f"This bot is no longer searching {clan_name.replace('_', ' ')}'s RuneClan page.", clan_server_tuples_list

    return "The clan you are searching does not exist or is not being tracked by your Discord server. Please ensure the clans name is spelled correctly.", clan_server_tuples_list


def set_clan(server, clan_name, clan_server_tuples_list):

    discord_server_id = str(server.id)

    if test_if_clan_exists(clan_name):
        if discord_server_id not in [clan_serve_tuple[0] for clan_serve_tuple in clan_server_tuples_list]:
            clan_server_tuples_list.append((discord_server_id, clan_name))
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
            clan_server_tuples_list = [(server_id, name) for (server_id, name) in clan_server_tuples_list if server_id != discord_server_id]
            clan_server_tuples_list.append((discord_server_id, clan_name))

            with open(CLAN_SERVER_MAPPING_FILE, 'a') as output_file:
                output_file.write(f'{discord_server_id},{clan_name}\n')

        return f"This bot is now searching {clan_name.replace('_', ' ')}'s RuneClan page.", clan_server_tuples_list

    return "The clan you are searching does not exist or is not being tracked by RuneClan. Please ensure the clans name is spelled correctly.", clan_server_tuples_list


def clan_server_management(server, sent_message, list_of_clan_server_tuples):

    # Creates clan server mapping file if it doesn't yet exist.
    if not path.exists(CLAN_SERVER_MAPPING_FILE):
        with open(CLAN_SERVER_MAPPING_FILE, 'w'):
            pass

    if not server:
        return 'This bot is not meant to work in private chat. Please enter a command on a channel of a server that this bot has joined. Use the command "!help" for more info.', list_of_clan_server_tuples

    if not list_of_clan_server_tuples:
        list_of_clan_server_tuples = open_clan_server_mapping_file()

    if sent_message.lower().startswith("!setclan "):
        clan_name = re.split("!setclan", sent_message, flags=re.IGNORECASE)[1].strip().replace(" ", "_")
        return set_clan(server, clan_name, list_of_clan_server_tuples)

    elif sent_message.lower().startswith("!removeclan "):
        clan_name = re.split("!removeclan", sent_message, flags=re.IGNORECASE)[1].strip().replace(" ", "_")
        return remove_clan(server, clan_name, list_of_clan_server_tuples)

    return "", list_of_clan_server_tuples
