import pandas as pd
import re
from os import getcwd, makedirs, path

from helper_methods import soup_session

CLAN_SERVER_MAPPING_FILE = getcwd() + "/clanfile/clan_server_mapping.csv"
SERVER_ID_COLUMN_NAME = "ServerId"
CLAN_NAME_COLUMN_NAME = "ClanName"


def get_clan_server_dict():
    """Reads clan server mapping file and returns its contents as a dictionary."""

    df = pd.read_csv(CLAN_SERVER_MAPPING_FILE)
    return dict(zip(df[SERVER_ID_COLUMN_NAME], df[CLAN_NAME_COLUMN_NAME]))


def clan_exists(clan_name):
    """
    Checks if clan name entered can be found on https://www.runeclan.com.
    Returns True if clan exists. Returns False otherwise.
    """

    soup = soup_session(clan_name)
    if soup.find('span', attrs={'class': 'clan_subtext'}):
        return True

    return False


def remove_clan(discord_server_id):
    """
    Removes the row in the clan-server mapping csv file containing the Discord server ID passed in this method.
    Returns message indicating the bot is no longer being used on this server.
    """

    df = pd.read_csv(CLAN_SERVER_MAPPING_FILE)
    df.drop(df[df[SERVER_ID_COLUMN_NAME] == discord_server_id].index, inplace=True, errors='ignore')
    df.to_csv(CLAN_SERVER_MAPPING_FILE, index=False)

    return "RuneClanBot is no longer being used on this server."


def set_clan(discord_server_id, clan_name):
    """
    Adds a row to the clan-server mapping csv file containing the Discord server ID and clan name to
    associate to this Discord server, if the clan can be found on https://www.runeclan.com.

    Removes previously made clan-server associations on this Discord server, if any.

    Returns a message which indicates if the correct mapping has been made, or if the clan cannot be found.
    """

    if clan_exists(clan_name):
        data = [{SERVER_ID_COLUMN_NAME: discord_server_id, CLAN_NAME_COLUMN_NAME: clan_name}]

        df = pd.read_csv(CLAN_SERVER_MAPPING_FILE)
        df.drop(df[df[SERVER_ID_COLUMN_NAME] == discord_server_id].index, inplace=True, errors='ignore')
        df = df.append(data, ignore_index=True, sort=False)
        df.to_csv(CLAN_SERVER_MAPPING_FILE, index=False)

        return f"This bot is now searching {clan_name.replace('_', ' ')}'s RuneClan page."

    return "The clan you are searching does not exist or is not being tracked by RuneClan. Please ensure the clans name is spelled correctly."


def clan_server_management(server, sent_message):
    """Manages the clan server mapping file based on the command the user entered."""

    # Creates clan server mapping directory/file if it doesn't yet exist.
    if not path.exists(CLAN_SERVER_MAPPING_FILE):
        # Creates directory.
        makedirs(CLAN_SERVER_MAPPING_FILE.rsplit('/', 1)[0] + '/', exist_ok=True)

        # Creates clan server mapping file at specified location.

        with open(CLAN_SERVER_MAPPING_FILE, 'w') as f:
            f.write(f"{SERVER_ID_COLUMN_NAME},{CLAN_NAME_COLUMN_NAME}\n")

    if sent_message.lower().startswith("!setclan "):
        clan_name = re.split("!setclan", sent_message, flags=re.IGNORECASE)[1].strip().replace(" ", "_")
        return set_clan(server.id, clan_name)

    elif sent_message.lower() == "!removeclan":
        return remove_clan(server.id)
