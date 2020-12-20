import re
import requests
from bs4 import BeautifulSoup


def soup_session(url):
    """BeautifulSoup session."""
    session = requests.Session()
    page = session.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def test_if_clan_exists(website, clan_name):

    soup = soup_session(website + clan_name)

    list_to_print = ""
    for names in soup.find_all('span', attrs={'class': 'clan_subtext'}):
        list_to_print += names.text + " " + names.next_sibling + "\n"  # next sibling prints out untagged text

    return list_to_print


def open_external_file(stored_clan_tuples):
    with open(stored_clan_tuples, "r") as file:
        tmp_list_of_clan_server_tuples = []
        for line in file.readlines():
            line = line.split(",")
            tmp_list_of_clan_server_tuples.append((line[0], line[1][:-1]))

    return tmp_list_of_clan_server_tuples


def get_active_competition_rows(website, clan_name):

    soup = soup_session(website + clan_name + "/competitions")

    row_count = 0
    table_cell = 0
    for table in soup.find_all('table')[4:]:
        for _ in soup.find_all('tr'):
            row = table.find_all('td')
            try:
                if row[table_cell+2].find('span').text == "active":
                    row_count += 1
                table_cell += 5
            except (AttributeError, IndexError):
                break

    return row_count


def get_skills_in_clan_competition(website, clan_name):

    soup = soup_session(website + clan_name + "/competitions")

    for table in soup.find_all('table')[4:]:
        for _ in soup.find_all('tr'):
            return table.find_all('td')

    return []


def get_requested_list_count(message, max_list, default):

    try:
        if " top" in message.lower():
            if not re.split(" top", message, flags=re.IGNORECASE)[1].strip().isdigit() or not 1 <= int(re.split(" top", message, flags=re.IGNORECASE)[1].strip()) <= max_list:
                return 0, f"This feature is only valid for integer values between 1 and {max_list}."
            else:
                return int(re.split(" top", message, flags=re.IGNORECASE)[1].strip()), ""
    except:
        return 0, f"This feature is only valid for integer values between 1 and {max_list}."

    return default, ""
