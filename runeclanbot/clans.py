import csv
import re
from os import getcwd, makedirs, path

from helper_methods import soup_session


CLAN_SERVER_MAPPING_FILE = getcwd() + "/clanfile/clan_server_mapping.csv"


def clan_exists(clan_name):
    """
    Checks if clan name entered can be found on https://www.runeclan.com.
    Returns True if clan exists. Returns False otherwise.
    """

    soup = soup_session(clan_name)
    if soup.find('span', attrs={'class': 'clan_subtext'}):
        return True

    return False


def set_clan_server_file(clan_server_dict):
    """Converts dictionary to a csv formatted text string and writes contents to the clan-server mapping file."""

    clan_server_text_string = ""

    for server_id in clan_server_dict:
        clan_server_text_string += f"{server_id},{clan_server_dict[server_id]}\n"

    with open(CLAN_SERVER_MAPPING_FILE, 'w') as file:
        file.write(clan_server_text_string)


def get_clan_server_dict():
    """Reads clan server mapping file and returns its contents as a dictionary."""

    with open(CLAN_SERVER_MAPPING_FILE) as file:
        clan_server_dict = dict(filter(None, csv.reader(file)))

    return clan_server_dict


def remove_clan(discord_server_id):
    """
    Removes the row in the clan-server mapping csv file containing the Discord server ID passed in this method.
    Returns message indicating the bot is no longer being used on this server.
    """

    clan_server_dict = get_clan_server_dict()
    clan_server_dict.pop(discord_server_id, None)
    set_clan_server_file(clan_server_dict)

    return "RuneClanBot is no longer being used on this server."


def set_clan(discord_server_id, clan_name):
    """
    Adds a row to the clan-server mapping csv file containing the Discord server ID and clan name to
    associate to this Discord server, if the clan can be found on https://www.runeclan.com.

    Overwrites previously made clan-server associations on this Discord server, if any.

    Returns a message which indicates if the correct mapping has been made, or if the clan cannot be found.
    """

    if clan_exists(clan_name):
        clan_server_dict = get_clan_server_dict()
        clan_server_dict[discord_server_id] = clan_name
        set_clan_server_file(clan_server_dict)

        return f"This bot is now searching {clan_name.replace('_', ' ')}'s RuneClan page."

    return "The clan you are searching does not exist or is not being tracked by RuneClan. Please ensure the clans name is spelled correctly."


def clan_server_management(discord_server_id, sent_message):
    """Manages the clan server mapping file based on the command the user entered."""

    # Creates clan server mapping directory/file if it doesn't yet exist.
    if not path.exists(CLAN_SERVER_MAPPING_FILE):
        # Creates directory.
        makedirs(CLAN_SERVER_MAPPING_FILE.rsplit('/', 1)[0] + '/', exist_ok=True)

        # Creates clan server mapping file at specified location.

        with open(CLAN_SERVER_MAPPING_FILE, 'w'):
            pass

    if sent_message.lower().startswith("!setclan "):
        clan_name = re.split("!setclan", sent_message, flags=re.IGNORECASE)[1].strip().replace(" ", "_")
        return set_clan(discord_server_id, clan_name)

    elif sent_message.lower() == "!removeclan":
        return remove_clan(discord_server_id)
