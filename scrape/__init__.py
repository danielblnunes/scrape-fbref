import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from alive_progress import alive_bar


def get_urls_per_team(base_url):

    page = requests.get(base_url)
    soup = BeautifulSoup(page.text, 'lxml')
    urls = {}

    table_standings = soup.find(
        'table', {"id": re.compile('^results.*overall$')})

    rows = table_standings.tbody.find_all('tr')

    for i in range(len(rows)):
        team = rows[i].find("a").text
        urls[team] = rows[i].find("a").get("href")

    return urls


def parse_table(table, team=None):

    data = {}
    rows = table.find_all('tr')

    for tr in range(0, len(rows)):
        if (rows[tr].th.get('scope') == 'col') | (rows[tr].th.get('scope') == None):
            continue
        for th in rows[tr]:
            if th.get('data-stat') not in data:
                data[th.get('data-stat')] = [th.text]
            else:
                data[th.get('data-stat')].append(th.text)
    df = pd.DataFrame(data)

    if team != None:
        df['team'] = team

    return df


def scrape_league_stats(url):

    stats = {}
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    tables = soup.findAll('table')

    length_tables = len(tables)
    with alive_bar(length_tables) as bar:
        for table in tables:
            table_id = re.sub(r'(stats_)|(squads_)|_\d+$', "", table['id'])
            if table_id not in stats:
                stats[table_id] = [parse_table(table)]
            else:
                stats[table_id].append(parse_table(table))
            bar()

    for stat in stats.keys():
        stats[stat] = pd.concat(stats[stat])

    return stats


def scrape_player_stats(urls):

    base_url = "https://fbref.com/"
    stats = {}

    length_urls = len(urls.keys())

    for team in urls.keys():
        url = base_url+urls[team]
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
        tables = soup.findAll('table')

        for table in tables:
            table_id = re.sub(
                r'(stats_)|(squads_)|_\d+$', "", table['id'])
            if table_id not in stats:
                stats[table_id] = [parse_table(table, team)]
            else:
                stats[table_id].append(parse_table(table, team))

    for stat in stats.keys():
        stats[stat] = pd.concat(stats[stat])

    return stats
