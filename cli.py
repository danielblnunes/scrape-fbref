
from PyInquirer import (Token, prompt,
                        style_from_dict)

from pyfiglet import figlet_format


import scrape
from utils import get_competition_url, save_to_excel


try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})


def log(string, color, font="speed", figlet=False):
    if colored:
        if not figlet:
            print(colored(string, color))
        else:
            print(colored(figlet_format(
                string, font=font), color))
    else:
        print(string)


questions = [
    {
        'type': 'list',
        'name': 'comp_option',
        'message': 'Choose the league',
        'choices': ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1", "Primeira Liga"]
    },
    {
        'type': 'list',
        'name': 'season_option',
        'message': 'Choose the season',
        'choices': ["2020-2021", "2019-2020", "2018-2019", "2017-2018"]
    },

    {
        'type': 'list',
        'name': 'level_option',
        'message': 'Team or player stats?',
        'choices': ["Team", "Player"]
    },

    {
        'type': "input",
        "name": "filename",
        "message": "Please specify the file name",
    }


]

final_question = [
    {
        'type': 'list',
        'name': 'final',
        'message': 'Do you want to download more stats?',
        'choices': ["Yes", "No(exit)"]
    }
]


def main():

    log("Fbref.com Stats", color="blue", figlet=True)
    log("Welcome to Fbref.com Scrape Tool", "green")

    flag_end = True

    while flag_end:
        answers = prompt(questions, style=style)

        competition = answers.get('comp_option')
        season = answers.get('season_option')
        level = answers.get('level_option')
        filename = answers.get("filename")

        comp_url = get_competition_url(competition, season)

        if level == "Team":
            log("Srapping and saving...", "green")
            team_stats = scrape.scrape_league_stats(comp_url)
            save_to_excel('data/'+filename+'.xlsx', team_stats)
        else:
            log("Srapping and saving...", "green")
            urls = scrape.get_urls_per_team(comp_url)
            player_stats = scrape.scrape_player_stats(urls)

            save_to_excel('data/'+filename+'.xlsx', player_stats)

        print('Download of {} stats for {} {} season done!!'.format(
            level, season, competition))

        final = prompt(final_question, style=style)

        final_answer = final.get('final')

        if final_answer == "No(exit)":
            flag_end = False

    print("Thank you for using this tool!")


if __name__ == "__main__":
    main()
