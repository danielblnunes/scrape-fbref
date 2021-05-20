
import pandas as pd
import requests
from bs4 import BeautifulSoup


def save_to_excel(filename, stats_dict):

    # initialze the excel writer
    writer = pd.ExcelWriter(filename)

    # now loop thru and put each on a specific sheet
    for sheet, frame in stats_dict.items():
        frame.to_excel(writer, sheet_name=sheet)

    # critical last step
    writer.save()


def get_team_crests(base_url, urls):

    for team in urls.keys():

        page = requests.get(base_url+urls[team])
        soup = BeautifulSoup(page.text, 'lxml')
        team = team.replace(" ", "_")

        image_url = soup.find_all('img', {"class": "teamlogo"})[0].get('src')

        response = requests.get(image_url)

        file = open('crests/{0}.png'.format(team), "wb")
        file.write(response.content)
        file.close()


def get_competition_url(competition, season):

    country = league_to_country(competition)

    base_url = "https://fbref.com"
    base_competitions_url = "https://fbref.com/en/comps/"

    page_list_comps = requests.get(base_competitions_url)
    soup_comps = BeautifulSoup(page_list_comps.text, 'lxml')
    table_comps = soup_comps.find(
        'table', {"id": "comps_1_fa_club_league_senior"})
    rows_comps = table_comps.tbody.find_all('tr')

    url_comp = ""

    for i in range(len(rows_comps)):
        if rows_comps[i].find('td', {"data-stat": "country"}).text.split(" ")[1] == country:
            url_comp = base_url+rows_comps[i].find("a").get("href")
            break

    page_list_seasons = requests.get(url_comp)
    soup_seasons = BeautifulSoup(page_list_seasons.text, 'lxml')
    table_seasons = soup_seasons.find('table', {"id": "seasons"})
    rows_seasons = table_seasons.tbody.find_all('tr')

    url_season = ''

    for i in range(len(rows_seasons)):
        if rows_seasons[i].find('th', {'data-stat': 'season'}).text == season:
            url_season = base_url + rows_seasons[i].find("a").get("href")
            break

    return url_season


def league_to_country(league):

    league_country = {"Primeira Liga": "POR",
                      "Premier League": "ENG",
                      "Bundesliga": "GER",
                      "Ligue 1": "FRA",
                      "La Liga": "ESP",
                      "Serie A": "ITA"}

    return league_country[league]
